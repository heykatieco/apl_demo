# APL FAQ Assistant (prototype)

A question-answering bot built on American Public Life's public FAQ page. Ask a question in plain English and it answers using only the FAQ, with citations to the entries it used.

> Independent portfolio project. Not affiliated with or endorsed by American Public Life.

## How it works

1. `fetch_faq.py` downloads the public FAQ page.
2. `parse_faq.py` extracts 47 question/answer pairs into structured JSON, tagged by audience (Individuals, Groups, Brokers, Providers). It keeps link URLs and checks record counts against the live page.
3. `bot_v1.py` places the full FAQ in the prompt (context stuffing) and answers questions with Claude Haiku, citing entries by number.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
TODO: Create requirements.txt, as she doesn't exist yet 

Create a `.env` file containing `ANTHROPIC_API_KEY=your-key`, then run:

```bash
python fetch_faq.py
python parse_faq.py
python bot_v1.py
```

TODO: Streamline this process above
## What I've learned so far

- **Cost:** about 11,500 input tokens and roughly $0.001 per question.
- **Guardrails:** the bot declines out-of-scope questions and resisted a prompt-injection attempt in testing.


## Next steps

- Retrieval: search the FAQ and send only the relevant entries instead of the whole thing.
- A Streamlit chat interface with an audience selector.
- Docker packaging.