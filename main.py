from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "")
os.environ["SERPER_API_KEY"] = os.environ.get("SERPER_API_KEY", "")

# ─────────────────────────────────────────
# CONFIGURATION — change this to any topic
# ─────────────────────────────────────────

TOPIC = "AI & Technology"
COMPETITORS = ["OpenAI", "Google DeepMind", "Anthropic", "Meta AI", "Microsoft AI"]
OUTPUT_FILE = f"market_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

# ─────────────────────────────────────────
# TOOLS (optional — requires SERPER_API_KEY)
# Get a free key at: https://serper.dev
# Add SERPER_API_KEY to your .env file
# ─────────────────────────────────────────

tools = []
if os.environ.get("SERPER_API_KEY"):
    search_tool = SerperDevTool()
    tools = [search_tool]
    print("✅ Web search enabled (live data mode)")
else:
    print("ℹ️  No SERPER_API_KEY found — running in offline mode (model knowledge only)")
    print("   Get a free key at https://serper.dev and add SERPER_API_KEY to your .env\n")

# ─────────────────────────────────────────
# AGENTS
# ─────────────────────────────────────────

researcher = Agent(
    role=f'{TOPIC} Market Researcher',
    goal=f'Gather comprehensive data on the {TOPIC} market landscape',
    verbose=True,
    llm="groq/llama-3.3-70b-versatile",
    tools=tools,
    backstory=(
        f'You are an expert market researcher with 15 years of experience analyzing '
        f'the {TOPIC} sector. You have a talent for identifying emerging trends, '
        f'key players, and market opportunities before they become mainstream.'
    )
)

competitor_analyst = Agent(
    role='Competitor Analyst',
    goal=f'Analyze top competitors in the {TOPIC} space and identify their strengths and weaknesses',
    verbose=True,
    llm="groq/llama-3.3-70b-versatile",
    tools=tools,
    backstory=(
        f'You are a sharp competitive intelligence analyst who specializes in the {TOPIC} industry. '
        f'You have deep knowledge of companies like {", ".join(COMPETITORS)}, '
        f'and can break down their strategies, products, and market positioning.'
    )
)

strategist = Agent(
    role='Business Strategist',
    goal=f'Develop actionable business strategies and opportunities based on market research and competitor analysis',
    verbose=True,
    llm="groq/llama-3.3-70b-versatile",
    backstory=(
        f'You are a seasoned business strategist who turns market data into clear, '
        f'actionable recommendations. You specialize in helping companies find their '
        f'competitive edge in the fast-moving {TOPIC} industry.'
    )
)

report_writer = Agent(
    role='Market Report Writer',
    goal='Compile all findings into a professional, well-structured market analysis report',
    verbose=True,
    llm="groq/llama-3.3-70b-versatile",
    backstory=(
        'You are a professional business writer who specializes in creating clear, '
        'compelling market reports for executives and investors. Your reports are '
        'known for being insightful, concise, and easy to act upon.'
    )
)

# ─────────────────────────────────────────
# TASKS
# ─────────────────────────────────────────

research_task = Task(
    description=(
        f'Research the current state of the {TOPIC} market. Cover: '
        f'1) Market size and growth rate, '
        f'2) Key trends shaping the industry in 2024-2025, '
        f'3) Major investment areas and funding activity, '
        f'4) Emerging technologies to watch.'
    ),
    expected_output=(
        f'A detailed research summary covering market size, top trends, '
        f'investment activity, and emerging technologies in {TOPIC}.'
    ),
    agent=researcher
)

competitor_task = Task(
    description=(
        f'Analyze the top competitors in the {TOPIC} space. For each company cover: '
        f'1) Core products and services, '
        f'2) Key strengths, '
        f'3) Key weaknesses or gaps, '
        f'4) Recent strategic moves. '
        f'Focus on: {", ".join(COMPETITORS)}.'
    ),
    expected_output=(
        f'A competitor analysis covering {", ".join(COMPETITORS)} with their '
        f'strengths, weaknesses, products, and recent strategic moves.'
    ),
    agent=competitor_analyst
)

strategy_task = Task(
    description=(
        f'Based on the market research and competitor analysis, identify: '
        f'1) Top 3 market opportunities in {TOPIC}, '
        f'2) Potential threats and risks to watch, '
        f'3) Recommended strategic moves for a new or growing company in {TOPIC}, '
        f'4) Key success factors in this market.'
    ),
    expected_output=(
        f'A strategic recommendations report with market opportunities, risks, '
        f'and actionable advice for competing in the {TOPIC} space.'
    ),
    agent=strategist
)

report_task = Task(
    description=(
        f'Compile all previous research, competitor analysis, and strategic recommendations '
        f'into a single, professional Market Analysis Report on {TOPIC}. '
        f'Structure it with: '
        f'1) Executive Summary, '
        f'2) Market Overview, '
        f'3) Competitor Landscape, '
        f'4) Opportunities & Risks, '
        f'5) Strategic Recommendations, '
        f'6) Conclusion. '
        f'Use markdown formatting with clear headings and bullet points.'
    ),
    expected_output=(
        f'A complete, well-structured Market Analysis Report on {TOPIC}, '
        f'ready to present to executives or investors. Formatted in markdown.'
    ),
    agent=report_writer
)

# ─────────────────────────────────────────
# CREW
# ─────────────────────────────────────────

market_crew = Crew(
    agents=[researcher, competitor_analyst, strategist, report_writer],
    tasks=[research_task, competitor_task, strategy_task, report_task],
    process=Process.sequential,
    verbose=True
)

# ─────────────────────────────────────────
# RUN
# ─────────────────────────────────────────

print("\n" + "="*60)
print(f"   {TOPIC.upper()} MARKET ANALYSIS - STARTING")
print("="*60 + "\n")

result = market_crew.kickoff()

# ─────────────────────────────────────────
# OUTPUT — print and save to file
# ─────────────────────────────────────────

report_content = str(result)

print("\n" + "="*60)
print("   FINAL MARKET ANALYSIS REPORT")
print("="*60)
print(report_content)

# Save to markdown file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(f"# {TOPIC} Market Analysis Report\n")
    f.write(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}*\n\n")
    f.write(report_content)

print(f"\n✅ Report saved to: {OUTPUT_FILE}")