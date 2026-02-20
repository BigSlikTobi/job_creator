import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import Timeout, ConnectionError
from src.webhook import send_payload

@patch('src.webhook.requests.post')
def test_send_payload_success(mock_post):
    mock_post.return_value.status_code = 200
    
    success = send_payload("http://localhost:8000/webhook", {"test": "data"})
    
    assert success is True
    assert mock_post.call_count == 1

@patch('src.webhook.requests.post')
def test_send_payload_retry_on_timeout(mock_post):
    # Fail twice with timeout, succeed on third
    mock_response_success = MagicMock()
    mock_response_success.status_code = 200
    
    mock_post.side_effect = [Timeout, Timeout, mock_response_success]
    
    success = send_payload("http://localhost:8000/webhook", {"test": "data"}, max_retries=3, backoff_factor=0)
    
    assert success is True
    assert mock_post.call_count == 3

@patch('src.webhook.requests.post')
def test_send_payload_exhaust_retries(mock_post):
    # Continually fail
    mock_response_fail = MagicMock()
    mock_response_fail.status_code = 500
    
    mock_post.return_value = mock_response_fail
    
    success = send_payload("http://localhost:8000/webhook", {"test": "data"}, max_retries=2, backoff_factor=0)
    
    assert success is False
    assert mock_post.call_count == 2
