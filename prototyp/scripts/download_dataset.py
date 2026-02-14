"""Download script for SwimAth datasets

Automates downloading of SwimXYZ and other swimming datasets from various sources.

Usage:
    python download_dataset.py --dataset swimxyz --annotations-only
    python download_dataset.py --dataset swimxyz --style freestyle --part 1
    python download_dataset.py --dataset swimxyz --all-styles --all-parts
"""

import argparse
import sys
from pathlib import Path
from typing import Optional
import subprocess
import zipfile
from urllib.request import urlretrieve
from tqdm import tqdm

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from utils.logging_config import setup_logging, get_logger

# Setup logging
log_file = Path.home() / ".swimath" / "logs" / "download.log"
setup_logging(log_file=log_file, console=True)
logger = get_logger(__name__)


# SwimXYZ Zenodo URLs
SWIMXYZ_URLS = {
    "annotations": {
        "backstroke": "https://zenodo.org/record/8399376/files/Backstroke_labels.zip",
        "breaststroke": "https://zenodo.org/record/8399376/files/Breaststroke_labels.zip",
        "butterfly": "https://zenodo.org/record/8399376/files/Butterfly_labels.zip",
        "freestyle": "https://zenodo.org/record/8399376/files/Freestyle_labels.zip",
        "smpl": "https://zenodo.org/record/8399376/files/smpl_swimming_motions.zip",
    },
    "videos": {
        "backstroke": {
            "part1": "https://zenodo.org/record/8399837",
            "part2": "https://zenodo.org/record/8401680",
        },
        "breaststroke": {
            "part1": "https://zenodo.org/record/8401898",
            "part2": "https://zenodo.org/record/8401923",
        },
        "butterfly": {
            "part1": "https://zenodo.org/record/8401954",
            "part2": "https://zenodo.org/record/8401974",
        },
        "freestyle": {
            "part1": "https://zenodo.org/record/8402009",
            "part2": "https://zenodo.org/record/8402031",
        },
    }
}


