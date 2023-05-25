# args.py
from helpers import save_settings
def info():
    return "Change the value of an argument."


def handle_command(args, global_state):
    # Split the args into argument name and new value
    arg_name, new_value = args.split(maxsplit=1)

    # Check if the argument exists
    if hasattr(global_state.args, arg_name):
        # Get the current argument value
        current_value = getattr(global_state.args, arg_name)

        # Determine the type of the current argument value
        arg_type = type(current_value)

        # Try to convert the new value to the same type as the current argument value
        try:
            converted_value = arg_type(new_value)
        except ValueError:
            print(f"Invalid value for argument '{arg_name}'. Type mismatch.")
            return

        # Update the value of the argument
        setattr(global_state.args, arg_name, converted_value)
        if global_state.args.verbose:
            print(f"Argument '{arg_name}' set to '{converted_value}'.")
        if global_state.args.settings:
            save_settings(global_state.args, global_state.args.settings)

    else:
        print(f"Argument '{arg_name}' not found.")

