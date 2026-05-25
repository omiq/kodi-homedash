"""Runs at Kodi startup. Launches the dashboard window once the GUI is up.
Backing out of the dashboard returns to the normal Kodi home, so this is a
soft "startup page" rather than a lock-in. Toggle via the 'autostart' setting.
"""
import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()


def main():
    monitor = xbmc.Monitor()
    # Let the GUI finish coming up before throwing a modal window at it.
    if monitor.waitForAbort(5):
        return
    if ADDON.getSettingBool("autostart"):
        xbmc.executebuiltin("RunScript(script.homedash)")


if __name__ == "__main__":
    main()
