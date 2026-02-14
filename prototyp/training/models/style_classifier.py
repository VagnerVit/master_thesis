"""LSTM-based swimming style classifier

Classifies swimming style from keypoint sequences.

Architecture:
    Input: [batch, seq_len=32, keypoints=48, dims=3]
        ↓ Flatten keypoints
    [batch, 32, 144]
        ↓ LSTM (hidden=256, layers=2, bidirectional)
    [batch, 32, 512]
        ↓ Attention pooling
    [batch, 512]
        ↓ FC layers (512 → 128 → num_classes)
    [batch, num_classes]

Supports:
    - 4 swimming styles: freestyle, backstroke, breaststroke, butterfly
    - 5 camera views: Aerial, Front, Side_above_water, Side_underwater, Side_water_level
    - ONNX export for inference
"""

from dataclasses import dataclass
from typing import Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class StyleClassifierConfig:
    """Configuration for StyleClassifier model"""
    num_keypoints: int = 48
    keypoint_dims: int = 3
    sequence_length: int = 32
    hidden_size: int = 256
    num_lstm_layers: int = 2
    num_classes: int = 4
    dropout: float = 0.3
    bidirectional: bool = True
    use_attention: bool = True


class AttentionPooling(nn.Module):
    """Attention-based pooling over sequence dimension"""

    def __init__(self, hidden_size: int):
        super().__init__()
        self.attention = nn.Linear(hidden_size, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Input tensor [batch, seq_len, hidden_size]

        Returns:
            Pooled tensor [batch, hidden_size]
        """
        # Compute attention weights
        attn_weights = self.attention(x)  # [batch, seq_len, 1]
        attn_weights = F.softmax(attn_weights, dim=1)

        # Weighted sum
        return torch.sum(x * attn_weights, dim=1)  # [batch, hidden_size]


class StyleClassifier(nn.Module):
    """LSTM-based swimming style classifier

    Classifies keypoint sequences into swimming styles.
    """

    STYLE_NAMES = ["freestyle", "backstroke", "breaststroke", "butterfly"]

    def __init__(self, config: Optional[StyleClassifierConfig] = None):
        super().__init__()

        self.config = config or StyleClassifierConfig()
        c = self.config

        # Input projection
        input_size = c.num_keypoints * c.keypoint_dims
        self.input_proj = nn.Linear(input_size, c.hidden_size)
        self.input_norm = nn.LayerNorm(c.hidden_size)

        # LSTM layers
        lstm_hidden = c.hidden_size
        self.lstm = nn.LSTM(
            input_size=c.hidden_size,
            hidden_size=lstm_hidden,
            num_layers=c.num_lstm_layers,
            batch_first=True,
            dropout=c.dropout if c.num_lstm_layers > 1 else 0,
            bidirectional=c.bidirectional,
        )

        # Output size after LSTM
        lstm_output_size = lstm_hidden * (2 if c.bidirectional else 1)

        # Attention pooling
        self.use_attention = c.use_attention
        if c.use_attention:
            self.attention = AttentionPooling(lstm_output_size)
        else:
            self.attention = None

        # Classification head
        self.classifier = nn.Sequential(
            nn.Linear(lstm_output_size, c.hidden_size),
            nn.ReLU(),
            nn.Dropout(c.dropout),
            nn.Linear(c.hidden_size, c.num_classes),
        )

    def forward(
        self,
        keypoints: torch.Tensor,
        return_features: bool = False
    ) -> torch.Tensor | Tuple[torch.Tensor, torch.Tensor]:
        """Forward pass

        Args:
            keypoints: Input tensor [batch, seq_len, num_keypoints, dims]
            return_features: If True, also return intermediate features

        Returns:
            logits: Class logits [batch, num_classes]
            features: (optional) Features before classifier [batch, hidden_size]
        """
        batch_size, seq_len, num_kpts, dims = keypoints.shape

        # Flatten keypoints: [batch, seq_len, num_keypoints * dims]
        x = keypoints.view(batch_size, seq_len, -1)

        # Input projection and normalization
        x = self.input_proj(x)
        x = self.input_norm(x)

        # LSTM
        lstm_out, _ = self.lstm(x)  # [batch, seq_len, hidden*2]

        # Pooling
        if self.use_attention:
            features = self.attention(lstm_out)  # [batch, hidden*2]
        else:
            features = lstm_out[:, -1, :]  # Last hidden state

        # Classification
        logits = self.classifier(features)

        if return_features:
            return logits, features
        return logits

    def predict(self, keypoints: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Predict style with probabilities

        Args:
            keypoints: Input tensor [batch, seq_len, num_keypoints, dims]

        Returns:
            predictions: Predicted class indices [batch]
            probabilities: Class probabilities [batch, num_classes]
        """
        self.eval()
        with torch.no_grad():
            logits = self.forward(keypoints)
            probs = F.softmax(logits, dim=-1)
            preds = torch.argmax(probs, dim=-1)
        return preds, probs

    def get_style_name(self, class_idx: int) -> str:
        """Get style name from class index"""
        if 0 <= class_idx < len(self.STYLE_NAMES):
            return self.STYLE_NAMES[class_idx]
        return "unknown"

    @classmethod
    def from_checkpoint(cls, checkpoint_path: str) -> "StyleClassifier":
        """Load model from checkpoint"""
        checkpoint = torch.load(checkpoint_path, map_location="cpu")
        config = StyleClassifierConfig(**checkpoint.get("config", {}))
        model = cls(config)
        model.load_state_dict(checkpoint["model_state_dict"])
        return model

    def save_checkpoint(self, path: str, optimizer=None, epoch: int = 0, metrics: dict = None):
        """Save model checkpoint"""
        checkpoint = {
            "model_state_dict": self.state_dict(),
            "config": vars(self.config),
            "epoch": epoch,
            "metrics": metrics or {},
        }
        if optimizer is not None:
            checkpoint["optimizer_state_dict"] = optimizer.state_dict()
        torch.save(checkpoint, path)

    def export_onnx(self, path: str, opset_version: int = 14):
        """Export model to ONNX format

        Args:
            path: Output path for ONNX file
            opset_version: ONNX opset version
        """
        self.cpu()
        self.eval()
        c = self.config

        dummy_input = torch.randn(
            1, c.sequence_length, c.num_keypoints, c.keypoint_dims
        )

        torch.onnx.export(
            self,
            dummy_input,
            path,
            export_params=True,
            opset_version=opset_version,
            do_constant_folding=True,
            input_names=["keypoints"],
            output_names=["logits"],
            dynamic_axes={
                "keypoints": {0: "batch_size"},
                "logits": {0: "batch_size"},
            },
        )
