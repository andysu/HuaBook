import time
import os
import subprocess

def get_mtime(filepath):
    try:
        return os.path.getmtime(filepath)
    except OSError:
        return 0

def main():
    print("Auto-builder started. Watching HuaweiBook.md for changes...")
    file_to_watch = "HuaweiBook.md"
    last_mtime = get_mtime(file_to_watch)

    while True:
        time.sleep(5)
        current_mtime = get_mtime(file_to_watch)
        if current_mtime > last_mtime:
            print(f"[{time.strftime('%X')}] {file_to_watch} changed. Rebuilding docs...")
            subprocess.run(["make", "html"], cwd="docs")
            last_mtime = current_mtime

if __name__ == "__main__":
    main()