class DownloadProgressBar(tqdm):
    """Progress bar for URL downloads"""

    def update_to(self, b: int = 1, bsize: int = 1, tsize: Optional[int] = None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_file(url: str, output_path: Path, resume: bool = False) -> bool:
    """Download file with progress bar

    Args:
        url: URL to download
        output_path: Destination file path
        resume: Whether to resume partial download

    Returns:
        True if successful
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not resume:
        logger.info(f"File already exists: {output_path.name}")
        return True

    logger.info(f"Downloading: {url} -> {output_path.name}")

    try:
        with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=output_path.name) as t:
            urlretrieve(url, output_path, reporthook=t.update_to)
        logger.info(f"Downloaded: {output_path.name}")
        return True
    except Exception as e:
        logger.error(f"Download failed: {e}")
        if output_path.exists():
            output_path.unlink()
        return False


def download_with_zenodo_get(record_id: str, output_dir: Path) -> bool:
    """Download using zenodo_get (faster for large files)

    Args:
        record_id: Zenodo record ID
        output_dir: Output directory

    Returns:
        True if successful
    """
    try:
        cmd = ["zenodo_get", "-r", record_id, "-o", str(output_dir)]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"Downloaded Zenodo record {record_id}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"zenodo_get failed: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.warning("zenodo_get not installed. Install with: pip install zenodo_get")
        return False


def extract_zip(zip_path: Path, output_dir: Path) -> bool:
    """Extract ZIP archive

    Args:
        zip_path: Path to ZIP file
        output_dir: Extraction directory

    Returns:
        True if successful
    """
    logger.info(f"Extracting: {zip_path.name}")

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        logger.info(f"Extracted to: {output_dir}")
        return True
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return False


def download_swimxyz_annotations(data_dir: Path) -> bool:
    """Download SwimXYZ annotation files

    Args:
        data_dir: Data directory

    Returns:
        True if all downloads successful
    """
    logger.info("Downloading SwimXYZ annotations (6.7 GB)...")

    downloads_dir = data_dir / "downloads"
    annotations_dir = data_dir / "swimxyz" / "annotations"

    downloads_dir.mkdir(parents=True, exist_ok=True)
    annotations_dir.mkdir(parents=True, exist_ok=True)

    all_success = True

    for style, url in SWIMXYZ_URLS["annotations"].items():
        zip_path = downloads_dir / f"{style}_labels.zip"

        # Determine extract directory
        if style == "smpl":
            extract_dir = annotations_dir / "smpl_swimming_motions"
        else:
            extract_dir = annotations_dir / f"{style.capitalize()}_labels"

        # Skip if already extracted
        if extract_dir.exists() and any(extract_dir.iterdir()):
            logger.info(f"Already extracted: {extract_dir.name}")
            continue

        # Download
        if not download_file(url, zip_path):
            all_success = False
            continue

        # Extract
        if not extract_zip(zip_path, extract_dir):
            all_success = False

    return all_success


def download_swimxyz_videos(
    data_dir: Path,
    style: str,
    part: Optional[int] = None,
    use_zenodo_get: bool = True
) -> bool:
    """Download SwimXYZ video files

    Args:
        data_dir: Data directory
        style: Swimming style (freestyle, backstroke, breaststroke, butterfly)
        part: Part number (1 or 2), None for both
        use_zenodo_get: Whether to use zenodo_get (faster)

    Returns:
        True if successful
    """
    if style not in SWIMXYZ_URLS["videos"]:
        logger.error(f"Invalid style: {style}")
        return False

    parts = [part] if part else [1, 2]
    all_success = True

    for p in parts:
        part_key = f"part{p}"
        record_url = SWIMXYZ_URLS["videos"][style][part_key]
        record_id = record_url.split("/")[-1]

        logger.info(f"Downloading SwimXYZ {style} {part_key} (~37.5 GB)...")

        videos_dir = data_dir / "swimxyz" / "videos" / style / part_key
        videos_dir.mkdir(parents=True, exist_ok=True)

        # Try zenodo_get first (faster)
        if use_zenodo_get:
            if download_with_zenodo_get(record_id, videos_dir):
                continue

        # Fallback: manual download (slower)
        logger.warning(f"Manual download not implemented for videos. Use zenodo_get:")
        logger.warning(f"  cd {videos_dir}")
        logger.warning(f"  zenodo_get -r {record_id}")
        all_success = False

    return all_success


def list_available_datasets():
    """List available datasets"""
    print("\n📦 Available Datasets:\n")

    print("1. SwimXYZ (Zenodo)")
    print("   - Annotations: 6.7 GB")
    print("   - Videos (per style): ~75 GB")
    print("   - Styles: freestyle, backstroke, breaststroke, butterfly")
    print("   - Usage: --dataset swimxyz --style <style> --part <1|2>")
    print()

    print("2. Roboflow Swimming Strokes")
    print("   - Size: ~100 MB")
    print("   - Manual download: https://universe.roboflow.com/gecko-vision/swimming-strokes-detection")
    print()

    print("3. SwimTrack (MediaEval 2022)")
    print("   - Requires registration: https://forms.gle/JcKoa5ycxR2KEiTJ7")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Download SwimAth datasets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download only annotations (6.7 GB)
  python download_dataset.py --dataset swimxyz --annotations-only

  # Download Freestyle Part 1 videos (~37.5 GB)
  python download_dataset.py --dataset swimxyz --style freestyle --part 1

  # Download all Freestyle videos (~75 GB)
  python download_dataset.py --dataset swimxyz --style freestyle --all-parts

  # Download everything (~300 GB)
  python download_dataset.py --dataset swimxyz --all-styles --all-parts
        """
    )

    parser.add_argument("--dataset", type=str, choices=["swimxyz"], default="swimxyz",
                        help="Dataset to download")
    parser.add_argument("--style", type=str, choices=["freestyle", "backstroke", "breaststroke", "butterfly"],
                        help="Swimming style")
    parser.add_argument("--part", type=int, choices=[1, 2],
                        help="Video part (1 or 2)")
    parser.add_argument("--annotations-only", action="store_true",
                        help="Download only annotations (no videos)")
    parser.add_argument("--all-styles", action="store_true",
                        help="Download all styles")
    parser.add_argument("--all-parts", action="store_true",
                        help="Download all parts")
    parser.add_argument("--output-dir", type=Path, default=Path("data"),
                        help="Output directory (default: ./data)")
    parser.add_argument("--resume", action="store_true",
                        help="Resume interrupted download")
    parser.add_argument("--list", action="store_true",
                        help="List available datasets")
    parser.add_argument("--no-zenodo-get", action="store_true",
                        help="Don't use zenodo_get (slower)")

    args = parser.parse_args()

    if args.list:
        list_available_datasets()
        return 0

    logger.info(f"Starting download to: {args.output_dir}")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.dataset == "swimxyz":
        # Download annotations
        if not download_swimxyz_annotations(args.output_dir):
            logger.error("Annotation download failed")
            return 1

        # Download videos if requested
        if not args.annotations_only:
            styles = ["freestyle", "backstroke", "breaststroke", "butterfly"] if args.all_styles else [args.style]

            if args.style is None and not args.all_styles:
                logger.error("Specify --style or --all-styles for video download")
                return 1

            for style in styles:
                part = None if args.all_parts else args.part
                if not download_swimxyz_videos(
                    args.output_dir,
                    style,
                    part,
                    use_zenodo_get=not args.no_zenodo_get
                ):
                    logger.warning(f"Video download incomplete for {style}")

    logger.info("Download complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
