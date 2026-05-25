import os
import sys

import xbmcaddon
import xbmcgui

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo("path")
# Kodi does not add the addon's lib dir to sys.path for plain scripts, so do it.
sys.path.append(os.path.join(ADDON_PATH, "resources", "lib"))

import bins  # noqa: E402
import feeds  # noqa: E402  (path appended above)

LIST_ID = 100
BIN_LABEL_ID = 200


class Dashboard(xbmcgui.WindowXML):
    def onInit(self):
        self._set_bin_line()
        lst = self.getControl(LIST_ID)
        lst.reset()
        self._entries = feeds.fetch_all(feeds.configured_feeds(ADDON))
        items = []
        for e in self._entries:
            li = xbmcgui.ListItem(e["title"])
            li.setLabel2(f"{e['source']}   {e['date']}")
            items.append(li)
        if not items:
            items = [xbmcgui.ListItem("No items. Set feed URLs in addon settings.")]
        lst.addItems(items)
        self.setFocusId(LIST_ID)

    def onClick(self, control_id):
        if control_id != LIST_ID or not getattr(self, "_entries", None):
            return
        pos = self.getControl(LIST_ID).getSelectedPosition()
        if not 0 <= pos < len(self._entries):
            return
        e = self._entries[pos]
        body = e.get("body") or "(no summary in feed)"
        link = e.get("link")
        if link:
            body = f"{body}\n\n{link}"
        xbmcgui.Dialog().textviewer(e["title"], body)

    def _set_bin_line(self):
        # Best-effort: bin_url is per-device (addon settings), empty until set.
        try:
            line = bins.format_line(bins.next_collection(ADDON.getSetting("bin_url")))
        except Exception:
            line = ""
        try:
            self.getControl(BIN_LABEL_ID).setLabel(line)
        except Exception:
            pass  # label control absent in some skin tweak; non-fatal

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
