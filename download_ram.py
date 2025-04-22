# download_ram.py
#!/usr/bin/env python3
import urllib.request
import sys

URL = "https://web.archive.org/web/20011004233905/file:////CCXA10/%83f%81%5B%83%5E/HomePage/hakke_shoukai/ram/hakkelive9911.ram"
OUTPUT_PATH = "hakkelive9911.ram"

def download_file(url: str, output_path: str) -> None:
    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"Downloaded → {output_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    download_file(URL, OUTPUT_PATH)
