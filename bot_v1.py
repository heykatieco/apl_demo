import json
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

FAQ_FILE = Path("data/faq.json")
MODEL = "claude-haiku-5-5"

# Prices per million tokens 
INPUT_PRICE = 0.10
OUTPUT_PRICE = 0.50

INSTRUCTIONS = """You are a customer service assistant for American Public Life (APL), \
a supplemental insurance company. Answer questions using ONLY the FAQ entries provided below.

Rules:
- If the FAQ does not answer the question, say so plainly and suggest contacting APL directly. Never guess.
- Cite the FAQ entries you used by number, like [3] or [3][12].
- If the answer differs by audience (individual, group, broker, provider), say which audience it applies to.
- Never ask for or repeat personal information such as policy numbers, Social Security numbers, or health details.
- Keep answers short and practical: a few sentences, or a short list of steps."""


def load_faq(path=FAQ_FILE):
    return json.loads(path.read_text(encoding="utf-8"))


def format_faq(records):
    """Turn the FAQ records into one numbered block of text for the prompt."""
    entries = []
    for number, record in enumerate(records, start=1):
        entries.append(
            f"[{number}] Audience: {record['audience']}\n"
            f"Q: {record['question']}\n"
            f"A: {record['answer']}\n"
            f"Source: {record['url']}"
        )
    return "\n\n".join(entries)


def ask(client, system_prompt, question):
    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=system_prompt,
        messages=[{"role": "user", "content": question}],
    )
    answer = "".join(block.text for block in response.content if block.type == "text")
    return answer, response.usage


def main():
    load_dotenv()
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY is missing. Check your .env file.")

    records = load_faq()
    system_prompt = f"{INSTRUCTIONS}\n\n<faq>\n{format_faq(records)}\n</faq>"
    client = Anthropic()

    print(f"Loaded {len(records)} FAQ entries. Ask a question (or type 'quit').\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"quit", "exit", "q"}:
            break
        if not question:
            continue

        answer, usage = ask(client, system_prompt, question)
        cost = (usage.input_tokens * INPUT_PRICE + usage.output_tokens * OUTPUT_PRICE) / 1_000_000
        print(f"\nBot: {answer}\n")
        print(f"   [tokens in: {usage.input_tokens:,} | out: {usage.output_tokens:,} | cost: ${cost:.4f}]\n")


if __name__ == "__main__":
    main()