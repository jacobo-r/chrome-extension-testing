Here you go — copy this directly into README.md:

# 🎹 Chrome Extension + Test Page for Global Hotkeys

This project is a **minimal setup** to test controlling a webpage (audio player + clipboard) from **global keyboard shortcuts** in Chrome — even when Chrome is not in focus.  

---

## 📂 Project Structure

```text
test-project/
├── manifest.json      # Chrome extension config
├── background.js      # Background service worker (listens for hotkeys)
├── content.js         # Injected into page, forwards extension messages → page
├── test.html          # Test page with audio + clipboard logic
├── sample1.mp3
├── sample2.mp3
└── sample3.mp3
```
---

## 🔧 How to Use

### 1. Prepare the test page
- Put `test.html` in the same folder as your `.mp3` files.  
- Example: `sample1.mp3`, `sample2.mp3`, `sample3.mp3`.  
- Open `test.html` in Chrome (drag & drop it, or use `File → Open`).

### 2. Load the extension
1. Open Chrome and go to:  

chrome://extensions

2. Enable **Developer mode** (toggle in top right).  
3. Click **Load unpacked** and select the project folder.  
4. In the extension **Details** page, enable **Allow access to file URLs**.

### 3. Configure shortcuts
1. Open:  

chrome://extensions/shortcuts

2. You’ll see your extension commands (Play/Pause, Next, Prev, Copy text).  
3. Change the default shortcut (e.g. from `Ctrl+Shift+5`) to your preferred key (F6, F7, etc.).  
4. Set each shortcut’s scope to **Global** (so they work when Chrome is out of focus).

### 4. Test it
- Open `test.html` in Chrome.  
- Switch focus to another app (e.g. Finder, VSCode).  
- Press your configured hotkeys:  
- **Play/Pause** → toggles the audio.  
- **Next / Prev** → changes the track.  
- **Copy text** → copies `Hello from test app!` to your clipboard.  

You’ll see updates in the test page even when Chrome is not the active window.

---

## 📝 What Each File Does
- **manifest.json** → Defines the extension, permissions, and global hotkeys.  
- **background.js** → Runs in the background; listens for hotkeys and sends messages to the page.  
- **content.js** → Injected into pages; listens for messages from the background script and dispatches custom events.  
- **test.html** → A simple page with an audio player and clipboard logic; reacts to the custom events.  

---

✅ With this setup, you can prove that **Chrome extensions with global shortcuts** can control a background page (like your React app) without bringing Chrome to focus.
