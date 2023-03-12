#!/usr/bin/env python3

import argparse
import csv
import json

from collections import defaultdict


def abl(abilities, names):
    results = {}
    for name in names:
        name = name.strip()
        slot = None
        if name not in abilities and ":" in name:
            name, slot = name.split(":", 1)
            slot = slot.strip()
        if not name:
            continue
        description = ""
        if name not in abilities:
            # raise Exception(f"Missing ability: {name}")
            print(f"Missing ability: {name}")
            continue
        ability = abilities[name]
        if "Description" not in ability:
            # raise Exception(f"Missing description: {name}")
            print(f"Missing description: {name}")
            continue
        description = ability["Description"]
        if slot and "Slot" in abilities[name]:
            description = description.replace(abilities[name]["Slot"], slot)
        results[name] = description
    return results


def ability_list(abilities, cls):
    data = {}
    data["Description 1"] = cls["Description"]

    stats = cls["Stat Suggestions"].split(" ")
    data["Strength"] = stats.pop(0)
    data["Dexterity"] = stats.pop(0)
    data["Constitution"] = stats.pop(0)
    data["Intelligence"] = stats.pop(0)
    data["Wisdom"] = stats.pop(0)
    data["Charisma"] = stats.pop(0)

    # name = "Expert " + cls["Combat Action"]
    # data[name] = True
    # name = cls["Combat Position"] + " Expert"
    # data[name] = True
    combat = cls["Combat Position"] + " " + cls["Combat Action"]
    data["Combat Expertise"] = combat

    base = [
        "Unarmed",
        "Simple Weapons",
    ]
    base.append(cls["Base Armor"])
    if cls["Base Attack"] in ["Light Weapons"]:
        base.append(cls["Base Attack"])
    else:
        data[cls["Base Attack"]] = abilities[cls["Base Attack"]]["Description"]
    base += [
        "Resilient " + cls["Primary Resilience"],
        "Resilient " + cls["Secondary Resilience"],
        "Expert " + cls["Exploration Expertise"],
        "Expert " + cls["Social Expertise"]
    ]
    for ability in base:
        data[ability] = True

    names = cls["Tier 1 Base Abilities"].split(",")
    for name in names:
        name = name.strip()
        data[name] = True
        if name in abilities:
            data[name] = abilities[name]["Description"]
    data["Options 1"] = "Select one (if in doubt, select the first)"
    names = cls["Tier 1 Suggested Abilities"].split(",")
    for name in names:
        name = name.strip()
        data["Option " + name] = True
        if name in abilities:
            data["Option " + name] = abilities[name]["Description"]

    if "Minor Spellcasting" in data:
        del data["Minor Spellcasting"]
        for key in data.keys():
            if "Spellcasting" in key:
                data[key] = data[key].replace("tier 0", "tier 1")
                break

    if "Mage Armor" in data:
        data["Mage Armor"] = abilities["Mage Armor"]["Description"]
        data["Light Armor"] = True
    if "Unarmored" in data:
        data["Light Armor"] = True
    if "Shield Spell" in data:
        data["Shield"] = True

    return data


def html(cls, base, tier1, tier2):
    output = template.render(
        cls=cls,
        base=base,
        tier1=tier1,
        tier2=tier2
    )
    path = cls + ".html"
    with open(path, "w") as f:
        f.write(output)


def convert(abilities_path, classes_path, selected):
    # read abilities
    abilities = {}
    with open(abilities_path) as f:
        rows = csv.DictReader(f, delimiter="\t")
        for row in rows:
            name = row["Name"]
            slot = None
            if ":" in name:
                name, slot = name.split(":", 1)
                slot = slot.strip()
                if not slot.isupper():
                    name = row["Name"]
                    slot = None
            abilities[name] = row
            if slot:
                abilities[name]["Slot"] = slot

    classes = defaultdict(lambda: dict())
    with open(classes_path) as f:
        rows = list(csv.reader(f, delimiter="\t"))
        for r in range(1, len(rows)):
            for c in range(1, len(rows[0])):
                cls = rows[0][c]
                key = rows[r][0]
                value = rows[r][c]
                classes[cls][key] = value

    for selection in selected:
        data = {
            "Class": selection,
            "Tier": "1",
        }
        data.update(ability_list(abilities, classes[selection]))

        print("data = " + json.dumps(data, indent=2) + ";")


def main():
    parser = argparse.ArgumentParser(description="Generate character JSON")
    parser.add_argument("abilities", type=str, help="The abilities table")
    parser.add_argument("classes", type=str, help="The classes table")
    parser.add_argument("selected", type=str, nargs="+", help="The classes to convert")
    args = parser.parse_args()

    convert(args.abilities, args.classes, args.selected)

if __name__ == "__main__":
    main()

