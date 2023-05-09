import re
import json


def process_response(response, global_state):
    # find all matches of <Rename:{old name}-{new name}> in the response
    matches = re.findall(r'<Rename:([\w\s]+)-([\w\s]+)>', response)

    # loop through each match and update the name_changes dictionary and response string
    changes = False
    for old_name, new_name in matches:
        changes = True
        global_state.name_changes[old_name] = new_name
        response = response.replace(f'<Rename:{old_name}-{new_name}>', '')
        print(f"Bot issued command to rename {old_name} to {new_name}")

    # Save the changes
    if changes:
        save_name_changes(global_state)

    return response


def replace_names(input_str, global_state):
    # loop through the keys and values in the name_changes dictionary
    for old_name, new_name in global_state.name_changes.items():
        # replace old_name with new_name in the input string
        input_str = re.sub(r'(?i)\b{}\b'.format(re.escape(old_name.lower())),
                           f"{old_name}({new_name})", input_str)
    return input_str



def load_name_changes(global_state):
    try:
        with open('name_changes.json', 'r') as f:
            global_state.name_changes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or contains invalid JSON, create an empty dict
        global_state.name_changes = {}


def save_name_changes(global_state):
    with open('name_changes.json', 'w') as f:
        json.dump(global_state.name_changes, f)


def module_setup(global_state):
    load_name_changes(global_state)
