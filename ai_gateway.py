"""Optional Gemini interpretation; no claims of real factory performance."""
import json
from pydantic import BaseModel, Field

class Interpretation(BaseModel):
    summary: str = Field(min_length=10)
    observations: list[str]
    limitations: list[str]
    checks_for_reviewer: list[str]

def generate_interpretation(rows: list[dict], api_key: str, model: str = 'gemini-2.5-flash') -> Interpretation:
    if not api_key:
        raise ValueError('GEMINI_API_KEY is missing')
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=json.dumps(rows),
        config=types.GenerateContentConfig(
            system_instruction=('Explain only the supplied synthetic factory comparisons. '
                                'Do not claim real-world emissions reductions, cost savings, '
                                'causation, or actual industrial measurements. '
                                'Include limitations and human verification checks.'),
            response_mime_type='application/json',
            response_schema=Interpretation,
            temperature=0,
        ),
    )
    if not response.text:
        raise ValueError('Empty Gemini response')
    return Interpretation.model_validate_json(response.text)
