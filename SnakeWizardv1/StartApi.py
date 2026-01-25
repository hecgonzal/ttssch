import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent
APP_FILE = BASE / "main.py"

def main():
    if not APP_FILE.exists():
        print(f"Error: {APP_FILE} not found")
        sys.exit(1)

    # Run uvicorn as a module so PATH doesn't matter
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]

    print("Starting FastAPI server...")
    subprocess.Popen(cmd, cwd=BASE)

if __name__ == "__main__":
    main()
