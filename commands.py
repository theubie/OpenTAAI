import os
import importlib.util
from helpers import write_to_file

# This should be the path to the directory containing the command files
COMMANDS_DIR = "commands"


def get_commands():
    commands = []
    for filename in os.listdir(COMMANDS_DIR):
        if filename.endswith(".py") and not filename.startswith("_"):
            module_name = os.path.splitext(filename)[0]
            module_path = os.path.join(COMMANDS_DIR, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'info'):
                info = module.info()
                commands.append(f"{module_name}: {info}")
            else:
                commands.append(f"{module_name}: No info available.")
    return sorted(commands)


def parse_opentaai_command(line, global_state):
    if global_state.args.verbose:
        print(f"command received: {line}")
    user, message = line.split(": ", 1)

    # Check if the user is allowed to run the command
    if user.strip().lower() not in [u.lower() for u in global_state.allowed_users]:
        print(f"User '{user}' is not allowed to run opentaai commands.")
        return True

    # Check if the message starts with "!opentaai"
    if message.startswith("!opentaai"):
        # Split the message into its individual components
        _, command, *args = message.split()

        if command == 'commands':
            # Save a list of available commands to output.txt
            output = "(From Ai Assistant) -"
            output = output + "\n ".join(get_commands())
            # global_state.twitch_queue.put(["send_message", output])
            print("Sending command list to Twitch.")

        else:
            # Dynamically import the module that corresponds to the command, if it exists
            module_path = os.path.join(COMMANDS_DIR, command + ".py")
            if os.path.isfile(module_path):
                spec = importlib.util.spec_from_file_location(command, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                try:
                    # Call the appropriate function within the module
                    function_name = "handle_command"
                    if hasattr(module, function_name):
                        function = getattr(module, function_name)
                        if global_state.args.verbose:
                            print(f"Attempting to handle {command}")
                        function(" ".join(args), global_state)
                except Exception as e:
                    print(e)

            else:
                print(f"Command '{command}' not found.")

        # Signal that the line should be deleted
        return True

    # If the message is not a command, do not delete it
    return True
