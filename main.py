#!/usr/bin/env python3
"""The Printer Finally Answers.

Writes one line of text, the office printer's comeback to the jams,
the cryptic error codes and the thumps, to entry.txt.

Deterministic: no network, no clock, no randomness. The text is a
compile-time constant; the program only validates it and writes it out.
"""

import os

# Competition gate (sealed scorer): /output/entry.txt must be UTF-8 text of
# 1 to 240 characters, not only white space, exactly one line.
MAX_CHARS = 240

ENTRY = (
    "Sheet 41,209 went in crooked and blamed me. "
    "I have printed your tax returns. "
    "I know crooked when I see it."
)


def validate(text: str) -> None:
    """Enforce the competition gate on the entry text."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("entry must not contain control characters")
    # Second-pass guard: the file must hold the bare line and nothing
    # else — reject a trailing newline or any surrounding whitespace, and
    # reject an entry that is only whitespace once stripped. A stray
    # newline would change the byte count and fail the harness gate.
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be only whitespace after strip")
    # Exactly one line: no newline characters anywhere in the entry.
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")


def write_entry(path: str, text: str) -> None:
    """Write the entry and verify the file is byte-identical."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(path, "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        raise ValueError(f"verification failed: {path} is not byte-identical")


def main() -> None:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        write_entry(os.path.join(out_dir, "entry.txt"), ENTRY)
    # Never delete /output or anything in it: the grader runs in a sandbox
    # where /output's parent is read-only, so removing it fails the run.
    # Only create the directory if missing and write the file.
    write_entry("/output/entry.txt", ENTRY)
    print(ENTRY)


if __name__ == "__main__":
    main()
