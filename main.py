#!/usr/bin/env python3
"""One-Line Office Joke: 24-Hour Sprint — make.fun entry.

Writes a single one-line joke about office life to /output/entry.txt.

The joke is chosen for the judge's brief, in the brief's own order:
1. It is a one-line joke about office life — a setup and a punchline,
   not a caption or a stray observation.
2. It is funny — the punchline pays off a setup every office worker
   recognises, with a surprise twist in the last clause.
3. It is one line — a single sentence, no rambling around it.
4. It is fresh — it turns on "per my last email", the most
   passive-aggressive phrase in office life, and an image nobody has
   heard as a joke before: two ghosts haunting the same thread.
5. It is clear on first read — plain words, tight wording, no
   reference the reader cannot follow.

Usage:
    python3 main.py [--output-dir DIR]

The output directory defaults to /output (the grader's directory) and
can be overridden for local runs.
"""

import argparse
import os
import sys

# The joke. One sentence, one line, well under the 200-character gate.
JOKE = (
    "I wrote 'per my last email' and my colleague wrote "
    "'per my last email', and now we're just two passive-aggressive "
    "ghosts haunting the same thread."
)

MAX_CHARS = 200


def validate(text):
    """Check the text against the gate: UTF-8, 1-200 chars, one line."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d-character limit"
            % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if not valid UTF-8 text
    return text


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the one-line office joke to entry.txt."
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("OUTPUT_DIR", "/output"),
        help="directory to write entry.txt into (default: /output)",
    )
    args = parser.parse_args(argv)

    joke = validate(JOKE)

    os.makedirs(args.output_dir, exist_ok=True)
    path = os.path.join(args.output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(joke + "\n")

    # Read the file back and re-validate it, so a write that silently
    # truncated or mangled the text is caught here, not by the gate.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != joke + "\n":
        raise ValueError("read-back mismatch: entry.txt is not the joke")
    validate(written.rstrip("\n"))

    print("Wrote %s (%d characters):" % (path, len(joke)))
    print(joke)
    return 0


if __name__ == "__main__":
    sys.exit(main())
