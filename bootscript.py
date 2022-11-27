#bootscript by FlyOS Cloud GPL - 3.0
#creator: Edward Hsing
print("Welcome to FlyOS Cloud!")
import os
import socket
def netip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
        s.close()
    except:
        return 'Failed to obtain IP address'
os.system(f"""
if (whiptail --title "FlyOS Cloud" --yes-button "Reload" --no-button "Settings"  --yesno "FlyOS service has started\nYour IP address:{netip()}\nFlyOS WEB panel address:http://{netip()}" 10 60) then
    echo reload
    python3 /flyos/bootscript.py
else
    python3 /flyos/scripts/settings.py
fi""")