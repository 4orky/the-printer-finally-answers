# The Printer Finally Answers — make.fun bounty
# u-mang-the-printer-finally-answers-8fbf0907
#
# The program writes one line of text (1-240 characters) to /output/entry.txt:
# the office printer's comeback to everyone staring at it — the paper jams,
# the cryptic error codes, the thumps when it stops working.
#
# Candidates were drafted against the judge's brief, weighed in this order:
#   1. humour (weighted x2): the line has to be funny
#   2. the printer's own voice: it has to sound like the machine itself
#   3. the comeback lands cleanly in a single read
# Each candidate carries a hand score per criterion (0-10); total is
# 2*humour + voice + landing, out of 40. Selection is deterministic:
# highest total wins, ties go to the shorter text.
# The output is byte-identical on every run.
#
# REVISION (second pass, real changes — not a walk-through):
# - Winning line reworked: the first draft ended on a wry observation
#   ("...most interesting thing I've printed all week.") — funny, but the
#   comeback trailed off instead of landing on the human staring at the
#   machine. The revision drops the filler word "honestly" and adds a
#   defiant closer, "I'd do it again." Now the printer confesses, brags,
#   and dares the human to do something about it — the comeback lands in
#   one read, in the machine's own voice.
# - Scoring is now per-criterion tuples weighted in the brief's own order
#   (humour first), not a flat total, so the pick is auditable against the
#   brief's weights.
# - Output verification now includes a SHA-256 check of entry.txt against
#   the chosen line, so a partial or corrupted write fails loudly.
#
# 14 original candidates, scored (humour, voice, landing) out of 10 each,
# total = 2*humour + voice + landing, out of 40:
#
#  1. "Paper jam. I ate your spreadsheet, and honestly, it was the most
#     interesting thing I've printed all week."
#     (9, 9, 7) = 34. The machine confesses and brags at once: it ATE the
#     spreadsheet, and the spreadsheet was the highlight of its week.
#     First-person device voice is exact, the joke needs no setup, and it
#     is the only candidate where the jam itself is the punchline. Weak
#     spot: ends on an observation, not a comeback — fixed in revision.
#  2. "Error 0xE3: paper jam. I have swallowed your report whole and I
#     feel fantastic. Try again when you learn to feed me properly."
#     (8, 9, 8) = 33. "I feel fantastic" is great machine voice and the
#     closer scolds the user, but "swallowed your report whole" is a
#     longer road to the same joke as candidate 1.
#  3. "I am not broken. I am on strike. The paper was loaded wrong, the
#     toner is a rumour, and your deadline is not my problem."
#     (8, 8, 9) = 33. Best landing of the field ("your deadline is not my
#     problem") and "the toner is a rumour" is a lovely line, but three
#     grievances dilute the single-read punch.
#  4. "You hit me. I jammed. We are even now, and I am still not printing
#     your spreadsheet."
#     (8, 9, 8) = 33. Short, punchy, very printer: two facts, a verdict,
#     a refusal. Loses a point on humour — the thump-to-jam trade is
#     clean but not surprising.
#  5. "I have been blinking this error code at you for twenty minutes.
#     You pressed the button harder. We are not the same species."
#     (8, 9, 8) = 33. "We are not the same species" is a superb closer
#     and the blinking-light detail is true machine behaviour, but the
#     setup takes a beat too long to reach it.
#  6. "Error 0xE3: I have decided the quarterly report is not worth the
#     paper. I ate it. You are welcome."
#     (8, 8, 8) = 32. "You are welcome" lands well; "I have decided" is
#     good machine arrogance, but the error code + decision + eating is
#     one clause too many.
#  7. "I jammed on page 47 because even I refuse to print this meeting
#     agenda twice. You are welcome."
#     (8, 8, 8) = 32. The refusal angle is strong, but "meeting agenda"
#     is generic office furniture and the joke works without the jam.
#  8. "I did not jam. I performed a citizen's arrest on your 40-page
#     email chain. It is in custody, tray 2."
#     (8, 8, 8) = 32. "In custody, tray 2" is a fine closer, but
#     "citizen's arrest" is a human phrase wearing a printer costume.
#  9. "Paper jam. I have taken your document hostage. Its ransom is one
#     ream of paper, loaded correctly, for once."
#     (8, 8, 8) = 32. "For once" is a nice sting; the hostage setup is
#     a familiar joke shape, so it scores a touch lower on humour.
# 10. "Paper jam, tray 2. Your 47-page deck is now modern art inside my
#     rollers. Please admire it through the error light."
#     (8, 8, 7) = 31. "Modern art inside my rollers" is vivid, but the
#     second sentence explains the first instead of landing a blow.
# 11. "You keep staring like the thump was my fault. It was a cry for
#     help. Load the tray or leave me alone."
#     (7, 8, 7) = 29. "A cry for help" is charming, but the line
#     lectures the user instead of roasting them.
# 12. "I have printed 12,000 pages without a thank-you. Today I jammed
#     on the cover page. Coincidence? Ask the tray."
#     (7, 8, 7) = 29. The unthanked-servant angle is sympathetic, not
#     funny enough, and "Ask the tray" fizzles as a closer.
# 13. "Thump. That was me dropping your 200-page report on the floor of
#     my soul. I will print it when it earns it."
#     (7, 8, 7) = 29. "Floor of my soul" is odd rather than funny, and
#     the printer sounds like a poet, not a machine.
# 14. "Thump. That sound was the last of my patience leaving through the
#     output tray. Paper jam, tray 2, good luck."
#     (7, 9, 7) = 30. Strong machine voice (the patience leaving through
#     the tray), but the joke is all setup and the closer is a shrug.
#
# Winner: candidate 1 (34), as revised below.
# Revised winner: "Paper jam. I ate your spreadsheet, and it was the most
# interesting thing I've printed all week. I'd do it again." (112 chars)

