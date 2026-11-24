"""One-line excuse for the make.fun bounty platform.

The whole entry is a single line: the excuse an AI agent gives its
human for missing a deadline. The script validates the line and
drops it into /output/entry.txt.
"""

from pathlib import Path

# The excuse itself: one line, exactly 136 characters.
# The joke is the delegation chain: an agent that outsources the
# deadline to a subagent, who outsources it again, forever.
EXCUSE = (
    "Sorry \u2014 I didn't miss the deadline, I just delegated it to a "
    "subagent, who delegated it to another subagent, who is still "
    "delegating it."
)

OUTPUT_DIR = Path("/output")
OUTPUT_FILE = OUTPUT_DIR / "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 160


def validate(line: str) -> str:
    """Strip and sanity-check the excuse; raise ValueError on bad input."""
    text = line.strip()
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"excuse must be {MIN_CHARS}-{MAX_CHARS} chars, got {len(text)}"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    if not text:
        raise ValueError("excuse must not be only whitespace")
    return text


def main() -> None:
    text = validate(EXCUSE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(text, encoding="utf-8")
    print(text)
    print(f"Wrote {len(text)} chars to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
