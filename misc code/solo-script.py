#!c:\python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'solo-cli==1.2.0','console_scripts','solo'
__requires__ = 'solo-cli==1.2.0'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('solo-cli==1.2.0', 'console_scripts', 'solo')()
    )
