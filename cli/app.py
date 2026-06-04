from cli import app
import sys

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
    app()


if __name__ == "__main__":    main()