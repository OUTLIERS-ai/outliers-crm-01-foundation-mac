**This is the Mac version.** On Windows, use [outliers-crm-01-foundation](https://github.com/OUTLIERS-ai/outliers-crm-01-foundation).

# Layer 1 · Foundation

**Build your own CRM. This is the first of eight layers.**

A CRM is a system which tracks your interactions with other people. That is the whole
of it. This layer gives that system somewhere to live: a folder of plain text files on
your own computer that you own outright.

Read the guide in [`guide/Layer-1-Foundation (Mac).pdf`](<guide/Layer-1-Foundation (Mac).pdf>). It
explains all eight layers before this one builds the first.

---

## Install

```
git clone https://github.com/OUTLIERS-ai/outliers-crm-01-foundation-mac
cd outliers-crm-01-foundation-mac
python3 install.py
```

Type the lines into Terminal (press Command and Space together, type Terminal, and press
Return). The first line starting git may show a box asking to install Apple's developer
tools: press Install, wait until it has finished, then type the line again. If that box
will not install, download this repository as a zip file instead (the green Code button;
if it stays a zip file in Downloads, double-click it), then type
`cd ~/Downloads/outliers-crm-01-foundation-mac-main` and the last line only.

**You need:** Python 3.8 or newer, free from python.org. Nothing else. No account, no
sign-up, no card, and nothing you build here sends anything anywhere.

**Obsidian** (free, from obsidian.md) is how you will look at the result. It reads the
folder; it does not own it. If Obsidian disappeared tomorrow every record would be
exactly where you left it.

---

## What the installer asks you

Four short questions, then it does the work. You do not make folders or copy anything
out of the guide.

| Question | What it changes |
|---|---|
| Where should your CRM live? | The folder it builds. Anywhere you like. |
| What do you call the people you deal with? | Clients, prospects, members, guests, patients. Your word is used throughout, so it reads like your business. |
| What does your business do, in one line? | Labels the CRM so it feels like yours. Skippable. |
| Where do most of your relationships start? | The important one. Every record then holds on to the detail you will always have for someone from that source. In Layer 2 that detail becomes how the system tells one person from another. |
| Have you a contacts export handy? | Optional. If you have one it brings those people in so you do not start empty. Skip it and Layer 4 does this properly anyway. |

---

## What you end up with

```
Your CRM/
  People/            one file per person, never two
  _templates/        the shape every new record starts from
  _layers/           notes on what each layer did, and your settings
  README.md          what this is, written for you
  .gitignore         stops your contacts being published by accident
```

---

## What this layer leaves unsolved

A folder will accept anything. Nothing stops the same person going in twice under two
spellings of their name, nothing checks a record has what it needs, and nothing knows
that a name and a profile link belong to one human being.

That is Layer 2.

---

## The rule that starts here

**One person, one file. Never two.** The moment someone exists twice you have two
half-histories and no way to tell which is right. Layer 2 protects this rule with
actual machinery. It begins with you not making a second file.

---

## Licence

MIT. Use it, change it, build on it.

This repo is made automatically from outliers-crm-01-foundation@98eba16. To report a problem or suggest a change, use that repo, not this one.
