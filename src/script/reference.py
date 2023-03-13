#!/usr/bin/env python3

import argparse
import re

from markdown import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader("src/template/"),
    autoescape=select_autoescape()
)


def replace_entities(lines):
    result = []
    for line in lines:
        line = re.sub(r'(\w)"', r"\1&rdquo;", line)
        line = re.sub(r'"(\w)', r"&ldquo;\1", line)
        line = re.sub(r"(\w)'", r"\1&rsquo;", line)
        line = re.sub(r"'(\w)", r"&lsquo;\1", line)
        result.append(line)
    return result


def split_sections(level, lines):
    match = "#" * level + " "
    sections = {}
    title = None
    for line in lines:
        if line.startswith(match):
            title = line.lstrip("#").strip()
            sections[title] = []
        else:
            if title:
                sections[title].append(line)
    return sections


def sections2html(sections):
    for title, lines in sections.items():
        lines = replace_entities(lines)
        text = "".join(lines)
        sections[title] = markdown(text)
    return sections


def read_frontmatter():
    path = "src/rule/frontmatter.md"
    with open(path) as f:
        lines = f.readlines()[2:]
        return sections2html(split_sections(2, lines))


def read_overview():
    path = "src/rule/overview.md"
    with open(path) as f:
        lines = f.readlines()[2:]
        sections = split_sections(2, lines)
    for title, text in sections.items():
        sections[title] = sections2html(split_sections(3, text))
    return sections


def title2id(title):
    return title.lower().replace(" ", "-").replace(",", "").replace("'", "")


def main():
    parser = argparse.ArgumentParser(description="COnvert B&D rules")
    parser.add_argument("output", type=str, help="The output HTML file")
    args = parser.parse_args()

    template = env.get_template("reference.html")
    output = template.render(
        version="v0",
        frontmatter=read_frontmatter(),
        overview=read_overview()
    )

    with open(args.output, "w") as f:
        f.write(output)


if __name__ == "__main__":
    main()
