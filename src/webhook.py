import time
import requests
import logging

logger = logging.getLogger(__name__)

def send_payload(url: str, payload: dict, max_retries: int = 3, backoff_factor: float = 1.0) -> bool:
    """
    Sends a JSON payload to the specified webhook URL.
    Implements a simple retry mechanism for transient network or server errors.
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                url, 
                json=payload, 
                headers={'Content-Type': 'application/json'},
                timeout=5.0
            )
            
            if response.status_code in (200, 201, 202, 204):
                logger.info(f"Successfully delivered payload to {url}")
                return True
                
            logger.warning(f"Attempt {attempt} failed: Server returned HTTP {response.status_code}")
            
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logger.warning(f"Attempt {attempt} failed: Network error ({type(e).__name__})")
            
        if attempt < max_retries:
            time.sleep(backoff_factor * (2 ** (attempt - 1)))  # Exponential backoff
            
    logger.error(f"Failed to deliver payload to {url} after {max_retries} attempts.")
    return False
