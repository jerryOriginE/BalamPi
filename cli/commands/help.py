from registry import register
from registry import commands

@register('help')
def help(args):
    print("Available commands:")
    for cmd in sorted(commands.keys()):
        print(f" - {cmd}")