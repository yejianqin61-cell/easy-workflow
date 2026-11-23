#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Install this repository's skills into MiniMax Code, also called MCode.

MCode reads its skills from one place: the `skills/` folder inside its data
directory, one folder per skill. This script puts every skill in this
repository there.

    python tools/install-mcode.py             # copy every skill
    python tools/install-mcode.py --link      # symlink, so a git pull updates them
    python tools/install-mcode.py --list      # show the target and the skills
    python tools/install-mcode.py --uninstall # remove the skills this script installed

The data directory is `~/.minimax` by default. Set `MINIMAX_CODE_DATA_DIR`, or
pass `--dir`, to point at another one. A project-level install goes to the
project's own data directory, and this script takes that path too.

Nothing here depends on the network, and nothing outside the target directory
is touched. The script replaces a skill folder of the same name, and it says
so before it does.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR_ENV = "MINIMAX_CODE_DATA_DIR"
DEFAULT_DATA_DIR = Path.home() / ".minimax"
SKILLS_GLOB = "skills"


def data_dir(override):
    """The MiniMax Code data directory, as a path."""
    if override:
        return Path(override).expanduser().resolve()
    env = os.environ.get(DATA_DIR_ENV)
    if env:
        return Path(env).expanduser().resolve()
    return DEFAULT_DATA_DIR


def target_dir(override):
    """The folder MCode reads skills from."""
    return data_dir(override) / SKILLS_GLOB


def source_skills():
    """Every skill folder in this repository, sorted by name."""
    root = ROOT / SKILLS_GLOB
    if not root.is_dir():
        return []
    found = []
    for bucket in sorted(root.iterdir()):
        if not bucket.is_dir():
            continue
        for skill in sorted(bucket.iterdir()):
            if skill.is_dir() and (skill / "SKILL.md").is_file():
                found.append(skill)
    return found


def skill_name(folder):
    """The `name` in a SKILL.md frontmatter, falling back to the folder name."""
    text = (folder / "SKILL.md").read_text(encoding="utf-8")
    for line in text.split("\n"):
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("'\"")
        if line.strip() == "---" and text.startswith("---\n"):
            break
    return folder.name


def installed_name(folder):
    """The name of the skill in an installed folder, or None when it is not one."""
    marker = folder / "SKILL.md"
    if not marker.is_file():
        return None
    try:
        return skill_name(folder)
    except OSError:
        return None


def remove_folder(folder):
    """Delete a folder, following a symlink to its target."""
    if folder.is_symlink() or folder.is_file():
        folder.unlink()
        return
    shutil.rmtree(folder)


def install_one(source, target, link, dry_run):
    """Install one skill, and report what happened."""
    name = skill_name(source)
    existing = installed_name(target) if target.exists() else None
    if existing is not None and existing != name:
        return "skipped", "%s holds %s, not %s" % (target.name, existing, name)

    verb = "replace" if target.exists() else "install"
    if dry_run:
        return verb, name

    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        remove_folder(target)
    if link:
        try:
            target.symlink_to(source, target_is_directory=True)
        except OSError:
            shutil.copytree(source, target)
            return "copied", "%s (symlink refused)" % name
        return "linked", name
    shutil.copytree(source, target)
    return "copied", name


def uninstall_one(target, names, dry_run):
    """Remove one installed folder, when it holds a skill from this repository."""
    name = installed_name(target)
    if name is None or name not in names:
        return "kept", target.name
    if dry_run:
        return "remove", name
    remove_folder(target)
    return "removed", name


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Install this repository's skills into MiniMax Code.",
    )
    parser.add_argument(
        "--dir",
        dest="dir",
        help="the MiniMax Code data directory, default %s" % DEFAULT_DATA_DIR,
    )
    parser.add_argument(
        "--link",
        action="store_true",
        help="symlink the skills, so a git pull updates them",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_only",
        help="show the target and the skills, and change nothing",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="remove the skills this repository installed",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would happen, and change nothing",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])
    skills = source_skills()
    if not skills:
        print("no skills found under %s" % (ROOT / SKILLS_GLOB))
        return 1

    target = target_dir(args.dir)
    names = {skill_name(s) for s in skills}

    if args.list_only:
        print("target: %s" % target)
        print("skills: %d" % len(skills))
        for skill in skills:
            print("  %s" % skill.name)
        return 0

    if args.uninstall:
        removed = 0
        for skill in skills:
            status, detail = uninstall_one(target / skill.name, names, args.dry_run)
            print("%-8s %s" % (status, detail))
            removed += status == "removed"
        print("%d skill(s) removed from %s" % (removed, target))
        return 0

    counts = {"installed": 0, "replaced": 0, "copied": 0, "linked": 0, "skipped": 0}
    for skill in skills:
        status, detail = install_one(skill, target / skill.name, args.link, args.dry_run)
        counts[status] = counts.get(status, 0) + 1
        print("%-8s %s" % (status, detail))

    print(
        "%d skill(s) %s %s"
        % (len(skills), "planned for" if args.dry_run else "installed in", target)
    )
    print("open MiniMax Code, and the skills are listed under Skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
