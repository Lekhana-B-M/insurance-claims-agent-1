# Autonomous Insurance Claims Processing Agent

An AI-driven pipeline designed to automate the extraction, validation, and routing of First Notice of Loss (FNOL) insurance documents.

## Project Overview
This project leverages Google Gemini AI and Python to transform unstructured insurance PDF or text documents into structured JSON data. It automatically applies business logic to route claims for Fast-track processing, Specialist review, or Manual intervention based on predefined criteria.

## Architecture
The system follows a modular agent-based pattern:
1. Extraction Agent: Digitizes PDFs using PyMuPDF and extracts key insurance fields using Gemini 1.5/2.5 Flash.
2. Validation Agent: Performs a deterministic check to ensure all mandatory insurance fields are present and valid.
3. Routing Engine: Applies if/then business logic based on damage estimates, claim types, and fraud-related keywords.
4. Output Generator: Compiles the final standardized JSON report and saves it to the local file system.

## Folder Structure
insurance_claims_agent/
├── agents/             # Logic modules for AI, Validation, and Routing
├── config/             # Configuration files for business rules and field definitions
├── data/               # Input directory for FNOL documents (PDF/TXT)
├── outputs/            # Target directory for generated JSON results
├── tests/              # Unit tests for independent module verification
├── .env                # Environment variables for API security
├── main.py             # Application entry point and orchestrator
└── requirements.txt    # Project dependencies

## Installation and Setup
1. Create a Virtual Environment:
   python -m venv venv

2. Activate the Environment:
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate

3. Install Dependencies:
   pip install -r requirements.txt

4. Configure API Key:
   Create a .env file in the root directory and add:
   GEMINI_API_KEY=your_actual_key_here

## Usage
Place the insurance PDF in the data/ directory and execute:
python main.py

## Routing Rules
- Fast-track: Claims with estimated damage below $25,000 and zero missing fields.
- Specialist Queue: Claims where the claim type is identified as "Injury".
- Investigation Flag: Claims where fraud-related keywords are detected in the description.
- Manual Review: Claims with missing mandatory fields or those failing other automated criteria.

## Technologies Used
- Python 3.9+
- Google Gemini AI (Generative Language Model)
- PyMuPDF (fitz) for PDF parsing
- Python-dotenv for environment variable management