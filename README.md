# AI Market Analysis Crew

## Introduction
This project uses the [CrewAI](https://www.crewai.com/) framework with [Groq](https://groq.com/) (llama-3.3-70b-versatile) to run a team of 4 AI agents that automatically generate a professional market analysis report on any topic.

## Agents
| Agent | Role |
|---|---|
| 🔍 Market Researcher | Gathers market size, trends, and investment data |
| 🕵️ Competitor Analyst | Analyzes top competitors' strengths and weaknesses |
| 📊 Business Strategist | Identifies opportunities, risks, and strategic moves |
| ✍️ Report Writer | Compiles everything into a structured markdown report |

## Prerequisites
- Python 3.10 or 3.11
- A free Groq API key from [console.groq.com](https://console.groq.com)

## Setup

**1. Create and activate a virtual environment**
```bash
**python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate**
```

**2. Install dependencies**
```bash
pip install crewai crewai-tools python-dotenv langchain_openai groq
```

**3. Configure environment variables**

Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

```dotenv
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here   # optional — enables live web search
```

**4. Run the script**
```bash
python main.py
```

## Output
The crew will run 4 agents sequentially and produce:
- A full report printed to the terminal
- A timestamped markdown file saved to the project folder (e.g. `market_report_20260307_225756.md`)

## Configuration
To change the research topic, edit the top of `main.py`:
```python
TOPIC = "Cybersecurity"
COMPETITORS = ["CrowdStrike", "Palo Alto Networks", "SentinelOne", "Microsoft", "Fortinet"]
```

## Web Search (Optional)
By default the crew runs in **offline mode**, using only the model's built-in knowledge.

To enable **live web search**, add a free `SERPER_API_KEY` to your `.env` file. Agents will then search the web for current data during each run.

## License
This project is released under the MIT License.
