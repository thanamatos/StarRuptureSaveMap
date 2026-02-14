# Star Rupture Save Map

A single-file web app that analyzes Star Rupture save files (`.sav`): view buildings, production, storage, package transport, and a map of building locations.

## Download

**Option 1 – Clone the repo**
```bash
git clone https://github.com/your-username/StarRuptureSaveMap.git
cd StarRuptureSaveMap
```
(Use the clone URL from the repo’s **Code** button on GitHub.)

**Option 2 – Download the file**
- Open the repo on GitHub and click **Code** → **Download ZIP**, or
- Download only [portable.html](portable.html) (right‑click → Save link as).

## Run locally

1. Open **portable.html** in a web browser:
   - **Double‑click** `portable.html` in your file manager, or
   - **Drag** `portable.html` into an open browser window, or
   - From the browser: **File → Open File** and choose `portable.html`.

2. On the start screen, click **Open .sav File** (or drag and drop a `.sav` file onto the page).

3. Your save is analyzed in the browser; nothing is sent to a server. You can then use the **Buildings**, **Production**, **Storage**, **Map**, and **Package transport** tabs.

## Where to find your save file

Star Rupture stores saves under your Steam userdata folder, for example:

- **Windows:** `C:\Program Files (x86)\Steam\userdata\<USER_ID>\1631270\remote\Saved\SaveGames\`
- **Linux/Steam Deck:** `~/.steam/steam/steamapps/compatdata/1631270/pfx/drive_c/users/steamuser/AppData/Local/StarRupture/Saved/SaveGames/` (path may vary)

Use a `.sav` file from the folder that matches your game version (e.g. `beta1`).

## Requirements

- A modern browser (Chrome, Firefox, Edge, Safari).
- The map loads a base image from the internet; otherwise the app works offline once the page is loaded.
