from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

import os
import importlib
import pkgutil
from registry import commands


def load_commands():
    """Dynamically import all modules from the `commands` directory by filepath.

    This avoids requiring `cli` to be an importable package and works when
    running `python app.py` from the `cli/` folder.
    """
    commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
    if not os.path.isdir(commands_dir):
        return

    for filename in os.listdir(commands_dir):
        if not filename.endswith('.py') or filename == '__init__.py':
            continue
        name = filename[:-3]
        path = os.path.join(commands_dir, filename)
        try:
            spec = importlib.util.spec_from_file_location(f'cli.commands.{name}', path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"Failed to load command module {name} from {path}: {e}")


def app():
    # load commands when we start the app (avoid running on import)
    load_commands()

    SESSION = PromptSession()
    # Build completer from the registry at runtime (after loading commands)
    COMPLETER = WordCompleter(list(commands.keys()), ignore_case=True)

    print("Welcome to the BalamPi CLI! Type 'help' to see available commands. Type 'exit' to quit.")
    while True:
        try:
            user_input = prompt('\n> ',
                                history=FileHistory('.cli_history'),
                                auto_suggest=AutoSuggestFromHistory(),
                                completer=COMPLETER)
            user_input = user_input.lower()
            if user_input == 'exit':
                break

            parts = user_input.split()

            if not parts:
                continue

            cmd = parts[0]
            args = parts[1:]

            if cmd in commands:
                try:
                    commands[cmd](args)
                except Exception as e:
                    print(f"Error running command '{cmd}': {e}")
            else:
                print(f"Unknown command: {cmd}")

        except KeyboardInterrupt:
            continue
        except EOFError:
            break


if __name__ == '__main__':
    app()