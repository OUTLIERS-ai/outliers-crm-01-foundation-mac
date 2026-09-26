"""
Outliers CRM · Layer 1 · Foundation

Builds your CRM. You do not have to make folders, write templates, or copy anything
out of a PDF. Run this once, answer a few questions, and it puts the whole thing
together for you.

    python install.py

It will ask where you want your CRM to live, what you call the people you deal
with, and what your business is. Then it builds it, and tells you what each part
is for.

Nothing here costs money and nothing leaves your computer. No account, no sign-up,
no internet connection required.

Needs: Python 3.8 or newer. Nothing else.
"""

import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

# The key a member presses. A Mac keyboard's key is Return; Windows keeps Enter, exactly as before
# (Mac build plan V3, wave s1: the Session 7 ruling on the words installers print).
KEY = "Return" if sys.platform == "darwin" else "Enter"

# ---------------------------------------------------------------- small helpers

# No colour codes anywhere. Plenty of terminals print them as literal gibberish
# ("[1m" all over the screen), and a member's first minute with this must not look
# broken. Plain text works everywhere, which is the whole point of the exercise.
BOLD = DIM = OFF = ""


def say(msg=""):
    print(msg, flush=True)


def ask(question, default=None, helptext=None):
    """One plain question. Enter accepts the default."""
    say()
    say(BOLD + question + OFF)
    if helptext:
        say(DIM + "  " + helptext + OFF)
    prompt = "  > " if default is None else "  [%s] > " % default
    try:
        answer = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        say("\nStopped. Nothing was changed.")
        sys.exit(1)
    return answer or (default or "")


def ask_yes(question, default=True):
    d = "Y/n" if default else "y/N"
    a = ask(question, default=d).strip().lower()
    if a in ("y/n", "y/n".upper(), "y", "yes"):
        return True if a != "y/n" else default
    if a in ("n", "no"):
        return False
    return default


def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_-]+", "-", text) or "person"


def write(path, content):
    """Write a file without ever damaging one that already exists.

    Writes to a temporary file first, then swaps it into place in a single step.
    If anything goes wrong halfway through, the original is untouched. This is a
    habit worth keeping: the notes in here are the record, and there is no copy.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def vault_over(path):
    """The Obsidian vault this path would land inside, if there is one.

    Obsidian marks a vault with a `.obsidian` folder at its root. The mistake this
    catches is a member pointing this installer at the second brain they already
    built, which is the obvious thing to do when that is the vault sitting open in
    front of them. It costs them twice: every later layer reads every file under
    the folder given here, and a second brain holds things that have no business
    being anywhere near a commercial contact record.

    Returns None when the folder is already an Outliers CRM, because re-running the
    installer over your own CRM is not a mistake.
    """
    path = Path(path).expanduser()
    for parent in [path] + list(path.parents):
        if (parent / ".obsidian").is_dir():
            if (parent / "_layers" / "config.json").exists():
                return None
            return parent
    return None


def choose_home(default_home):
    """Ask where the CRM goes, and refuse to be quiet about a vault-inside-a-vault."""
    while True:
        home = ask("Where should your CRM live?",
                   default=default_home,
                   helptext="A new folder on your own machine. If it does not exist, it "
                            "gets created. Press " + KEY + " to take the one in brackets.")
        clash = vault_over(home)
        if clash is None:
            return home

        say()
        say("  Hold on. That is inside a vault Obsidian already opens:")
        say("    %s" % clash)
        say()
        say("  Your CRM should sit alongside that one, not inside it. Every layer")
        say("  after this reads every file under the folder you name here, and the")
        say("  vault you have pointed at holds things that are not contact records.")
        if ask_yes("Use %s instead? (recommended)" % default_home, default=True):
            return default_home
        if ask_yes("Then carry on anyway, into that vault?", default=False):
            return home
        say(DIM + "  Fair enough. Give me another folder." + OFF)


# ---------------------------------------------------------------- the interview

def interview():
    say()
    say(BOLD + "=" * 66 + OFF)
    say(BOLD + "  OUTLIERS CRM   LAYER 1   FOUNDATION" + OFF)
    say(BOLD + "=" * 66 + OFF)
    say()
    say("  This builds your CRM. It asks four questions, then does the work.")
    say("  Everything stays on this computer. Nothing is sent anywhere.")
    say()
    say(DIM + "  Press %s to accept anything in [brackets]." % KEY + OFF)

    default_home = str(Path.home() / "CRM")
    say()
    say("  Your CRM is its own vault, separate from your second brain.")
    say("  Two folders side by side, both yours. Not one inside the other.")
    home = choose_home(default_home)

    people_word = ask("What do you call the people you deal with?",
                      default="contacts",
                      helptext="clients, prospects, members, guests, patients, contacts. "
                               "Whatever you actually say out loud.")

    business = ask("What does your business do, in one line?",
                   default="",
                   helptext="Used to label your CRM so it feels like yours. Skip it if you like.")

    platform = ask("Where do most of your relationships start?",
                   default="LinkedIn",
                   helptext="LinkedIn, email, referrals, events, WhatsApp, in person. "
                            "This decides which detail every record keeps hold of.")

    return {
        "home": Path(home).expanduser(),
        "people_word": people_word.strip().lower() or "contacts",
        "business": business.strip(),
        "platform": platform.strip() or "LinkedIn",
    }


# ------------------------------------------------------------------ what we build

IDENTIFIER_FOR = {
    "linkedin": ("linkedin-url", "https://www.linkedin.com/in/their-profile"),
    "email":    ("email", "them@theircompany.com"),
    "whatsapp": ("phone", "+44 7000 000000"),
    "phone":    ("phone", "+44 7000 000000"),
}


def identifier_for(platform):
    p = platform.lower()
    for key, val in IDENTIFIER_FOR.items():
        if key in p:
            return val
    return ("email", "them@theircompany.com")


def person_template(cfg):
    field, example = identifier_for(cfg["platform"])
    return """---
