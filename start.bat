@echo off
python --version && (
    python -m pip install -r requirements.txt
    python main.py
) || (
    echo "An error occurred during startup. Please ensure that Python is installed."
)