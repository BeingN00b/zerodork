# ZeroDork 🔎

> Advanced automated Google Dorking tool with multi-engine support, anti-bot logic, rich CLI, progress animations, and output logging.

## 🚀 Features

- Fetches latest Google dorks from Exploit-DB (GHDB)
- Multi-threaded searching across search engines
- Proxy-ready for low detection
- Rich CLI with argparse
- Progress bars and animations using `rich`
- Saves results in TXT/CSV/JSON formats
- Supports `--limit`, `--output`, and more!

## 🛠️ Usage

```bash
make install       # Installs all dependencies
make run           # Runs the script
python3 zerodork.py -h  # CLI help

Example:
python3 zerodork.py -u example.com --output results.txt --threads 10

📦 Installation:
git clone https://github.com/<your-username>/zerodork.git
cd zerodork
make install

🧩 Requirements
	•	Python 3.7+
	•	Internet connection
	•	requests, beautifulsoup4, tqdm, rich

Install manually if needed:
pip install -r requirements.txt

📂 Output Formats
	•	--output-format txt (default)
	•	--output-format csv
	•	--output-format json

🧠 To-Do:
API-based Google/Bing support
