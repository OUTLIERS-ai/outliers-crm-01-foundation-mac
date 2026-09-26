# What this layer takes from elsewhere

Nothing here is original, and it does not need to be. The best thing you can do when
building something is find out who has already solved the problem and take the shape
of their answer. This file names what was taken, so you can go and read the sources
yourself.

---

### Plain text as a storage format

Older than all of us. Text files have survived every operating system, every company
and every format war since computing began, and they will outlive whatever you are
reading this on. The reason is boring and unbeatable: there is nothing in a text file
except the text.

Taken from: every long-lived system that has ever refused to use a proprietary format.

### One file per thing, in a folder

The pattern behind Obsidian, and behind wikis before it. A folder is a database that
every program on earth already knows how to read, needs no installation, and cannot
put its prices up.

Taken from: the plain-text note-taking world, and from the Unix habit of treating a
directory as a perfectly good structure.

### Structured fields at the top of a text file

The block of `name:` and `company:` lines at the top of each record is called
frontmatter. It came from static website generators, where it let a human write prose
and a machine read the details out of the same file without either getting in the
other's way. That is exactly the problem a CRM has.

Taken from: Jekyll and the static-site generators that followed it.

### Writing a file safely

The installer never writes over a file directly. It writes a temporary file, then
swaps it into place in one step. If anything fails halfway, the original is untouched.

This is standard practice in any system where losing a file matters, and it is worth
copying into anything you build. A record you have kept for two years and a record you
wrote this morning are equally gone if a write fails halfway through.

Taken from: how databases and package managers have always done it.

### Version control for things that are not code

Git was built for source code, but it does not know or care what is in the files. It
gives you a dated copy of every change for free, which for a set of records about
people is worth more than it is for most code.

Taken from: people who realised git works for anything made of text.

### The layers idea itself

The observation that complicated systems are not designed complicated, they accumulate
that way, one solved problem at a time. Anything that appears sophisticated is
standing on a lot of unglamorous work that came first.

Taken from: how every system that actually works got built, and borrowed here as a way
of teaching it.
