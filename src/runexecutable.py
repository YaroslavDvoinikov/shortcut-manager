import subprocess


class RunAnExecutable:
    def action(self, *args):
        subprocess.Popen(args[0])

    def info():
        return "Run an executable"
