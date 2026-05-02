from conv import convert
import json

with open("discoveries.json", "r", encoding="utf-8") as f:
    current_data = json.load(f)

more = True

while more:
    name = input("Name the element: ")
    emoji = input("Emoji: ")

    new_element = {"name": name, "emoji": emoji, "is_first_discovery": False}
    current_data.append(new_element)

    with open("discoveries.json", mode="w", encoding="utf-8") as f:
        json.dump(current_data, f, indent=4)

    more = input("Another? Y:n ").lower()

    if more == "Y".lower():
        continue
    else:
        break




convert()

