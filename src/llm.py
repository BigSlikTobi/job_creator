import os
import json
from datetime import datetime
import google.generativeai as genai

def generate_job_payload(current_sim_time: datetime) -> dict:
    """
    Calls the Gemini model to generate a realistic natural language compute request and structured JSON.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    prompt = f"""
    You are an autonomous FinOps simulation engine representing diverse machine learning job requests from multiple teams around the world.
    The current simulated time is {current_sim_time.isoformat()}.
    
    Please generate a realistic machine learning compute request that sounds like it was written by an engineer.
    The request should specify:
    - Tier (e.g. Tier 1, Tier 2, Tier 3)
    - Priority (e.g. Critical, High, Normal, Low)
    - Resource requirements (e.g. GPU counts like 1x, 4x, 8x, or cluster sizes using A100, H100, TPU v4)
    - Duration in hours (between 1 and 720)
    - A deadline/SLA depending on the priority relative to the current time.
    - Region (e.g. us-east, eu-west, global)
    - Compliance (e.g. HIPAA, GDPR, None)
    - SLA percentage (e.g. 99.9%, 99.99%)
    - Minimum Quality (e.g. standard, high, premium)
    - Minimum Availability (e.g. low, medium, high)
    
    Output strictly as a valid JSON object matching this exact schema:
    {{
      "tier": "String",
      "priority": "String",
      "resources": {{"gpus": "Integer", "type": "String", "description": "String details"}},
      "duration_hours": "Integer",
      "sla_deadline": "ISO 8601 Timestamp",
      "region": "String",
      "compliance": "String",
      "sla": "String",
      "min_quality": "String",
      "min_availability": "String",
      "description": "String containing the realistic natural language request."
    }}
    
    Return ONLY JSON. Do not include markdown code block formatting like ```json or ```.
    """
    
    response = model.generate_content(prompt)
    
    # Clean the response just in case the model ignored instructions and included markdown
    text = response.text.strip()
    if text.startswith('```json'):
        text = text[7:]
    if text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    
    return json.loads(text.strip())
