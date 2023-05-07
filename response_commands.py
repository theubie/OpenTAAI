import re
import json

name_changes = {}


def process_response(response):
    global name_changes

    # find all matches of <Rename:{old name}-{new name}> in the response
    matches = re.findall(r'<Rename:([\w\s]+)-([\w\s]+)>', response)

    # loop through each match and update the name_changes dictionary and response string
    changes = False
    for old_name, new_name in matches:
        changes = True
        name_changes[old_name] = new_name
        response = response.replace(f'<Rename:{old_name}-{new_name}>', '')
        print(f"Bot issued command to rename {old_name} to {new_name}")

    # Save the changes
    if changes:
        save_name_changes()

    return response


def replace_names(input_str):
    # loop through the keys and values in the name_changes dictionary
    for old_name, new_name in name_changes.items():
        # replace old_name with new_name in the input string
        input_str = input_str.replace(old_name, f"{old_name}({new_name})")
    return input_str


def load_name_changes():
    global name_changes
    try:
        with open('name_changes.json', 'r') as f:
            name_changes = json.load(f)
    except FileNotFoundError:
        pass


def save_name_changes():
    with open('name_changes.json', 'w') as f:
        json.dump(name_changes, f)


def module_setup():
    load_name_changes()
