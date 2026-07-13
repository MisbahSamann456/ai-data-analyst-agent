# 📊 AI Data Analyst Agent


🔗 **Live Demo:** [https://ai-data-analyst-agent-fbdyrsnd63j4u3vyqrbshq.streamlit.app/](https://ai-data-analyst-agent-fbdyrsnd63j4u3vyqrbshq.streamlit.app/)

An AI-powered agent that lets you upload a CSV or Excel file and ask questions about your data in plain English...

An AI-powered agent that lets you upload a CSV or Excel file and ask questions about your data in plain English. It converts your natural language question into a SQL query, runs it against the full dataset using DuckDB, and returns a clear, human-readable answer.

## How it works

1. **Upload** — A CSV/Excel file is parsed with pandas and loaded into an in-memory DuckDB table.
2. **Ask** — You type a question like "What is the total sales by country?"
3. **Reason** — The LLM (Groq's LLaMA 3.3 70B) interprets your question and writes the corresponding SQL query.
4. **Execute** — DuckDB runs that SQL against the entire dataset (not just a sample).
5. **Explain** — The LLM converts the raw SQL result into a clear natural-language answer.

This reason → act → observe loop is what makes it an *agent* rather than a simple chatbot — it doesn't just talk, it writes and executes real code to get accurate answers from the full dataset.

## Tech Stack

- **Streamlit** — web interface
- **Groq (LLaMA 3.3 70B)** — LLM for query generation and reasoning
- **DuckDB** — in-memory SQL engine for fast, accurate analysis over the full dataset
- **Agno** — agent framework tying the LLM and tools together
- **Pandas** — file parsing and preprocessing

## Setup

```bash
pip install -r requirements.txt
streamlit run ai_data_analyst.py
```

Enter your free Groq API key (get one at [console.groq.com](https://console.groq.com)) in the sidebar, upload a CSV/Excel file, and start asking questions.

## Example queries

- "What is the total sales by country?"
- "Top 5 customers by sales"
- "Which product line has the highest revenue?"

## Known limitations

- Very broad or multi-part questions can exceed the LLM's context window — future improvement would be chunking schema/data sent per request.
- Currently single-turn; no conversation memory across questions yet.

## Notes

Inspired by open-source data-analyst-agent patterns, rebuilt with Groq's free LLaMA models instead of OpenAI to keep it cost-free for prototyping.