name:
{field}:
company:
met-through:
date: {today}
type: person
tags: [crm]
---

## Who they are

## What we have talked about

## What happens next
""".format(field=field, today=date.today().isoformat())


def example_person(cfg):
    """One made-up person, so the folder is never empty and the shape is obvious."""
    field, example = identifier_for(cfg["platform"])
    return """---
name: Rowan Ashdown
{field}:
company: Ashdown & Co
met-through: {platform}
date: {today}
type: person
tags: [crm, example]
---

## Who they are

Invented, so you can see the shape of a record before you have any of your own.
The identifier line is deliberately blank: a made-up person should not claim a real one.
Delete this whenever you like.

## What we have talked about

Nothing. Rowan is not real.

## What happens next

Layer 2 gives this file an identity, so the system can tell one person from
another even when the names look the same.
""".format(field=field, platform=cfg["platform"], today=date.today().isoformat())


def vault_readme(cfg):
    w = cfg["people_word"]
    field, _ = identifier_for(cfg["platform"])
    line = ("\n> " + cfg["business"] + "\n") if cfg["business"] else "\n"
    return """# Your CRM
{line}
A CRM is a system that tracks your interactions with other people. That is the
whole of it. Everything you add from here on is in service of that one sentence.

## This is a vault of its own

Separate from your second brain, and it stays separate. Two vaults side by side:
one holds what you know, this one holds who you know. Obsidian opens as many as
you like and switches between them. Keeping them apart costs you nothing and
saves you from a CRM that has quietly swallowed your notes, or the other way
round.

## What is in here

| Folder | What it holds |
|---|---|
| `People/` | One file per person. One file, never two. |
| `_templates/` | The shape a new record starts from. |
| `_layers/` | Notes on what each layer of this system does. Grows as you build. |

## The one rule that matters right now

**One person, one file.** If someone ends up in here twice, you now have two
half-histories and no way to tell which is right. Everything in Layer 2 exists to
protect this rule, but it starts with you not making a second file.

## Why plain files

Your {w} live in text files on your own machine. You can read them without this
app, without any app, and in ten years. Nothing you write here is locked inside
software that can put its prices up or shut down.

## The detail every record keeps

Most of your relationships start on **{platform}**, so every record has a
`{field}` field. It looks like a small thing. In Layer 2 it becomes the way the
system knows one person from another, which is the hardest problem in the whole
build.

## What you do now

Nothing, honestly. There is no data in here yet, so anything asked of you today
would be typing for the sake of it. Read the Layer 1 guide if you have not, then
Layer 2 makes this folder into something that can hold a real business.
""".format(line=line, w=w, platform=cfg["platform"], field=field)


def layer_note():
    return """# Layer 1 · Foundation

