import os
import json
import logging
from agents.gemini_extractor import GeminiExtractor
from agents.field_validator import validate_fields
from agents.routing_engine import determine_route
from agents.preprocessor import preprocess_text
from agents.output_generator import save_and_display_results

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_agent(pdf_path):
    print("\n" + "="*50)
    print("🚀 STARTING AUTONOMOUS CLAIMS AGENT")
    print("="*50 + "\n")

    try:
        # 1. Initialize AI - THIS WAS MISSING OR MISPLACED
        agent = GeminiExtractor()

        # 2. Extract Text from PDF
        raw_text = agent.read_pdf(pdf_path)
        
        # 3. Preprocess Text (New Utility)
        clean_text = preprocess_text(raw_text)
        
        # 4. AI Extraction (Gemini)
        structured_data = agent.extract_structured_data(clean_text)
        
        # 5. Field Validation
        missing = validate_fields(structured_data)
        
        # 6. Routing Decision
        route, reason = determine_route(structured_data, missing)

        # 7. Final Result Assembly
        final_output = {
            "extractedFields": structured_data.get("extractedFields", {}),
            "missingFields": missing,
            "recommendedRoute": route,
            "reasoning": reason
        }

        # 8. Save and Display Results
        save_and_display_results(final_output)

    except Exception as e:
        logging.error(f"PIPELINE CRASHED: {e}")

if __name__ == "__main__":
    target_pdf = "data/sample_fnol.pdf"
    run_agent(target_pdf)