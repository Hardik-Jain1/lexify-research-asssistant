import requests
from pathlib import Path

def download_pdfs(pdf_urls: list, save_dir: str = "data/papers/") -> None:
    """
    Downloads PDFs from a list of dicts containing PDF URLs.
    Each item in pdf_urls should be a dict with a 'pdf_url' key.
    Only downloads if the file does not already exist in the directory.
    """
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    for item in pdf_urls:
        if "pdf_url" not in item:
            raise ValueError("Each item must contain a 'pdf_url' key.")
        url = item["pdf_url"]
        file_name = f"{url.split('/')[-1]}.pdf"
        file_path = save_path / file_name
        if file_path.exists():
            print(f"[✓] Already exists: {file_path}")
            continue
        print(f"Downloading {file_name} from {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"[✓] Downloaded: {file_path}")
        else:
            print(f"[✗] Failed to download PDF: {url}")
