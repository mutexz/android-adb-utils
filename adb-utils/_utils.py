import os
import subprocess
import sys

import whichcraft
from pkg_resources import resource_filename


def adb_path():
    if os.getenv("ADBUTILS_ADB_PATH"):
        return os.getenv("ADBUTILS_ADB_PATH")

    exe = whichcraft.which("adb")
    if exe and _is_valid_exe(exe):
        return exe
    adb_bin_dir = resource_filename("adb-utils", "binaries")
    exe = os.path.join(adb_bin_dir, "adb.exe" if os.name == "nt" else "adb")
    if os.path.isfile(exe) and _is_valid_exe(exe):
        return exe
    raise RuntimeError("No adb exe could be found. Install adb on your system")


def _is_valid_exe(exe: str) -> bool:
    cmd = [exe, "version"]
    try:
        subprocess.check_call(
            cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT, **_popen_kwargs()
        )
        return True
    except (OSError, ValueError, subprocess.CalledProcessError):
        return False


def _popen_kwargs(prevent_sigint=False):
    startupinfo = None
    preexec_fn = None
    creationflags = 0
    if sys.platform.startswith("win"):
        # Stops executable from flashing on Windows (see imageio/imageio-ffmpeg#22)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    if prevent_sigint:
        # Prevent propagation of sigint (see imageio/imageio-ffmpeg#4)
        # https://stackoverflow.com/questions/5045771
        if sys.platform.startswith("win"):
            creationflags = 0x00000200
        else:
            preexec_fn = os.setpgrp  # the _pre_exec does not seem to work
    return {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "preexec_fn": preexec_fn,
    }


if __name__ == "__main__":
    adb_path()