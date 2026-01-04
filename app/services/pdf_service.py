from pypdf import PdfReader
from io import BytesIO

class PdfService:
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """
        Extracts raw text from a PDF file provided as bytes.
        """
        try:
            reader = PdfReader(BytesIO(file_content))
            text = ""
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
            return text.strip()
        except Exception as e:
            # Handle specific PDF exceptions or log the error
            print(f"Error extracting text from PDF: {e}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
