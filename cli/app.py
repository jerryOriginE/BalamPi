import sys
import os
import importlib.util

VERSION = "0.1.0"

if "--version" in sys.argv or "-v" in sys.argv:
    print(f"BalamPi CLI Version: {VERSION}")
    sys.exit(0)
if "--author" in sys.argv or "-a" in sys.argv:
    print("BalamPi CLI Author: Gerardo L. Guizar")
    sys.exit(0)

if "--help" in sys.argv or "-h" in sys.argv:
    print("BalamPi CLI - Control your BalamPi robot from the command line!")
    print("Usage: python app.py [options]")
    print("Options:")
    print("  --version, -v   Show version information")
    print("  --author, -a    Show author information")
    print("  --help, -h      Show this help message")
    sys.exit(0)


def main():
    # Load the local cli.py module (same directory) and call app()
    base_dir = os.path.dirname(__file__)
    cli_path = os.path.join(base_dir, 'cli.py')
    if not os.path.exists(cli_path):
        print(f"cli.py not found in {base_dir}")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location('local_cli', cli_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, 'app'):
        print("cli.py does not expose an `app()` function")
        sys.exit(1)

    module.app()


if __name__ == "__main__":
    main()