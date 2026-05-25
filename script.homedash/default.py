import os
import sys

import xbmcaddon
import xbmcgui

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo("path")
# Kodi does not add the addon's lib dir to sys.path for plain scripts, so do it.
sys.path.append(os.path.join(ADDON_PATH, "resources", "lib"))

import feeds  # noqa: E402  (path appended above)

LIST_ID = 100


class Dashboard(xbmcgui.WindowXML):
    def onInit(self):
        lst = self.getControl(LIST_ID)
        lst.reset()
        items = []
        for e in feeds.fetch_all(feeds.configured_feeds(ADDON)):
            li = xbmcgui.ListItem(e["title"])
            li.setLabel2(f"{e['source']}   {e['date']}")
            items.append(li)
        if not items:
            items = [xbmcgui.ListItem("No items. Set feed URLs in addon settings.")]
        lst.addItems(items)
        self.setFocusId(LIST_ID)

    def onAction(self, action):
        # 9 parent, 10 previous menu, 92 nav-back: any of these closes the window.
        if action.getId() in (9, 10, 92):
            self.close()


def run():
    # XML resolves to resources/skins/Default/1080i/script-homedash-main.xml
    win = Dashboard("script-homedash-main.xml", ADDON_PATH, "Default", "1080i")
    win.doModal()
    del win


if __name__ == "__main__":
    run()
