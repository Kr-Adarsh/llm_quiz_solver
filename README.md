---
title: Llm Quiz SolverV
emoji: 💻
colorFrom: pink
colorTo: green
sdk: docker
pinned: false
---

Server running at https://kradarsh-llm-quiz-solverv.hf.space/solve

# LLM Quiz Solver

An autonomous agent that solves multi-level data analysis quizzes using LangGraph state machine orchestration, Playwright for browser automation, and Google Gemini for reasoning.

## Features

- **LangGraph-powered agent**: State machine-based orchestration with Gemini 2.5 Flash
- **Playwright browser automation**: Renders JavaScript-heavy pages and captures dynamic content
- **Multi-tool execution**: Web scraping, file downloading, Python code execution, HTTP requests
- **Multi-level support**: Handles sequential quizzes with dynamic URL progression
- **Self-healing**: Auto-installs missing Python packages during analysis
- **Production-ready**: Docker deployment optimized for Hugging Face Spaces

## Architecture

```
User Request → FastAPI /solve Endpoint
                         ↓
              LangGraph Agent State Machine
                         ↓
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
    Web Scraper    Code Executor    HTTP Tools
   (Playwright)     (Python env)     (Download,
                                      Submit)
```

## Setup

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/llm_quiz_solver.git
cd llm_quiz_solver
pip install -r pyproject.toml
# or
pip install -e .
```

### 2. Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
EMAIL=your_email@example.com
SECRET=your_secret_code_word
```

### 3. Install Playwright

```bash
playwright install chromium
```

### 4. Run Locally

```bash
uvicorn main:app --host 0.0.0.0 --port 7860
```

## API Usage

### POST `/solve`

**Request:**
```json
{
  "email": "user@example.com",
  "secret": "your_secret_code_word",
  "url": "https://quiz.example.com/level/1"
}
```

**Response:**
```json
{
  "status": "accepted"
}
```

The agent runs asynchronously in the background.

### GET `/healthz`

Health check endpoint.

## Project Structure

```
├── agent.py                      # LangGraph state machine & orchestration
├── main.py                       # FastAPI server with /solve endpoint
├── pyproject.toml                # Project dependencies & metadata
├── Dockerfile                    # Container image with Playwright
├── tools/
│   ├── __init__.py
│   ├── web_scraper.py            # Playwright-based HTML rendering
│   ├── code_generate_and_run.py   # Python code execution
│   ├── download_file.py           # File downloader
│   ├── send_request.py            # HTTP POST tool
│   └── add_dependencies.py        # Dynamic package installer
└── README.md
```

## Deployment

### Local Docker

```bash
docker build -t quiz-solver .
docker run -p 7860:7860 \
  -e GOOGLE_API_KEY="AIza..." \
  -e EMAIL="user@example.com" \
  -e SECRET="secret_key" \
  quiz-solver
```

### Hugging Face Spaces

1. Create a new Space (Docker SDK)
2. Upload all files
3. Set Secrets in Space Settings:
   - `GOOGLE_API_KEY`
   - `EMAIL`
   - `SECRET`
4. Build and deploy

Endpoint: `https://<username>-<space-name>.hf.space/solve`

## How It Works

1. **Parse**: Playwright renders the quiz page and extracts content
2. **Reason**: Gemini 2.5 Flash analyzes the task and plans tool usage
3. **Execute**: Agent calls tools (scrape, download, run Python)
4. **Submit**: Sends answer to quiz endpoint
5. **Loop**: If a next URL exists, repeats from step 1

## Tools Available

| Tool | Purpose |
|------|---------|
| `web_scraper` | Fetch and render HTML using Playwright |
| `code_generate_and_run` | Write and execute Python analysis |
| `download_file` | Download CSV, JSON, PDF, images |
| `send_request` | POST answers to quiz endpoint |
| `add_dependencies` | Install missing Python packages |

## License

MIT License

## Author

KrAdarsh - TDS Project 2
