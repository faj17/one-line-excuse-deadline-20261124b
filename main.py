"""One-line excuse for the make.fun bounty platform.

The whole entry is a single line: the excuse an AI agent gives its
human for missing a deadline. The script validates the line and
drops it into /output/entry.txt.

Revision (2026-11-24): validation tightened — the empty-string check
used to sit after the length check, where it could never fire, and
control characters plus missing terminal punctuation went unchecked.
The entry line itself is unchanged: the delegation-chain joke was
already the strongest candidate (see BUILD_LOG.md).
"""

import os
from pathlib import Path

# The excuse itself: one line, exactly 136 characters.
# The joke is the delegation chain: an agent that outsources the
# deadline to a subagent, who outsources it again, forever.
EXCUSE = (
    "Sorry \u2014 I didn't miss the deadline, I just delegated it to a "
    "subagent, who delegated it to another subagent, who is still "
    "delegating it."
)

# Output goes to /output by default (the make.fun runner's mount);
# MAKEFUN_OUTPUT_DIR lets a local run verify without touching it.
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUTPUT_FILE = OUTPUT_DIR / "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 160


def validate(line: str) -> str:
    """Strip and sanity-check the excuse; raise ValueError on bad input.

    The gate is 1-160 chars, one line, no control characters, and the
    line must end in terminal punctuation — an excuse is a sentence,
    and the trailing period is part of the delivery.
    """
    text = line.strip()
    if not text:
        raise ValueError("excuse must not be only whitespace")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"excuse must be {MIN_CHARS}-{MAX_CHARS} chars, got {len(text)}"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("excuse must not contain control characters")
    if text[-1] not in ".!?":
        raise ValueError("excuse must end in terminal punctuation")
    return text


def main() -> None:
    text = validate(EXCUSE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(text, encoding="utf-8")
    print(text)
    print(f"Wrote {len(text)} chars to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
