import os
import time
import random
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables before importing src modules that might rely on them
load_dotenv()

from src.workload import SimulationClock, get_workload_rate
from src.llm import generate_job_payload
from src.webhook import send_payload

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("finops_generator")

def main():
    webhook_url = os.environ.get("WEBHOOK_URL", "http://127.0.0.1:8080/webhook")
    
    # Accelerated mode: 30 days (2,592,000s) in 1 hour (3600s) = scale factor 720
    # Configurable, defaulting to 720 (1 hour simulation) for fast observing
    scale_factor = float(os.environ.get("SCALE_FACTOR", 720.0))
    tick_interval_real_sec = float(os.environ.get("TICK_INTERVAL_SEC", 1.0))
    
    logger.info(f"Starting FinOps Input Generator. Target Webhook: {webhook_url}")
    logger.info(f"Scale Factor: {scale_factor}x. Tick Interval: {tick_interval_real_sec}s")
    
    if not os.environ.get("GEMINI_API_KEY"):
        logger.warning("GEMINI_API_KEY is not set in the environment or .env file. LLM generation may fail.")
    
    real_start = datetime.now()
    sim_start = datetime(2026, 1, 1, 0, 0, 0) # Start simulation from Jan 1st 2026
    clock = SimulationClock(real_start, sim_start, scale_factor)
    
    try:
        while True:
            current_real = datetime.now()
            current_sim = clock.get_simulated_time(current_real)
            
            # Rate is in jobs per simulated hour
            rate_per_hour = get_workload_rate(current_sim)
            
            # Convert rate per simulated hour to probability per simulated tick
            simulated_tick_duration = tick_interval_real_sec * scale_factor
            rate_per_tick = rate_per_hour * (simulated_tick_duration / 3600.0)
            
            # Simple probability of a job occurring exactly in this tick
            if random.random() < rate_per_tick:
                logger.info(f"[SIM TIME: {current_sim.isoformat()}] Triggering generation... (Rate: {rate_per_hour:.2f}/hr)")
                
                try:
                    payload = generate_job_payload(current_sim)
                    logger.info(f"Generated Payload:\n{json.dumps(payload, indent=2)}")
                    # Deliver webhook
                    success = send_payload(webhook_url, payload)
                    if not success:
                        logger.error("Payload delivery failed. Moving on to the next scheduled interval.")
                except Exception as e:
                    logger.error(f"Error generating payload using LLM: {str(e)}")
                    
            time.sleep(tick_interval_real_sec)
            
    except KeyboardInterrupt:
        logger.info("FinOps Input Generator shutting down.")

if __name__ == "__main__":
    main()
