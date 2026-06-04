from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

import os
import importlib

def load_commands():
    for file in os.listdir('commands'):
        if file.endswith('.py') and file != '__init__.py':
            importlib.import_module(f'commands.{file[:-3]}')

load_commands()

from registry import commands
#print(commands)

SESSION = PromptSession()
COMPLETER = WordCompleter(commands.keys(), ignore_case=True)

def app():
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
                commands[cmd](args)
            else:
                print(f"Unknown command: {cmd}")

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

app()