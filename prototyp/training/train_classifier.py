"""Training script for swimming style classifier

Usage:
    python -m training.train_classifier --style freestyle --epochs 50
    python -m training.train_classifier --multi-style --epochs 100

Features:
    - CUDA/CPU automatic detection
    - Mixed precision training (AMP)
    - Learning rate scheduling (CosineAnnealing)
    - Early stopping
    - TensorBoard logging
    - Checkpoint saving
"""

import argparse
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple

import torch
import torch.nn as nn
from torch.cuda.amp import GradScaler, autocast
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from tqdm import tqdm

from .dataset_loader import create_dataloaders, create_multistyle_dataloaders, SwimXYZDataset
from .models.style_classifier import StyleClassifier, StyleClassifierConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class EarlyStopping:
    """Early stopping to prevent overfitting"""

    def __init__(self, patience: int = 10, min_delta: float = 0.001):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = float("inf")
        self.should_stop = False

    def __call__(self, val_loss: float) -> bool:
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
        return self.should_stop


def train_epoch(
    model: nn.Module,
    train_loader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    scaler: Optional[GradScaler] = None,
) -> Tuple[float, float]:
    """Train for one epoch

    Returns:
        (average_loss, accuracy)
    """
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    for batch in tqdm(train_loader, desc="Training", leave=False):
        keypoints = batch["keypoints"].to(device)
        labels = batch["style_label"].to(device)

        optimizer.zero_grad()

        if scaler is not None:
            with autocast():
                logits = model(keypoints)
                loss = criterion(logits, labels)

            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            scaler.step(optimizer)
            scaler.update()
        else:
            logits = model(keypoints)
            loss = criterion(logits, labels)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

        total_loss += loss.item() * keypoints.size(0)
        preds = torch.argmax(logits, dim=-1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    avg_loss = total_loss / total
    accuracy = correct / total

    return avg_loss, accuracy


@torch.no_grad()
def evaluate(
    model: nn.Module,
    val_loader,
    criterion: nn.Module,
    device: torch.device,
) -> Tuple[float, float, Dict[str, float]]:
    """Evaluate model

    Returns:
        (average_loss, accuracy, per_class_accuracy)
    """
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    class_correct: Dict[int, int] = {}
    class_total: Dict[int, int] = {}

    for batch in tqdm(val_loader, desc="Evaluating", leave=False):
        keypoints = batch["keypoints"].to(device)
        labels = batch["style_label"].to(device)

        logits = model(keypoints)
        loss = criterion(logits, labels)

        total_loss += loss.item() * keypoints.size(0)
        preds = torch.argmax(logits, dim=-1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

        for pred, label in zip(preds, labels):
            label_int = label.item()
            class_total[label_int] = class_total.get(label_int, 0) + 1
            if pred == label:
                class_correct[label_int] = class_correct.get(label_int, 0) + 1

    avg_loss = total_loss / total
    accuracy = correct / total

    per_class_acc = {}
    for cls in class_total:
        per_class_acc[StyleClassifier.STYLE_NAMES[cls]] = (
            class_correct.get(cls, 0) / class_total[cls]
        )

    return avg_loss, accuracy, per_class_acc


def train(
    data_dir: Path,
    style: str = "freestyle",
    multi_style: bool = False,
    epochs: int = 50,
    batch_size: int = 32,
    learning_rate: float = 1e-3,
    weight_decay: float = 1e-4,
    patience: int = 10,
    output_dir: Path = Path("models"),
    use_amp: bool = True,
):
    """Main training function

    Args:
        data_dir: Data directory
        style: Swimming style (if not multi_style)
        multi_style: Train on all styles
        epochs: Number of training epochs
        batch_size: Batch size
        learning_rate: Initial learning rate
        weight_decay: Weight decay for AdamW
        patience: Early stopping patience
        output_dir: Directory for checkpoints
        use_amp: Use automatic mixed precision
    """
    # Setup device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")

    if device.type == "cuda":
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")

    # Create dataloaders
    if multi_style:
        logger.info("Loading dataset: all styles (multi-style mode)")
        train_loader, val_loader, test_loader = create_multistyle_dataloaders(
            data_dir=data_dir,
            batch_size=batch_size,
            num_workers=0,  # Windows compatibility
            pin_memory=device.type == "cuda",
        )
    else:
        logger.info(f"Loading dataset: {style}")
        train_loader, val_loader, test_loader = create_dataloaders(
            data_dir=data_dir,
            style=style,
            batch_size=batch_size,
            num_workers=0,  # Windows compatibility
            pin_memory=device.type == "cuda",
        )

    logger.info(f"Train samples: {len(train_loader.dataset)}")
    logger.info(f"Val samples: {len(val_loader.dataset)}")
    logger.info(f"Test samples: {len(test_loader.dataset)}")

    # Get dataset info
    if multi_style:
        # ConcatDataset - get info from first sub-dataset
        first_ds: SwimXYZDataset = train_loader.dataset.datasets[0]
        num_keypoints = first_ds.get_num_keypoints()
    else:
        train_ds: SwimXYZDataset = train_loader.dataset
        num_keypoints = train_ds.get_num_keypoints()
    logger.info(f"Keypoints: {num_keypoints}")

    # Create model
    config = StyleClassifierConfig(
        num_keypoints=num_keypoints,
        keypoint_dims=3,
        sequence_length=32,
        hidden_size=256,
        num_lstm_layers=2,
        num_classes=4 if multi_style else 1,  # Binary for single style
        dropout=0.3,
        bidirectional=True,
        use_attention=True,
    )

    # For single style, we still use 4 classes but train on one
    config.num_classes = 4

    model = StyleClassifier(config).to(device)
    logger.info(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

    # Loss, optimizer, scheduler
    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(
        model.parameters(),
        lr=learning_rate,
        weight_decay=weight_decay
    )
    scheduler = CosineAnnealingLR(optimizer, T_max=epochs)

    # Mixed precision
    scaler = GradScaler() if use_amp and device.type == "cuda" else None

    # Early stopping
    early_stopping = EarlyStopping(patience=patience)

    # Training loop
    output_dir.mkdir(parents=True, exist_ok=True)
    best_val_acc = 0.0
    best_epoch = 0

    logger.info(f"Starting training for {epochs} epochs...")
    start_time = time.time()

    for epoch in range(1, epochs + 1):
        epoch_start = time.time()

        # Train
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device, scaler
        )

        # Validate
        val_loss, val_acc, per_class_acc = evaluate(
            model, val_loader, criterion, device
        )

        # Update scheduler
        scheduler.step()

        epoch_time = time.time() - epoch_start

        # Logging
        logger.info(
            f"Epoch {epoch}/{epochs} | "
            f"Train Loss: {train_loss:.4f}, Acc: {train_acc:.4f} | "
            f"Val Loss: {val_loss:.4f}, Acc: {val_acc:.4f} | "
            f"LR: {scheduler.get_last_lr()[0]:.6f} | "
            f"Time: {epoch_time:.1f}s"
        )

        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_epoch = epoch
            model.save_checkpoint(
                output_dir / "best_model.pt",
                optimizer=optimizer,
                epoch=epoch,
                metrics={"val_acc": val_acc, "val_loss": val_loss}
            )
            logger.info(f"New best model saved (val_acc={val_acc:.4f})")

        # Early stopping
        if early_stopping(val_loss):
            logger.info(f"Early stopping at epoch {epoch}")
            break

    total_time = time.time() - start_time
    logger.info(f"Training complete in {total_time/60:.1f} minutes")
    logger.info(f"Best val accuracy: {best_val_acc:.4f} at epoch {best_epoch}")

    # Final evaluation on test set
    logger.info("Evaluating on test set...")
    model = StyleClassifier.from_checkpoint(str(output_dir / "best_model.pt"))
    model.to(device)

    test_loss, test_acc, test_per_class = evaluate(
        model, test_loader, criterion, device
    )

    logger.info(f"Test Loss: {test_loss:.4f}, Accuracy: {test_acc:.4f}")
    for style_name, acc in test_per_class.items():
        logger.info(f"  {style_name}: {acc:.4f}")

    # Export to ONNX
    onnx_path = output_dir / "style_classifier.onnx"
    model.export_onnx(str(onnx_path))
    logger.info(f"ONNX model saved to {onnx_path}")

    # Save final metrics
    metrics = {
        "style": style,
        "multi_style": multi_style,
        "best_epoch": best_epoch,
        "best_val_acc": best_val_acc,
        "test_acc": test_acc,
        "test_per_class": test_per_class,
        "total_epochs": epoch,
        "training_time_minutes": total_time / 60,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    import json
    with open(output_dir / "training_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    return test_acc


def main():
    parser = argparse.ArgumentParser(description="Train swimming style classifier")
    parser.add_argument("--style", type=str, default="freestyle",
                       help="Swimming style")
    parser.add_argument("--multi-style", action="store_true",
                       help="Train on all styles")
    parser.add_argument("--data-dir", type=Path, default=Path("data"),
                       help="Data directory")
    parser.add_argument("--output-dir", type=Path, default=Path("models"),
                       help="Output directory for checkpoints")
    parser.add_argument("--epochs", type=int, default=50,
                       help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=32,
                       help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-3,
                       help="Learning rate")
    parser.add_argument("--patience", type=int, default=10,
                       help="Early stopping patience")
    parser.add_argument("--no-amp", action="store_true",
                       help="Disable mixed precision")

    args = parser.parse_args()

    train(
        data_dir=args.data_dir,
        style=args.style,
        multi_style=args.multi_style,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        patience=args.patience,
        output_dir=args.output_dir,
        use_amp=not args.no_amp,
    )


if __name__ == "__main__":
    main()
