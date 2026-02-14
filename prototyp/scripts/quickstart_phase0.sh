#!/bin/bash
# Quick Start script for Phase 0 - Dataset Setup (Linux/Mac)
# Run: bash scripts/quickstart_phase0.sh

set -e

echo "================================================"
echo "SwimAth Phase 0: Dataset Setup Quick Start"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Phase 0 dependencies
echo ""
echo "Installing Phase 0 dependencies..."
pip install -r requirements-phase0.txt

echo ""
echo "================================================"
echo "Phase 0 Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Download annotations only (6.7 GB):"
echo "   python scripts/download_dataset.py --dataset swimxyz --annotations-only"
echo ""
echo "2. Download Freestyle videos Part 1 (37.5 GB):"
echo "   python scripts/download_dataset.py --dataset swimxyz --style freestyle --part 1"
echo ""
echo "3. Prepare dataset for training:"
echo "   python scripts/prepare_dataset.py --dataset swimxyz --style freestyle"
echo ""
echo "4. Verify dataset:"
echo "   python scripts/verify_dataset.py --dataset swimxyz --style freestyle --detailed"
echo ""
echo "See PHASE0_DATASET_SETUP.md for full documentation."
echo ""
