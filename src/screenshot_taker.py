from datetime import datetime
from pathlib import Path

import mss


class ScreenshotTaker:
    def action(self, *args):
        with mss.mss() as sct:
            dir_path = Path(args[0])
            now = datetime.now()
            filename = (
                dir_path
                / f"Screenshot-{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}{now.minute:02d}{now.second:02d}.png"
            )
            sct.shot(output=str(filename))

    def info():
        return "Take screenshot"
