import subprocess
try:
    from ctypes import windll
except:
    raise ImportError('ctypes must be installed for this module to work.')

SHERB_NOCONFIRMATION = 1
SHERB_NOPROGRESSUI   = 2
SHERB_NOSOUND        = 4

EWX_LOGOFF = 0x00000000

CREATE_NO_WINDOW = 0x08000000

def EmptyRecycleBin():
    windll.shell32.SHEmptyRecycleBinA(None, None, SHERB_NOCONFIRMATION)

def OpenRecycleBin():
    subprocess.call(["cmd", "/c", "start", "shell:RecycleBinFolder"], creationflags=CREATE_NO_WINDOW)

def LockWorkStation():
    windll.user32.LockWorkStation()

def Logout():
    windll.user32.ExitWindowsEx(EWX_LOGOFF, 1)

def Restart():
    subprocess.call(["shutdown.exe", "-r", "-t", "0"], creationflags=CREATE_NO_WINDOW)

def Sleep():
    windll.PowrProf.SetSuspendState(0, 1, 0)

def Hibernate():
    windll.PowrProf.SetSuspendState(1, 1, 0)

def Shutdown():
    subprocess.call(["shutdown.exe", "-s", "-t", "0"], creationflags=CREATE_NO_WINDOW)