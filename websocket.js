// Add this to your React app (Node.js/Express setup)
const WebSocket = require('ws');

// Create WebSocket server on port 8080
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  console.log('Native app connected via WebSocket');
  
  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message);
      console.log('Received from native app:', data);
      
      if (data.type === 'command') {
        handleWebSocketCommand(data.command, ws);
      } else if (data.type === 'heartbeat') {
        // Respond to heartbeat
        ws.send(JSON.stringify({ type: 'heartbeat_response', timestamp: Date.now() }));
      }
    } catch (error) {
      console.error('WebSocket message error:', error);
    }
  });
  
  ws.on('close', () => {
    console.log('Native app disconnected from WebSocket');
  });
});

function handleWebSocketCommand(command, ws) {
  try {
    let result = { success: false, command: command };
    
    switch (command) {
      case 'play_pause':
        const audioElement = document.getElementById('player');
        if (audioElement.paused) {
          audioElement.play();
        } else {
          audioElement.pause();
        }
        result.success = true;
        result.isPlaying = !audioElement.paused;
        break;
        
      case 'next':
        const nextIndex = (currentAudioIndex + 1) % audioFiles.length;
        currentAudioIndex = nextIndex;
        audioElement.src = audioFiles[nextIndex];
        audioElement.play();
        result.success = true;
        result.currentFile = audioFiles[nextIndex];
        break;
        
      case 'previous':
        const prevIndex = (currentAudioIndex - 1 + audioFiles.length) % audioFiles.length;
        currentAudioIndex = prevIndex;
        audioElement.src = audioFiles[prevIndex];
        audioElement.play();
        result.success = true;
        result.currentFile = audioFiles[prevIndex];
        break;
        
      case 'forward':
        audioElement.currentTime += 10;
        result.success = true;
        result.currentTime = audioElement.currentTime;
        break;
        
      case 'backward':
        audioElement.currentTime -= 10;
        result.success = true;
        result.currentTime = audioElement.currentTime;
        break;
        
      case 'get_transcription':
        // THIS IS THE KEY PART FOR COPY TRANSCRIPTION
        const transcription = getCurrentTranscription();
        result.success = true;
        result.transcription = transcription; // Send transcription back
        break;
        
      default:
        result.error = 'Unknown command';
    }
    
    // Send response back to native app
    ws.send(JSON.stringify({
      type: 'response',
      ...result,
      timestamp: Date.now()
    }));
    
  } catch (error) {
    ws.send(JSON.stringify({
      type: 'response',
      success: false,
      command: command,
      error: error.message,
      timestamp: Date.now()
    }));
  }
}

// Helper function - YOU NEED TO IMPLEMENT THIS
function getCurrentTranscription() {
  // Return your current transcription text
  // This should return whatever transcription is currently displayed/available
  return currentTranscription || "No transcription available";
}