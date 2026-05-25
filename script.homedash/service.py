"""Runs at Kodi startup. Opens the dashboard once the home window is actually
up, so we never throw a modal at a half-initialised GUI (which can wedge Kodi at
boot). Backing out returns to normal Kodi home. Toggle via 'autostart' setting.
"""
import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()


def main():
    if not ADDON.getSettingBool("autostart"):
        return
    monitor = xbmc.Monitor()
    # Wait for the skin/home window to be live before launching our window.
    for _ in range(60):
        if monitor.abortRequested():
            return
        if xbmc.getCondVisibility("Window.IsActive(home)"):
            break
        if monitor.waitForAbort(1):
            return
    else:
        return  # home never came up within 60s; bail rather than risk a crash
    if monitor.waitForAbort(3):  # let the home screen settle
        return
    xbmc.executebuiltin("RunScript(script.homedash)")


if __name__ == "__main__":
    main()
