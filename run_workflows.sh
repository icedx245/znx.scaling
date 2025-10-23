#!/bin/bash
# Automation script to run all workflow streams in order

set -e

python3 workflows/data_ingestion.py
python3 workflows/data_cleaning.py
python3 workflows/data_analysis.py
python3 workflows/data_visualization.py

echo "All workflows completed successfully."