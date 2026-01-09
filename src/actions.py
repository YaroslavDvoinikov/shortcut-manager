from datetime import datetime
from pathlib import Path

import mss
import subprocess
import pyscreenrec

recorder = pyscreenrec.ScreenRecorder()
screen_record_started = False


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
    elif command == 2:
        dir_path = Path(arg)
        now = datetime.now()
        filename = (
                dir_path
                / f"Video-{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}{now.minute:02d}{now.second:02d}.mp4"
        )
        recorder.start_recording(str(filename),30,{
            "mon": 1,
            "left": 100,
            "top": 100,
            "width": 1000,
            "height": 1000
        })
    elif command == 3:
        recorder.stop_recording()

def info(command: int):
    if command == 0:
        return "Run an executable"
    elif command == 1:
        return "Take screenshot"
    elif command == 2:
        return "Start recording screen"
    elif command == 3:
        return "Stop recording screen"
