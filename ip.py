#!/usr/bin/python
import os
import subprocess
import appindicator
import gtk
import gobject
ICON = os.path.abspath("./images/icon.png")

def get_ip():
    ip = subprocess.check_output('ifconfig |\
        grep -o -P "inet addr:([^ ]*)" |\
        grep -o -P "[0-9.]+"', shell=True)
    ip = ip.replace("127.0.0.1", "")
    return ip.strip()

class IPIndicator:
    def __init__(self):
        self.ip = ""
        self.ind = appindicator.Indicator("ip-indicator", ICON, appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.update()
        self.ind.set_menu(self.setup_menu())
        gobject.timeout_add(5000, self.update)

    def setup_menu(self):
        menu = gtk.Menu()
        refresh = gtk.MenuItem("Refresh")
        refresh.connect("activate", self.on_refresh)
        refresh.show()
        menu.append(refresh)
        return menu

    def update(self):
        """
        
        Update the IP address.
        
        """
        ip = get_ip()
	if not ip:
	    ip = "No IP"
        if ip != self.ip:
            self.ip = ip
            self.ind.set_label(ip)
        # Timeout function requires function to return True
        return True

    def on_refresh(self, widget):
        self.update()


if __name__ == "__main__":
    i = IPIndicator()
    gtk.main()

