from flask import current_app
from pathlib import Path
from app.utils.retriever.download_papers import download_pdfs as download_pdfs_external

class DownloadService:
    @staticmethod
    def download_paper_pdfs(pdf_urls: list[dict]) -> list[str]:
        """Downloads PDFs and returns a list of local file paths for successfully downloaded files."""
        save_dir = Path(current_app.config['PAPER_SAVE_DIR'])
        save_dir.mkdir(parents=True, exist_ok=True)
        
        successfully_downloaded_paths = []
        import requests

        for item in pdf_urls:
            url = item.get("pdf_url")
            paper_id = item.get("paper_id")

            if not url or not paper_id:
                current_app.logger.warning(f"Missing pdf_url or paper_id in item: {item}. Skipping download.")
                continue

            # Sanitize paper_id for use as a filename
            safe_paper_id = paper_id.replace('/', '_').replace(':', '_')
            file_name = f"{safe_paper_id}.pdf"
            file_path = save_dir / file_name

            if file_path.exists():
                current_app.logger.info(f"[✓] Already exists: {file_path}")
                successfully_downloaded_paths.append(str(file_path))
                continue

            current_app.logger.info(f"Downloading {file_name} from {url}...")
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                with open(file_path, "wb") as f:
                    f.write(response.content)
                current_app.logger.info(f"[✓] Downloaded: {file_path}")
                successfully_downloaded_paths.append(str(file_path))
            except requests.exceptions.RequestException as e:
                current_app.logger.error(f"[✗] Failed to download PDF {url}: {e}")
            except Exception as e:
                current_app.logger.error(f"[✗] An unexpected error occurred while downloading {url}: {e}")
        
        return successfully_downloaded_paths