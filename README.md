Here’s a clean README.md you can drop into your mini-project folder:

⸻

🎹 Chrome Extension + Test Page for Global Hotkeys

This project is a minimal setup to test controlling a webpage (audio player + clipboard) from global keyboard shortcuts in Chrome — even when Chrome is not in focus.

⸻

📂 Project Structure

/test-project/
  ├── manifest.json      # Chrome extension config
  ├── background.js      # Background service worker
  ├── content.js         # Script injected into pages
  ├── test.html          # Test page with audio + clipboard logic
  ├── sample1.mp3
  ├── sample2.mp3
  └── sample3.mp3


⸻

🔧 Setup Instructions

1. Prepare the test page
	•	Place your .mp3 files in the same folder as test.html.
	•	Example: sample1.mp3, sample2.mp3, sample3.mp3.
	•	Open test.html in Chrome (drag & drop, or File → Open).

2. Load the extension
	1.	Open Chrome and go to:

chrome://extensions


	2.	Enable Developer mode (toggle in top right).
	3.	Click Load unpacked and select the project folder.
	4.	In your extension’s Details page,
