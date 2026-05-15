import os
import json
import logging
from bs4 import BeautifulSoup
import requests
import fitz  # PyMuPDF
import docx
import pytesseract
from PIL import Image

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

class DataIngestionPipeline:
    def __init__(self):
        # Configure tesseract path if on Windows (update path as needed)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass

    def clean_text(self, text: str) -> str:
        """Removes excessive newlines and whitespace."""
        if not text:
            return ""
        return " ".join(text.split()).strip()

    def extract_pdf(self, file_path: str) -> str:
        """Extracts text from PDF using PyMuPDF, handling multi-page."""
        text = ""
        try:
            with fitz.open(file_path) as pdf:
                for page_num in range(len(pdf)):
                    page = pdf.load_page(page_num)
                    # Simple heuristic: ignore top 5% (header) and bottom 5% (footer)
                    rect = page.rect
                    clip = fitz.Rect(0, rect.height * 0.05, rect.width, rect.height * 0.95)
                    text += page.get_text(clip=clip) + "\n"
        except Exception as e:
            logger.error(f"Error reading PDF {file_path}: {e}")
        return self.clean_text(text)

    def extract_json(self, file_path: str) -> str:
        """Extracts and flattens JSON data into readable text."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert JSON structure to readable text format
            text_lines = []
            if isinstance(data, list):
                for item in data:
                    text_lines.append(json.dumps(item, indent=2))
            else:
                text_lines.append(json.dumps(data, indent=2))
                
            return self.clean_text(" ".join(text_lines))
        except Exception as e:
            logger.error(f"Error reading JSON {file_path}: {e}")
            return ""

    def extract_docx(self, file_path: str) -> str:
        """Extracts text from DOCX while maintaining paragraphs."""
        try:
            doc = docx.Document(file_path)
            full_text = [para.text for para in doc.paragraphs if para.text.strip()]
            return self.clean_text("\n".join(full_text))
        except Exception as e:
            logger.error(f"Error reading DOCX {file_path}: {e}")
            return ""

    def extract_image(self, file_path: str) -> str:
        """Extracts text from images using Tesseract OCR."""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return self.clean_text(text)
        except Exception as e:
            logger.error(f"Error performing OCR on {file_path}: {e}")
            return ""

    def scrape_url(self, url: str) -> str:
        """Scrapes text from Web Links, removing scripts and styles."""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Remove scripts, styles, headers, and navs
            for script in soup(["script", "style", "header", "footer", "nav"]):
                script.extract()
                
            text = soup.get_text(separator=' ')
            return self.clean_text(text)
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return ""

    def process_file(self, file_path: str, source_type: str, domain: str):
        """Routes file to correct parser, extracts text, formats, and saves."""
        logger.info(f"Processing {file_path} [{source_type}]")
        filename = os.path.basename(file_path)
        extracted_text = ""

        if source_type == "pdf":
            extracted_text = self.extract_pdf(file_path)
        elif source_type == "json":
            extracted_text = self.extract_json(file_path)
        elif source_type == "docx":
            extracted_text = self.extract_docx(file_path)
        elif source_type == "image":
            extracted_text = self.extract_image(file_path)
            
        self._save_processed_data(extracted_text, filename, source_type, domain)

    def process_links(self, links_file: str, domain: str):
        """Reads a file containing URLs and processes each one."""
        try:
            with open(links_file, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f.readlines() if line.strip()]
                
            for url in urls:
                logger.info(f"Processing URL: {url}")
                extracted_text = self.scrape_url(url)
                # Use a safe filename based on the URL
                safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_")[:50] + ".txt"
                self._save_processed_data(extracted_text, safe_name, "web", domain)
        except Exception as e:
            logger.error(f"Error processing links file {links_file}: {e}")

    def _save_processed_data(self, text: str, source_name: str, source_type: str, domain: str):
        """Standardizes data into a JSON format and saves to the processed folder."""
        if len(text) < 50:
            logger.warning(f"Skipping {source_name}: Extracted text too short.")
            return

        # Limit text length per file to prevent memory overflow (e.g., 500k chars)
        text = text[:500000]

        output_data = {
            "text": text,
            "metadata": {
                "domain": domain,
                "source_type": source_type,
                "source_name": source_name
            }
        }

        # Determine target directory
        target_dir = os.path.join(PROCESSED_DIR, domain)
        os.makedirs(target_dir, exist_ok=True)
        
        # Save as JSON
        output_filename = f"{source_name}_processed.json"
        output_path = os.path.join(target_dir, output_filename)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=4)
            logger.info(f"Successfully saved structured data to {output_path}")
        except Exception as e:
            logger.error(f"Error saving {output_path}: {e}")

    def determine_domain(self, filename: str) -> str:
        """Determines the domain based on keyword matching in the filename."""
        filename_lower = filename.lower()
        if any(keyword in filename_lower for keyword in ["university", "admission", "syllabus", "placement", "faculty"]):
            return "university"
        elif any(keyword in filename_lower for keyword in ["company", "infosys", "hr", "policy", "report"]):
            return "company"
        return "custom"

    def run_pipeline(self):
        """Batch processes all files in raw directories according to STRICT structure."""
        logger.info("PIPELINE START: RAW DATA → TYPE DETECTION → PARSING → CLEANING → METADATA ADDITION → SAVE TO PROCESSED → READY FOR RAG")
        
        source_types = ["pdf", "json", "docx", "images"]
        for stype in source_types:
            raw_type_dir = os.path.join(RAW_DIR, stype)
            if not os.path.exists(raw_type_dir):
                os.makedirs(raw_type_dir, exist_ok=True)
                continue
                
            for filename in os.listdir(raw_type_dir):
                file_path = os.path.join(raw_type_dir, filename)
                if os.path.isfile(file_path):
                    domain = self.determine_domain(filename)
                    # Convert 'images' folder name to 'image' type
                    p_type = "image" if stype == "images" else stype
                    self.process_file(file_path, p_type, domain)
        
        # Process Web Links
        links_dir = os.path.join(RAW_DIR, "links")
        if not os.path.exists(links_dir):
            os.makedirs(links_dir, exist_ok=True)
        else:
            for filename in os.listdir(links_dir):
                if filename.endswith(".txt"):
                    domain = self.determine_domain(filename)
                    self.process_links(os.path.join(links_dir, filename), domain)

if __name__ == "__main__":
    pipeline = DataIngestionPipeline()
    pipeline.run_pipeline()
    logger.info("Advanced Ingestion Pipeline Completed Successfully.")
