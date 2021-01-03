import sys
import cx_Freeze

base = None
if (sys.platform == "win32"):
    base = "Win32GUI" 


cx_Freeze.setup(
    name = "Octoprog",
    version = "1.0",
    options =  {
        "build_exe":{
            "includes": [
                'PySide2',
            ],
            'excludes': [
                'tkinter',
            ],
            "include_files": [
                'src/main.py',
                'src/main_window.py',
                "src/qt",
            ],
        }
    },
    executables = [
        cx_Freeze.Executable(
            "src/main.py", 
            targetName='Octoprog', 
            base=base,
            shortcutName='Octoprog',
            shortcutDir='DesktopFolder'
            )
    ]
) 
