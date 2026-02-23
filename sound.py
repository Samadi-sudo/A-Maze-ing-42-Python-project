import subprocess

_running_sounds = {}


def play_song(sound_path):
    process = _running_sounds.get(sound_path)

    if process and process.poll() is None:
        return

    try:
        process = subprocess.Popen(["aplay", sound_path])
        _running_sounds[sound_path] = process
    except Exception as e:
        print(f"Sound Error: {e}")


def stop_song(sound_path):
    process = _running_sounds.get(sound_path)
    if process and process.poll() is None:
        process.terminate()
