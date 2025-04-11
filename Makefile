# Makefile for ZeroDork

APP_NAME = zerodork
PYTHON = python3

install:
	@echo "[+] Installing dependencies..."
	pip install -r requirements.txt
	@echo "[✓] Done."

run:
	@echo "[+] Running $(APP_NAME).py..."
	$(PYTHON) $(APP_NAME).py

help:
	@echo "ZeroDork CLI commands:"
	@echo "  make install   - Install all dependencies"
	@echo "  make run       - Run the ZeroDork script"
	@echo "  make help      - Show this help menu"

clean:
	@echo "[+] Cleaning up __pycache__ and .pyc files..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -name "*.pyc" -delete
	@echo "[✓] Clean complete."
