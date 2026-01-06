from datetime import datetime
from pathlib import Path

import mss
import subprocess

def action(command: int, arg):
    if command == 0:
        subprocess.Popen(arg)
    elif command == 1:
        with mss.mss() as sct:
            dir_path = Path(arg)
            now = datetime.now()
            filename = (
                    dir_path
                    / f"Screenshot-{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}{now.minute:02d}{now.second:02d}.png"
            )
            sct.shot(output=str(filename))

def info(command: int):
    if command == 0:
        return "Run an executable"
    elif command == 1:
        return "Take screenshot"
