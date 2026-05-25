# kodi-homedash

A launchable custom **home dashboard** for Kodi. Your own Python + one XML
layout, not tied to a skin. v0.1 shows RSS; reminders and bin day come next.

Addon lives in `script.homedash/`.

## Install

**Easiest (works on any Kodi, incl. Android TV / LibreELEC):**
1. Zip the addon folder so the zip contains `script.homedash/` at its root:
   ```bash
   cd ~/github/kodi-homedash
   zip -r script.homedash.zip script.homedash
   ```
2. Copy the zip to the box (USB / network share / `scp`).
3. Kodi → Settings → System → Add-ons → enable **Unknown sources**.
4. Kodi → Add-ons → **Install from zip file** → pick `script.homedash.zip`.

**Or copy the folder directly** into Kodi's addons dir (then restart Kodi):
- LibreELEC / CoreELEC: `/storage/.kodi/addons/`
- Linux: `~/.kodi/addons/`
- macOS: `~/Library/Application Support/Kodi/addons/`
- Windows: `%APPDATA%\Kodi\addons\`

## Run

- Add-ons → Program add-ons → **Home Dashboard**, or
- bind it anywhere with `RunScript(script.homedash)` (keymap, favourite, or a
  skin home-menu button).

**Launch on startup:** put a `service.py`/autoexec calling `RunScript`, or add a
favourite and set it as the startup action. (v0.1 is launch-on-demand; auto-open
is a small follow-up.)

## Configure feeds

Add-on settings → **Feed URLs** (comma or newline separated). Defaults to the
retrogamecoders.com feed. Parser is stdlib-only and handles both RSS and Atom.

## Expect to tweak (the skinning friction)

Fonts (`font13`, `font30`), the `white.png` texture, and coordinates in
`resources/skins/Default/1080i/script-homedash-main.xml` are **skin-dependent**.
If text is the wrong size or the background does not draw, that file is where you
adjust. The Python (`resources/lib/feeds.py`, `default.py`) is validated and
shouldn't need changes for layout fixes.

## Roadmap (next panels)

- **Reminders** from the vault (Haversack todos) or a Google Calendar iCal.
- **Bin day** from your council (iCal / postcode lookup / scrape), cached.
- A background **service addon** to refresh data and set window properties, so
  panels update without reopening.
- Auto-open at startup.
