chrome.runtime.onMessage.addListener((msg) => {
  // Dispatch a custom event your page can listen for
  window.dispatchEvent(
    new CustomEvent("extensionCommand", { detail: { command: msg.command } })
  );
});
