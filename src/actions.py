import subprocess
from datetime import datetime
from pathlib import Path

import mss
import pyscreenrec

recorder = pyscreenrec.ScreenRecorder()
screen_record_started = False


def action(command: int, *args):
    match command:
        case 0:
            subprocess.Popen(args[0])
        case 1:
            with mss.mss() as sct:
                dir_path = Path(args[0])
                now = datetime.now()
                filename = (
                    dir_path
                    / f"Screenshot-{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}{now.minute:02d}{now.second:02d}.png"
                )
                sct.shot(output=str(filename))
        case 2:
            global screen_record_started
            if not screen_record_started:
                screen_record_started = True
                dir_path = Path(args[0])
                now = datetime.now()
                filename = (
                    dir_path
                    / f"Video-{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}{now.minute:02d}{now.second:02d}.mp4"
                )
                recorder.start_recording(
                    str(filename),
                    30,
                    {
                        "mon": 1,
                        "left": 0,
                        "top": 0,
                        "width": args[1],
                        "height": args[2],
                    },
                )

            else:
                screen_record_started = False
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
