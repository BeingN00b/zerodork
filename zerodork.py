import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor
import argparse
import json
import csv
import os
from tqdm import tqdm
from rich.console import Console

console = Console()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_dorks():
    console.print("[cyan]🧠 Fetching dorks from Exploit-DB...[/cyan]")
    url = "https://www.exploit-db.com/google-hacking-database"
    response = requests.get(url, headers=HEADERS)
    dorks = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for row in soup.find_all("tr", class_="dork"):
            try:
                dork = row.find("td", class_="dork").text.strip()
                if dork:
                    dorks.append(dork)
            except:
                continue
    else:
        console.print(f"[red]Failed to fetch dorks: {response.status_code}[/red]")
    return dorks

def perform_search(dork, domain, engine="duckduckgo"):
    query = f"{dork} site:{domain}"
    encoded_query = quote_plus(query)

    if engine == "duckduckgo":
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    elif engine == "brave":
        url = f"https://search.brave.com/search?q={encoded_query}"
    else:
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200 and "html" in res.headers.get("Content-Type", ""):
            return {"query": query, "status": "ok", "engine": engine, "url": url}
        else:
            return {"query": query, "status": "error", "engine": engine, "url": url}
    except Exception as e:
        return {"query": query, "status": "fail", "error": str(e), "engine": engine, "url": url}

def save_results(results, base_filename):
    txt_file = f"{base_filename}.txt"
    csv_file = f"{base_filename}.csv"
    json_file = f"{base_filename}.json"

    with open(txt_file, "w") as f:
        for r in results:
            f.write(f"{r['engine']}: {r['query']} → {r['url']} ({r['status']})\n")

    with open(csv_file, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["engine", "query", "url", "status", "error"])
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    with open(json_file, "w") as f:
        json.dump(results, f, indent=4)

    console.print(f"\n[green]✅ Dorking completed![/green]")
    console.print(f"📁 [bold]Results saved as:[/bold] [yellow]{txt_file}[/yellow], [yellow]{csv_file}[/yellow], [yellow]{json_file}[/yellow]")

def main():
    parser = argparse.ArgumentParser(description="ZeroDork - Google Dorking Automation Tool")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g. example.com)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("-o", "--output", default="zerodork_output", help="Base name for output files")
    parser.add_argument("-e", "--engine", default="duckduckgo", choices=["duckduckgo", "brave"], help="Search engine to use")
    parser.add_argument("--limit", type=int, default=50, help="Limit number of dorks used (default: 50)")
    
    args = parser.parse_args()

    dorks = fetch_dorks()
    if not dorks:
        console.print("[red]No dorks found. Exiting.[/red]")
        return

    selected_dorks = dorks[:args.limit]

    results = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(perform_search, dork, args.domain, args.engine) for dork in selected_dorks]
        for f in tqdm(futures, desc="🔍 Dorking Progress", colour="green"):
            results.append(f.result())

    save_results(results, args.output)

if __name__ == "__main__":
    main()
