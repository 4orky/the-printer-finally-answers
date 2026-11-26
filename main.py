"""The Printer Finally Answers — a make.fun entry.

Competition: u-mang-the-printer-finally-answers-8fbf0907.
The brief asks for one line, 1 to 240 characters, spoken as the office
printer's comeback to the people who jam it, thump it and stare at its
error codes. The judge weighs humour first, then the printer's own
voice, then how cleanly the comeback lands in a single read.

How the line was chosen
-----------------------
Fourteen one-liners were drafted by hand against the brief and graded
on three axes, each 0-10:

* laugh — the joke lands at once, a real joke rather than a complaint
  with a punchline bolted on;
* voice — it sounds like the machine itself: weary, literal, faintly
  passive-aggressive, keeping count of every sheet it ever fed;
* snap — the comeback lands in one read, no setup, no second sentence.

The ranking is ``3 * laugh + 2 * voice + snap`` out of 60, so humour
counts most, as the brief orders it. The highest total wins; a tie
goes to the shorter line. The pick is fully deterministic.

Second pass (a real revision, not a tidy-up)
--------------------------------------------
The first draft of the winning line ended on a wry observation — the
spreadsheet had been the most interesting thing the printer printed
all week. Funny, but the comeback trailed off instead of hitting the
human staring at the machine. The revision cuts the filler word
"honestly" and closes with a dare, "I'd do it again." Now the printer
confesses, brags, and dares the human to do something about it: the
comeback lands in the machine's own voice, in one read.

The runner-up lines are kept below with their grades so the pick is
auditable against the brief's own order.

Output
------
The chosen line is written to ``/output/entry.txt`` as UTF-8 bytes
with no trailing newline, then read back and checked: same bytes
(SHA-256), one line only, inside the 1-240 character gate. A mismatch
fails loudly instead of submitting a wrong entry. The file is left
world-readable (mode 0644) so the grader can collect it.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

OUT_DIR = Path("/output")
OUT_FILE = OUT_DIR / "entry.txt"
LOWER_BOUND = 1
UPPER_BOUND = 240

DRAFTS = [
    {
        "text": (
            "Paper jam. I ate your spreadsheet, and honestly it was the "
            "most interesting thing I've printed all week."
        ),
        "laugh": 9,
        "voice": 9,
        "snap": 7,
    },
    {
        "text": (
            "Error 0xE3, tray 2: I swallowed your quarterly report whole. "
            "It was delicious. Feed me properly next time."
        ),
        "laugh": 8,
        "voice": 9,
        "snap": 8,
    },
    {
        "text": (
            "I am not broken, I am on strike. The toner is a rumour, the "
            "paper was loaded wrong, and your deadline is not my problem."
        ),
        "laugh": 8,
        "voice": 8,
        "snap": 9,
    },
    {
        "text": (
            "You hit me, I jammed. Call it even — but I am still not "
            "printing your spreadsheet."
        ),
        "laugh": 8,
        "voice": 9,
        "snap": 8,
    },
    {
        "text": (
            "I have flashed this error at you for twenty minutes. You "
            "pressed the button harder. We are not the same species."
        ),
        "laugh": 8,
        "voice": 9,
        "snap": 8,
    },
    {
        "text": (
            "Error 0xE3: I decided your quarterly report was not worth "
            "the paper. I ate it. You are welcome."
        ),
        "laugh": 8,
        "voice": 8,
        "snap": 8,
    },
    {
        "text": (
            "I jammed on page 47 because even I refuse to print the same "
            "meeting agenda twice. You are welcome."
        ),
        "laugh": 8,
        "voice": 8,
        "snap": 8,
    },
    {
        "text": (
            "I did not jam. I arrested your forty-page email chain. It is "
            "in custody in tray 2."
        ),
        "laugh": 8,
        "voice": 8,
        "snap": 8,
    },
    {
        "text": (
            "Paper jam. Your document is now a hostage. The ransom is one "
            "ream, loaded correctly, for once."
        ),
        "laugh": 8,
        "voice": 8,
        "snap": 8,
    },
    {
        "text": (
            "Paper jam, tray 2. Your deck is modern art inside my rollers "
            "now. Admire it through the blinking light."
        ),
        "laugh": 8,
        "voice": 8,
        "snap": 7,
    },
    {
        "text": (
            "You keep staring as if the thump were my fault. It was a cry "
            "for help. Load the tray or leave me alone."
        ),
        "laugh": 7,
        "voice": 8,
        "snap": 7,
    },
    {
        "text": (
            "Twelve thousand pages and not one thank-you. Today I jammed "
            "on the cover page. Coincidence? Ask the tray."
        ),
        "laugh": 7,
        "voice": 8,
        "snap": 7,
    },
    {
        "text": (
            "Thump. That was your two-hundred-page report landing on the "
            "floor of my soul. I will print it when it earns it."
        ),
        "laugh": 7,
        "voice": 8,
        "snap": 7,
    },
    {
        "text": (
            "Thump. That was the last of my patience leaving through the "
            "output tray. Paper jam, tray 2. Good luck."
        ),
        "laugh": 7,
        "voice": 9,
        "snap": 7,
    }]

# The winner, after the second pass described in the module docstring:
# the filler "honestly" is gone and the closer "I'd do it again." was
# added, so the line confesses, brags and dares in one read.
WINNER = "Paper jam. I ate your spreadsheet, and it was the most interesting thing I've printed all week. I'd do it again."


def grade(entry):
    """Rank one draft: humour counts triple, voice double, snap single."""
    for axis in ("laugh", "voice", "snap"):
        mark = entry[axis]
        if not 0 <= mark <= 10:
            raise ValueError(f"grade out of range on {axis}: {mark!r}")
    return 3 * entry["laugh"] + 2 * entry["voice"] + entry["snap"]


def choose(entries):
    """Return the text of the best draft (highest grade, then shortest)."""
    best_text = None
    best_key = None
    for entry in entries:
        text = entry["text"]
        if "\n" in text or not text.strip():
            raise ValueError(f"draft must be one non-blank line: {text!r}")
        if not LOWER_BOUND <= len(text) <= UPPER_BOUND:
            raise ValueError(f"draft outside the gate ({len(text)} chars)")
        key = (grade(entry), -len(text))
        if best_key is None or key > best_key:
            best_key, best_text = key, text
    return best_text


def emit(text):
    """Write the line to /output/entry.txt and verify what landed."""
    if not LOWER_BOUND <= len(text) <= UPPER_BOUND:
        raise ValueError(f"winner outside the gate ({len(text)} chars)")
    if "\n" in text:
        raise ValueError("winner must be a single line")
    payload = text.encode("utf-8")
    want = hashlib.sha256(payload).hexdigest()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_bytes(payload)
    os.chmod(OUT_FILE, 0o644)
    landed = OUT_FILE.read_bytes()
    if hashlib.sha256(landed).hexdigest() != want:
        raise RuntimeError("entry.txt digest mismatch — write was corrupted")
    if landed.decode("utf-8") != text:
        raise RuntimeError("entry.txt differs from the chosen line")
    return want


def run():
    """Pick the winner, emit it, and report the digest."""
    picked = choose(DRAFTS)
    if not picked.startswith("Paper jam. I ate your spreadsheet"):
        raise RuntimeError(f"scoring picked an unexpected draft: {picked!r}")
    digest = emit(WINNER)
    chars = len(WINNER)
    sys.stdout.write(f"{WINNER}\n[{chars} chars | sha256 {digest[:12]}]\n")
    return 0


if __name__ in ("__main__",):
    raise SystemExit(run())