**What it built.** A folder on your own machine, one file per person, and a
template so every record starts the same shape.

**What it does.** It gives your relationship knowledge somewhere to live that you
own outright, readable by you today and by software later.

**What it leaves for Layer 2.** A folder will accept anything. Nothing yet stops
the same person being in here twice under two spellings, and nothing yet checks
that a record has what it needs. Rules are Layer 2.
"""


def gitignore():
    return """# Your CRM is yours. This stops it being published by accident.
People/
Companies/
_private/
*.tmp
.obsidian/workspace*
"""


# ------------------------------------------------------------------------- build

def build(cfg):
    home = cfg["home"]
    say()
    say(BOLD + "Building your CRM at %s" % home + OFF)
    say()

    made = []

    def note(path, what):
        made.append((path, what))
        say("  built  %-38s %s" % (str(Path(path).relative_to(home)), DIM + what + OFF))

    (home / "People").mkdir(parents=True, exist_ok=True)
    say("  built  %-38s %s" % ("People/", DIM + "one file per person, never two" + OFF))

    p = home / "_templates" / "Person.md"
    write(p, person_template(cfg))
    note(p, "the shape every new record starts from")

    p = home / "People" / "Rowan Ashdown.md"
    if not p.exists():
        write(p, example_person(cfg))
        note(p, "an invented person, so the folder is not empty")

    p = home / "README.md"
    write(p, vault_readme(cfg))
    note(p, "what this is and how it works")

    p = home / "_layers" / "Layer 1 - Foundation.md"
    write(p, layer_note())
    note(p, "what this layer did, for when you forget")

    p = home / ".gitignore"
    write(p, gitignore())
    note(p, "stops your contacts being published by accident")

    # A pointer in the member's home folder, so every later layer can find this CRM
    # wherever they chose to put it. Without it, anyone who declined the default
    # location gets told at the next layer that they have not done this one.
    try:
        write(Path.home() / ".outliers-crm", str(home) + os.linesep)
        say("  built  %-38s %s" % ("~/.outliers-crm", DIM + "so the next layer can find this folder" + OFF))
    except Exception:
        pass

    write(home / "_layers" / "config.json", json.dumps({
        "people_word": cfg["people_word"],
        "platform": cfg["platform"],
        "identifier": identifier_for(cfg["platform"])[0],
        "business": cfg["business"],
        "layer": 1,
        "built": date.today().isoformat(),
    }, indent=2) + "\n")

    return made


def offer_import(cfg, home):
    """Optional: bring in an existing contacts export, so the CRM is not empty.

    Entirely optional and skipping it costs nothing. Layer 4 does capture properly.
    This exists so that anyone who happens to have an export to hand can have a
    populated system in their first sitting rather than an empty folder.
    """
    say()
    say(BOLD + "Do you have a contacts export handy?" + OFF)
    say(DIM + "  A .csv from LinkedIn, your email, or your phone. Optional, and easy" + OFF)
    say(DIM + "  to skip: capture is handled properly later. Press %s to skip." % KEY + OFF)
    raw = ask("Path to the file, or %s to skip" % KEY, default="")
    if not raw.strip():
        say(DIM + "  Skipped. Your CRM starts empty, which is fine." + OFF)
        return 0

    path = Path(raw.strip().strip('"').strip("'")).expanduser()
    if not path.exists():
        say("  Cannot find that file. Skipping; you can run this again later.")
        return 0

    import csv
    field, _ = identifier_for(cfg["platform"])
    made = skipped = 0
    try:
        with open(path, encoding="utf-8-sig", errors="replace", newline="") as fh:
            # exports often carry a few preamble lines before the real header
            sample = fh.read(8192)
            fh.seek(0)
            start = 0
            for i, line in enumerate(sample.splitlines()[:12]):
                if line.lower().count(",") >= 2 and any(
                        k in line.lower() for k in ("first name", "name", "email")):
                    start = i
                    break
            for _ in range(start):
                fh.readline()
            for row in csv.DictReader(fh):
                low = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
                name = (" ".join(x for x in (low.get("first name"), low.get("last name")) if x)
                        or low.get("name") or low.get("full name") or "").strip()
                if not name:
                    skipped += 1
                    continue
                ident = (low.get("url") or low.get("profile url") or low.get("email address")
                         or low.get("email") or low.get("phone") or "")
                safe = re.sub(r'[<>:"/\\|?*]', "", name).strip()[:80]
                target = home / "People" / (safe + ".md")
                if not safe or target.exists():
                    skipped += 1
                    continue
                write(target, """---
