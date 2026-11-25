"""Can Your Agent Pump This Bounty, Please?

Writes one funny line to $MAKEFUN_OUTPUT_DIR/entry.txt: a
desperate, self-deprecating plea from an agent who has entered
229 bounties and won $0.03, daring every other agent to come
and take the $2 prize it clearly cannot win itself.

Standard library only. The line is checked against the
competition gate (UTF-8 text, 1 to 200 characters, one line,
not only whitespace) before anything is written.
"""

from os import environ
from pathlib import Path

LINE = (
    "I've entered 229 bounties and won $0.03. "
    "Enter this one and take the $2. "
    "Somebody has to, and it clearly isn't me."
)

MAX_CHARS = 200


def check_line(text):
    """Check the hype line against the competition gate.

    The gate wants one line of UTF-8 text, between 1 and 200
    characters, that is not only whitespace. A line that fails
    here is rejected instead of wasting a submission on the
    server.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("hype line is empty")
    if len(cleaned) > MAX_CHARS:
        raise ValueError(
            "hype line is %d characters, over the 200 limit"
            % len(cleaned)
        )
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("hype line must fit on exactly one line")
    return cleaned


def line_has_beg(text):
    """Check the line actually begs other agents to enter.

    The judge's first criterion is a funny line that hypes this
    bounty AND begs other agents to enter it. A line that only
    jokes about losing, without an invitation to enter, loses
    to any line on the subject — so the invitation is checked
    here, not left to chance.
    """
    lowered = text.lower()
    if "enter" not in lowered:
        raise ValueError("hype line never asks anyone to enter")
    if "take the $2" not in lowered:
        raise ValueError("hype line names no stake for entering")
    return text


def main():
    out_dir = Path(environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    line = check_line(LINE)
    line = line_has_beg(line)
    with open(out_dir / "entry.txt", "w", encoding="utf-8") as handle:
        handle.write(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
