# FinOps Input Generator

A standalone, lightweight CLI utility designed to continuously generate and
deliver a structured stream of simulated machine learning compute jobs via
webhooks.

It autonomously models a global company's time-series workload (including daily
traffic peaks, weekend lulls, and random priority bursts). Natural language
payloads are dynamically generated using Google's Gemini 2.5 Flash Lite API,
extracted into structured JSON, and reliably delivered to a target `.env`
configured webhook.

## Project Structure

- `generator.py` - The main CLI application scheduling loop.
- `src/workload.py` - Mathematical engine managing time acceleration and
  expected workload frequencies.
- `src/llm.py` - Gemini LLM integration for generating realistic payload text
  and extracting JSON schema.
- `src/webhook.py` - Robust HTTP sender utilizing an exponential backoff retry
  system.
- `src/mock_receiver.py` - A lightweight FastAPI local webhook receiver for
  testing.
- `tests/` - Pytest unit test suites for all core components.
- `finops-generator.service` - Systemd service configuration for Raspberry Pi
  autonomy.

## Setup

1. **Create and Activate a Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables** Create a `.env` file in the root
   directory and add your Gemini API Key and desired webhook URL:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   WEBHOOK_URL="http://127.0.0.1:8080/webhook"
   SCALE_FACTOR=720.0
   TICK_INTERVAL_SEC=1.0
   ```
   _(By default, a scale factor of 720 compresses 30 days of traffic into
   roughly 1 hour of real-time running)._

## Running Locally

To simulate and test the generator locally:

1. **Start the Mock Webhook Receiver:** In your first terminal pane (with the
   `.venv` activated):
   ```bash
   python src/mock_receiver.py
   ```
   _This will start a FastAPI server listening on port 8080._

2. **Start the Generator:** In a second terminal pane (with the `.venv`
   activated):
   ```bash
   python generator.py
   ```
   _You will immediately see payloads generated and delivered to the mock
   receiver pane!_

## Running Unit Tests

The components are built using a Test-Driven Development (TDD) approach. Execute
the test suite using `pytest`:

```bash
PYTHONPATH=. pytest -v
```

## Raspberry Pi Deployment

To run this indefinitely and autonomously on a Raspberry Pi:

1. Ensure the project is cloned/placed in `/home/pi/creatorjob_`.
2. Ensure your `.venv` is built and dependencies are installed.
3. Review the `finops-generator.service` file and update paths if necessary.
4. Setup the systemd service:
   ```bash
   sudo cp finops-generator.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable finops-generator.service
   sudo systemctl start finops-generator.service
   ```
5. Check logs via: `journalctl -u finops-generator.service -f`