name: {name}
{field}: {ident}
company: {company}
met-through: {platform}
date: {today}
type: person
tags: [crm, imported]
---

## Who they are

{position}

## What we have talked about

## What happens next
""".format(name=name, field=field, ident=ident, company=low.get("company", ""),
           platform=cfg["platform"], today=date.today().isoformat(),
           position=low.get("position", "") or low.get("title", "")))
                made += 1
    except Exception as e:
        say("  Could not read that file (%s). Skipping; nothing was harmed." % e)
        return 0

    say()
    say("  Brought in %d people. Skipped %d (no name, or already there)." % (made, skipped))
    if made:
        say(DIM + "  Some of those records will be duplicates of each other, and some" + OFF)
        say(DIM + "  will be half-empty. That is not a mistake, it is what every contact" + OFF)
        say(DIM + "  list actually looks like. Layer 2 is what sorts it out." + OFF)
    return made


def git(home, *args, quiet=False):
    """Run one git command in the CRM folder and return its exit code.

    `quiet` throws the output away. This is done by Python, not by the shell: the
    shell's way (`>nul` on Windows) makes a file called `nul` on a Mac. If git is
    not installed, the answer is a failure, the same as git refusing.
    """
    out = subprocess.DEVNULL if quiet else None
    try:
        return subprocess.run(["git", "-C", str(home)] + list(args),
                              stdout=out, stderr=out).returncode
    except OSError:
        return 1


def offer_git(home):
    say()
    if not ask_yes("Keep a dated history of every change? (recommended)", default=True):
        say(DIM + "  Skipped. You can turn it on later." + OFF)
        return
    if git(home, "rev-parse", "--git-dir", quiet=True) == 0:
        say("  History is already on.")
        return
    if git(home, "init", "-q") != 0:
        say(DIM + "  Could not turn it on. Git may not be installed. This is optional; carry on." + OFF)
        return
    git(home, "add", "-A", quiet=True)
    git(home, "-c", "user.email=you@example.com", "-c", "user.name=You",
        "commit", "-q", "-m", "Layer 1: foundation", quiet=True)
    say("  History is on. You can now see what any record said on any past date.")


def finish(cfg):
    home, w = cfg["home"], cfg["people_word"]
    say()
    say(BOLD + "=" * 66 + OFF)
    say(BOLD + "  Done. Your CRM exists." + OFF)
    say(BOLD + "=" * 66 + OFF)
    say()
    say("  It is at:  %s" % home)
    say()
    say("  What you have:")
    say("    - A folder you own, on your own machine, that no company can close.")
    say("    - One file per person, which is the rule the whole system rests on.")
    say("    - A template so every record starts the same shape.")
    say()
    say("  To look at it: open Obsidian, choose 'Open folder as vault', and pick")
    say("  that folder. Obsidian is free and it only reads the folder. If you")
    say("  stopped using it tomorrow, your %s would be completely unaffected." % w)
    say()
    say("  This is your second vault. Your second brain is the other one, and it")
    say("  stays exactly as it was. Obsidian holds as many vaults as you like and")
    say("  switches between them, so keeping the two apart costs you nothing.")
    say()
    say(BOLD + "  What to do now: nothing." + OFF)
    say("  There is no data in here yet, so any task today would be typing for the")
    say("  sake of it, and typing is the thing that kills CRMs. Layer 2 gives this")
    say("  folder rules, and Layer 4 fills it without you.")
    say()


def main():
    cfg = interview()
    say()
    say("  Building at:      %s" % cfg["home"])
    say("  You call them:    %s" % cfg["people_word"])
    say("  Relationships from: %s" % cfg["platform"])
    if not ask_yes("Go ahead?", default=True):
        say("\nStopped. Nothing was changed.")
        return 1
    build(cfg)
    offer_import(cfg, cfg["home"])
    offer_git(cfg["home"])
    finish(cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
