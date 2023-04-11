#!c:\python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'dronekit-sitl==3.1.0','console_scripts','dronekit-sitl'
__requires__ = 'dronekit-sitl==3.1.0'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('dronekit-sitl==3.1.0', 'console_scripts', 'dronekit-sitl')()
    )
