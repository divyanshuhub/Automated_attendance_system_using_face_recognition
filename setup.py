import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"],"include_files":['tcl86t.dll','tk86t.dll']}
#build_exe_options = {"packages": ["os"],"include_files":['tcl86t.dll','tk86t.dll','opencv_videoio_ffmpeg452_64.dll']}
# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Project Name",
        version = "0.1",
        description = "description",
        options = {"build_exe": build_exe_options},
        executables = [Executable("gui_final.py", base=base)])
