#!/usr/bin/env python3
import os
import subprocess
import sys


def check_venv():
    try:
        # Проверяем, активирована ли виртуальная среда
        subprocess.run([sys.executable, "-c", "import uvicorn"], check=True)
        print("Venv is healthy.")
    except subprocess.CalledProcessError:
        print("Venv seems to be broken. Reinstalling dependencies...")
        reinstall_dependencies()


def reinstall_dependencies():
    # Устанавливаем зависимости через Poetry
    result = subprocess.run(["poetry", "install", "--no-root"], check=False)
    if result.returncode == 0:
        print("Dependencies reinstalled successfully.")
    else:
        print("Failed to reinstall dependencies.")


if __name__ == "__main__":
    check_venv()
