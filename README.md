# MindMate Harmony — Final (Jac 0.18 + Python Gemini Microservice)

This project is tailored for the Generative AI + Jaseci Hackathon and uses Jac 0.18 as the main backend graph/agent logic.
Because Jac 0.18 does not include byLLM, the project uses a Python microservice to call Gemini (LLM) and then invokes Jac walkers to log data and store suggestions.

## Project layout
jaseci/
  nodes/
  edges/
  agents/
  walkers/
frontend/
backend/
README.md

## Quick start (recommended)
1. Install Python 3.12+ (or 3.10/3.11 if your jac version requires it).
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure `jac` CLI (Jaseci 0.18) is installed and available in PATH.
4. (Optional) Set GEMINI_API_KEY and GEMINI_URL in environment or .env to enable real Gemini calls.
5. Start the Python proxy:
   ```bash
   python backend/proxy.py
   ```
6. Open `frontend/index.html` with Live Server and interact with the UI.
7. For direct Jac testing, run walkers from the command line, e.g.:
   ```bash
   echo '{"mood":"sad","note":"had a rough day"}' | jac run jaseci/walkers/main.jac --walker support_agent
   ```

## How it maps to hackathon requirements
- **Jac as main backend**: All graph-related logic, nodes/edges and agents (analyze_mood, store_suggestion, trend_insights) live in `jaseci/`.
- **Multi-agent system**: mood_analyzer (Jac), support_generator (Python+LLM for generation, then stored by Jac), trend_agent (Jac).
- **OSP**: Nodes and edges defined in `jaseci/nodes` and `jaseci/edges`.
- **LLM (Gemini)**: Called by Python microservice; results are fed into Jac walkers so the graph stores suggestions.
- **End-to-end demo**: Frontend -> Python proxy -> Gemini -> Jac walkers -> frontend.

## Notes & Next steps
- The proxy currently uses a placeholder Gemini endpoint. Replace GEMINI_URL with the actual Gemini inference endpoint for your account and set GEMINI_API_KEY.
- If you'd like, I can adapt the proxy to a concrete Gemini REST payload (I will need the exact target API and auth flow you plan to use), or change the design so Jac calls Python instead.
