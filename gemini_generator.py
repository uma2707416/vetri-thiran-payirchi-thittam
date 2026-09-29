import os
from dotenv import load_dotenv

load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        self.client = None
        if self.api_key:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)

    def _prompt(self, document_type, parties, terms, dates):
        return f"""
You are LegalEase, an AI-assisted legal document drafting system.

Create a professional, structured draft for the following document.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE / DATES:
{dates}

TERMS AND CONDITIONS:
{terms}

Requirements:
1. Use clear professional legal drafting language.
2. Include a title, parties/definitions where appropriate, numbered sections,
   obligations, payment/term/termination/confidentiality clauses when relevant,
   and signature blocks.
3. Do not invent names, dates, addresses, money amounts, laws, jurisdictions,
   or facts that were not supplied.
4. If an important fact is missing, use a clearly marked placeholder such as
   [JURISDICTION] instead of guessing.
5. Preserve the user's supplied terms.
6. Return plain text only. Do not use Markdown code fences.
7. End with a short "Important Notice" stating that the output is an AI-generated
   draft and should be reviewed by a qualified legal professional before use.
"""

    def generate_document(self, document_type, parties, terms, dates):
        if not self.client:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Add it to the .env file."
            )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=self._prompt(document_type, parties, terms, dates),
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()
