import os
import subprocess
import sys
import wave
from datetime import datetime
from pathlib import Path

import mss
import pyaudio
import pyscreenrec

recorder = pyscreenrec.ScreenRecorder()
screen_record_started = False

pa = pyaudio.PyAudio()
stream = pa.open(
    format=pyaudio.paInt16, channels=2, rate=44400, input=True, frames_per_buffer=1024
)
frames = []
audio_record_started = False


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
        case 3:
            if sys.platform == "linux":
                subprocess.run(["shutdown", "now"])
            elif sys.platform == "win32":
                subprocess.run(["shutdown", "/s", "/t", "0"])
        case 4:
            if sys.platform == "linux":
                subprocess.run(["reboot"])
            elif sys.platform == "win32":
                subprocess.run(["shutdown", "/r", "/t", "0"])
        case 5:
            if sys.platform == "linux":
                os.system("pkill -KILL -u" + os.getlogin())
            elif sys.platform == "win32":
                subprocess.run(["shutdown", "/l", "/t", "0"])
        case 6:
            global audio_record_started
            global frames
            global pa
            global stream
            if not audio_record_started:
                audio_record_started = True
                pa = pyaudio.PyAudio()
                stream = pa.open(
                    format=pyaudio.paInt16,
                    channels=2,
                    rate=44400,
                    input=True,
                    frames_per_buffer=1024,
                )
                frames = []
                for i in range(0, int(44400 / 1024 * 4)):
                    data = stream.read(1024)
                    frames.append(data)
            else:
                audio_record_started = False
                stream.stop_stream()
                stream.close()
                pa.terminate()

                dir_path = Path(args[0])
                now = datetime.now()
                filename = (
                    dir_path
                    / f"Audio-{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}{now.minute:02d}{now.second:02d}.wav"
                )

                sf = wave.open(str(filename), "wb")
                sf.setnchannels(2)
                sf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
                sf.setframerate(44400)
                sf.writeframes(b"".join(frames))
                sf.close()


def info(command: int):
    text = [
        "Run an executable",
        "Take screenshot",
        "Start recording screen",
        "Power off",
        "Reboot",
        "Log out",
        "Record audio",
    ]
    return text[command]


def stop_recording():
    if screen_record_started:
        recorder.stop_recording()
