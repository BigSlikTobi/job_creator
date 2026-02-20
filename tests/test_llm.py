import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.llm import generate_job_payload

@patch('src.llm.genai.GenerativeModel')
def test_generate_job_payload(mock_model_class):
    # Mock the LLM response
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    
    # Mock generating content
    mock_response = MagicMock()
    mock_response.text = '{"tier": "Tier 1", "priority": "Critical", "description": "Need GPUs."}'
    mock_model_instance.generate_content.return_value = mock_response
    
    sim_time = datetime(2026, 2, 20, 12, 0, 0)
    payload = generate_job_payload(sim_time)
    
    # Verify model initialization used the correct model name
    mock_model_class.assert_called_with('gemini-2.5-flash-lite')
    
    # Verify the mocked JSON was parsed correctly
    assert payload["tier"] == "Tier 1"
    assert "description" in payload
