import os
import fitz  # PyMuPDF
import logging
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class GeminiExtractor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logging.error("GEMINI_API_KEY missing from .env file!")
            raise ValueError("Please set your GEMINI_API_KEY in the .env file.")
        
        genai.configure(api_key=self.api_key)
        
        try:
            # 1. List available models to see what your key supports
            available_models = [m.name for m in genai.list_models() 
                               if 'generateContent' in m.supported_generation_methods]
            
            # 2. Pick the best available one (Priority: Flash -> Pro)
            selected_model = None
            for model_name in ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]:
                if model_name in available_models:
                    selected_model = model_name
                    break
            
            if not selected_model:
                # Fallback to the first available if none of our preferred ones are found
                selected_model = available_models[0]

            logging.info(f"Using Model: {selected_model}")
            self.model = genai.GenerativeModel(selected_model)
            
        except Exception as e:
            logging.error(f"Discovery Error: {e}")
            # If discovery fails, we try the most basic legacy name
            self.model = genai.GenerativeModel("gemini-pro")

    def read_pdf(self, pdf_path):
        """Extract raw text from PDF and provide clear error feedback."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at: {pdf_path}")

        logging.info(f"Reading PDF: {pdf_path}")
        text = ""
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                text += page.get_text()
            doc.close()
            
            # CRITICAL CHECK: Is the text actually there?
            if not text.strip():
                logging.error("The PDF has no text layer. It is likely a scanned image.")
                raise ValueError("PDF is empty or contains only images/scans.")
            
            return text
        except Exception as e:
            logging.error(f"PyMuPDF Error: {e}")
            raise

    def extract_structured_data(self, raw_text):
        prompt = f"""
        Extract the following insurance fields from the text into a JSON object.
        
        REQUIRED KEYS:
        - policy_number
        - policyholder_name
        - effective_dates
        - incident_date
        - incident_location
        - incident_description
        - claim_type
        - estimated_damage (Provide as a number)

        STRICT RULES:
        1. If a field is not found in the text, you MUST use the JSON value null.
        2. Do not use strings like "Not Found". Use null.
        3. Return ONLY valid JSON.

        TEXT:
        {raw_text}
        """

        try:
            response = self.model.generate_content(prompt)
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            
            # Ensure the output is wrapped correctly for the validator
            return {"extractedFields": data}
        except Exception as e:
            return {"extractedFields": {}}
        

# --- Independent Test Script ---
if __name__ == "__main__":
    extractor = GeminiExtractor()
    try:
        # Replace with your actual test file path
        test_file = "data/sample_fnol.pdf"
        
        # Run Extraction
        raw_content = extractor.read_pdf(test_file)
        print(f"\n--- Preview of Raw Text ---\n{raw_content[:200]}...")
        
        final_json = extractor.extract_structured_data(raw_content)
        print("\n--- Structured JSON Result ---")
        print(json.dumps(final_json, indent=2))
        
    except Exception as e:
        print(f"\n[DEBUG ERROR]: {e}")