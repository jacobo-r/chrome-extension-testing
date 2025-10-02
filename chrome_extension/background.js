chrome.commands.onCommand.addListener(async (command) => {
  // Look for your test page or localhost app
  const tabs = await chrome.tabs.query({
    url: ["file:///*", "http://localhost:3000/*"]
  });

  if (!tabs.length) {
    console.log("No matching tab open");
    return;
  }

  // Just send the message — no injection needed anymore
  chrome.tabs.sendMessage(tabs[0].id, { command });
});
