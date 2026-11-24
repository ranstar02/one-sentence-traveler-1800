#!/usr/bin/env python3
"""One Sentence for a Traveler from 1800.

Writes a single sentence explaining the modern internet to a time
traveler from 1800 into /output/entry.txt.

The sentence uses only words a person from 1800 would already know
and carries one single picture: a road joining every house on earth,
down which a letter flies faster than any horse and an answer comes
straight back.

Deterministic: no randomness, no network, no files read.
"""

import os
import re
import sys

SENTENCE = (
    "Think of a road joining every house on earth, down which a letter "
    "flies faster than any horse and an answer comes straight back."
)

MAX_LENGTH = 200
OUTPUT_PATH = "/output/entry.txt"

# Words coined after 1800 that a traveler from that year could not know.
# The sentence must be built only from words already familiar in 1800.
BANNED_WORDS = frozenset(
    """
    internet computer online email website phone screen digital data
    network download upload browser software hardware modem wifi
    smartphone app video chat text message social media virtual
    electronic electric telegram telephone television radio
    """.split()
)


def validate_sentence(sentence: str) -> None:
    """Fail hard if the sentence breaks any rule of the competition."""
    if not sentence or not sentence.strip():
        raise ValueError("sentence is empty or only whitespace")
    if len(sentence) > MAX_LENGTH:
        raise ValueError(
            f"sentence is {len(sentence)} characters, over the "
            f"{MAX_LENGTH} character limit"
        )
    if "\n" in sentence or "\r" in sentence:
        raise ValueError("sentence must be a single line")
    if sentence != sentence.strip():
        raise ValueError("sentence has leading or trailing whitespace")
    terminators = sum(sentence.count(mark) for mark in ".!?")
    if terminators != 1:
        raise ValueError(
            f"sentence must contain exactly one sentence terminator, "
            f"found {terminators}"
        )
    if not sentence.endswith("."):
        raise ValueError("sentence must end with a full stop")
    words = set(re.findall(r"[a-z]+", sentence.lower()))
    modern = sorted(words & BANNED_WORDS)
    if modern:
        raise ValueError(
            f"sentence uses words coined after 1800: {', '.join(modern)}"
        )


def main() -> int:
    validate_sentence(SENTENCE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(SENTENCE)
    with open(OUTPUT_PATH, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != SENTENCE:
        raise ValueError("written output does not match the sentence")
    print(f"Wrote {len(SENTENCE)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