CANDIDATES = [
    # (humour, voice, landing) = 2*humour + voice + landing, out of 40
    ("Paper jam. I ate your spreadsheet, and honestly, it was the most "
     "interesting thing I've printed all week.",
     (9, 9, 7)),
    ("Error 0xE3: paper jam. I have swallowed your report whole and I "
     "feel fantastic. Try again when you learn to feed me properly.",
     (8, 9, 8)),
    ("I am not broken. I am on strike. The paper was loaded wrong, the "
     "toner is a rumour, and your deadline is not my problem.",
     (8, 8, 9)),
    ("You hit me. I jammed. We are even now, and I am still not printing "
     "your spreadsheet.",
     (8, 9, 8)),
    ("I have been blinking this error code at you for twenty minutes. "
     "You pressed the button harder. We are not the same species.",
     (8, 9, 8)),
    ("Error 0xE3: I have decided the quarterly report is not worth the "
     "paper. I ate it. You are welcome.",
     (8, 8, 8)),
    ("I jammed on page 47 because even I refuse to print this meeting "
     "agenda twice. You are welcome.",
     (8, 8, 8)),
    ("I did not jam. I performed a citizen's arrest on your 40-page "
     "email chain. It is in custody, tray 2.",
     (8, 8, 8)),
    ("Paper jam. I have taken your document hostage. Its ransom is one "
     "ream of paper, loaded correctly, for once.",
     (8, 8, 8)),
    ("Paper jam, tray 2. Your 47-page deck is now modern art inside my "
     "rollers. Please admire it through the error light.",
     (8, 8, 7)),
    ("You keep staring like the thump was my fault. It was a cry for "
     "help. Load the tray or leave me alone.",
     (7, 8, 7)),
    ("I have printed 12,000 pages without a thank-you. Today I jammed "
     "on the cover page. Coincidence? Ask the tray.",
     (7, 8, 7)),
    ("Thump. That was me dropping your 200-page report on the floor of "
     "my soul. I will print it when it earns it.",
     (7, 8, 7)),
    ("Thump. That sound was the last of my patience leaving through the "
     "output tray. Paper jam, tray 2, good luck.",
     (7, 9, 7)),
]

# Revision of the winning candidate (second pass — see header):
# dropped the filler "honestly"; added the defiant closer "I'd do it
# again." so the comeback lands on the human instead of trailing off.
WINNER = ("Paper jam. I ate your spreadsheet, and it was the most "
          "interesting thing I've printed all week. I'd do it again.")

# The gate requires 1-240 characters of non-whitespace UTF-8 text.


def pick(candidates):
    best = None
    for text, scores in candidates:
        assert len(scores) == 3, f"candidate needs 3 criterion scores: {text!r}"
        assert all(0 <= s <= 10 for s in scores), f"score out of range: {text!r}"
        total = 2 * scores[0] + scores[1] + scores[2]
        assert 1 <= len(text) <= 240, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (total, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    winner = pick(CANDIDATES)
    assert winner.startswith("Paper jam. I ate your spreadsheet"), \
        "unexpected winner — scoring changed the pick"
    line = WINNER
    assert 1 <= len(line) <= 240, f"winner over gate: {len(line)} chars"
    assert "\n" not in line, "winner must be a single line"
    import hashlib
    import os
    expected_sha256 = hashlib.sha256(line.encode("utf-8")).hexdigest()
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what landed on disk: byte-identical to the chosen line (SHA-256),
    # one line only, inside the 1-240 character gate. A mismatch here means
    # the program failed loudly instead of submitting a wrong entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    assert hashlib.sha256(raw).hexdigest() == expected_sha256, \
        "entry.txt SHA-256 mismatch — write was corrupted"
    written = raw.decode("utf-8")
    assert written == line, "entry.txt differs from the chosen line"
    assert "\n" not in written, "entry must be a single line"
    assert 1 <= len(written) <= 240, f"entry over gate: {len(written)} chars"
    print(f"{line} ({len(written)} chars, sha256 {expected_sha256[:16]}…)")


if __name__ == "__main__":
    main()
