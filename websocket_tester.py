"""
WebSocket Server Test Script
Simulates the native app to test React app WebSocket implementation
"""
import websocket
import json
import time
import threading
import sys
from datetime import datetime

class WebSocketTester:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.ws_url = f"ws://{host}:{port}"
        self.ws = None
        self.is_connected = False
        self.test_results = {}
        self.responses_received = []
        
    def log(self, message, level="INFO"):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def connect(self):
        """Connect to WebSocket server"""
        try:
            self.log(f"Connecting to {self.ws_url}")
            
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            
            # Run WebSocket in a separate thread
            self.ws.run_forever()
            
        except Exception as e:
            self.log(f"Connection error: {e}", "ERROR")
            return False
    
    def on_open(self, ws):
        """WebSocket connection opened"""
        self.is_connected = True
        self.log("✓ Connected to WebSocket server")
        self.test_results['connection'] = True
    
    def on_message(self, ws, message):
        """WebSocket message received"""
        try:
            data = json.loads(message)
            self.log(f"Received: {data}")
            self.responses_received.append(data)
        except json.JSONDecodeError as e:
            self.log(f"Invalid JSON received: {e}", "ERROR")
    
    def on_error(self, ws, error):
        """WebSocket error occurred"""
        self.log(f"WebSocket error: {error}", "ERROR")
        self.test_results['connection'] = False
    
    def on_close(self, ws, close_status_code, close_msg):
        """WebSocket connection closed"""
        self.is_connected = False
        self.log(f"Connection closed: {close_status_code} - {close_msg}")
    
    def send_command(self, command, data=None):
        """Send a command to the server"""
        if not self.is_connected:
            self.log("Not connected to WebSocket server", "ERROR")
            return False
        
        message = {
            'type': 'command',
            'command': command,
            'timestamp': time.time(),
            'data': data or {}
        }
        
        try:
            self.ws.send(json.dumps(message))
            self.log(f"Sent command: {command}")
            return True
        except Exception as e:
            self.log(f"Error sending command {command}: {e}", "ERROR")
            return False
    
    def send_heartbeat(self):
        """Send heartbeat"""
        if not self.is_connected:
            return False
        
        message = {
            'type': 'heartbeat',
            'timestamp': time.time()
        }
        
        try:
            self.ws.send(json.dumps(message))
            self.log("Sent heartbeat")
            return True
        except Exception as e:
            self.log(f"Error sending heartbeat: {e}", "ERROR")
            return False
    
    def wait_for_response(self, command, timeout=5):
        """Wait for a specific response"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            for response in self.responses_received:
                if response.get('command') == command:
                    return response
            time.sleep(0.1)
        return None
    
    def test_connection(self):
        """Test basic connection"""
        self.log("\n=== Testing Connection ===")
        if self.is_connected:
            self.log("✓ Connection test passed")
            return True
        else:
            self.log("✗ Connection test failed", "ERROR")
            return False
    
    def test_heartbeat(self):
        """Test heartbeat functionality"""
        self.log("\n=== Testing Heartbeat ===")
        
        # Send heartbeat
        if not self.send_heartbeat():
            self.log("✗ Heartbeat test failed - could not send", "ERROR")
            return False
        
        # Wait for response
        time.sleep(1)
        
        # Check if we received a heartbeat response
        heartbeat_response = None
        for response in self.responses_received:
            if response.get('type') == 'heartbeat_response':
                heartbeat_response = response
                break
        
        if heartbeat_response:
            self.log("✓ Heartbeat test passed")
            return True
        else:
            self.log("✗ Heartbeat test failed - no response received", "ERROR")
            return False
    
    def test_play_pause(self):
        """Test play/pause command"""
        self.log("\n=== Testing Play/Pause Command ===")
        
        if not self.send_command('play_pause'):
            self.log("✗ Play/Pause test failed - could not send command", "ERROR")
            return False
        
        # Wait for response
        response = self.wait_for_response('play_pause', timeout=3)
        
        if response:
            if response.get('success'):
                self.log("✓ Play/Pause test passed")
                self.log(f"  Response: {response}")
                return True
            else:
                self.log(f"✗ Play/Pause test failed - command failed: {response.get('error', 'Unknown error')}", "ERROR")
                return False
        else:
            self.log("✗ Play/Pause test failed - no response received", "ERROR")
            return False
    
    def test_next_audio(self):
        """Test next audio command"""
        self.log("\n=== Testing Next Audio Command ===")
        
        if not self.send_command('next'):
            self.log("✗ Next Audio test failed - could not send command", "ERROR")
            return False
        
        response = self.wait_for_response('next', timeout=3)
        
        if response:
            if response.get('success'):
                self.log("✓ Next Audio test passed")
                self.log(f"  Response: {response}")
                return True
            else:
                self.log(f"✗ Next Audio test failed - command failed: {response.get('error', 'Unknown error')}", "ERROR")
                return False
        else:
            self.log("✗ Next Audio test failed - no response received", "ERROR")
            return False
    
    def test_previous_audio(self):
        """Test previous audio command"""
        self.log("\n=== Testing Previous Audio Command ===")
        
        if not self.send_command('previous'):
            self.log("✗ Previous Audio test failed - could not send command", "ERROR")
            return False
        
        response = self.wait_for_response('previous', timeout=3)
        
        if response:
            if response.get('success'):
                self.log("✓ Previous Audio test passed")
                self.log(f"  Response: {response}")
                return True
            else:
                self.log(f"✗ Previous Audio test failed - command failed: {response.get('error', 'Unknown error')}", "ERROR")
                return False
        else:
            self.log("✗ Previous Audio test failed - no response received", "ERROR")
            return False
    
    def test_forward_audio(self):
        """Test forward audio command"""
        self.log("\n=== Testing Forward Audio Command ===")
        
        if not self.send_command('forward'):
            self.log("✗ Forward Audio test failed - could not send command", "ERROR")
            return False
        
        response = self.wait_for_response('forward', timeout=3)
        
        if response:
            if response.get('success'):
                self.log("✓ Forward Audio test passed")
                self.log(f"  Response: {response}")
                return True
            else:
                self.log(f"✗ Forward Audio test failed - command failed: {response.get('error', 'Unknown error')}", "ERROR")
                return False
        else:
            self.log("✗ Forward Audio test failed - no response received", "ERROR")
            return False
    
    def test_backward_audio(self):
        """Test backward audio command"""
        self.log("\n=== Testing Backward Audio Command ===")
        
        if not self.send_command('backward'):
            self.log("✗ Backward Audio test failed - could not send command", "ERROR")
            return False
        
        response = self.wait_for_response('backward', timeout=3)
        
        if response:
            if response.get('success'):
                self.log("✓ Backward Audio test passed")
                self.log(f"  Response: {response}")
                return True
            else:
                self.log(f"✗ Backward Audio test failed - command failed: {response.get('error', 'Unknown error')}", "ERROR")
                return False
        else:
            self.log("✗ Backward Audio test failed - no response received", "ERROR")
            return False
    
    def test_get_transcription(self):
        """Test get transcription command"""
        self.log("\n=== Testing Get Transcription Command ===")
        
        if not self.send_command('get_transcription'):
            self.log("✗ Get Transcription test failed - could not send command", "ERROR")
            return False
        
        response = self.wait_for_response('get_transcription', timeout=3)
        
        if response:
            if response.get('success'):
                transcription = response.get('transcription', '')
                if transcription:
                    self.log("✓ Get Transcription test passed")
                    self.log(f"  Transcription length: {len(transcription)} characters")
                    self.log(f"  Transcription preview: {transcription[:100]}...")
                    return True
                else:
                    self.log("✗ Get Transcription test failed - empty transcription", "ERROR")
                    return False
            else:
                self.log(f"✗ Get Transcription test failed - command failed: {response.get('error', 'Unknown error')}", "ERROR")
                return False
        else:
            self.log("✗ Get Transcription test failed - no response received", "ERROR")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        self.log("WebSocket Server Test Suite")
        self.log("=" * 50)
        self.log(f"Testing WebSocket server at: {self.ws_url}")
        self.log("Make sure your React app WebSocket server is running!")
        self.log("=" * 50)
        
        # Connect to WebSocket
        self.connect()
        
        # Wait a moment for connection
        time.sleep(1)
        
        # Run tests
        tests = [
            self.test_connection,
            self.test_heartbeat,
            self.test_play_pause,
            self.test_next_audio,
            self.test_previous_audio,
            self.test_forward_audio,
            self.test_backward_audio,
            self.test_get_transcription
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                time.sleep(0.5)  # Small delay between tests
            except Exception as e:
                self.log(f"Test {test.__name__} failed with exception: {e}", "ERROR")
                results.append(False)
        
        # Summary
        self.log("\n" + "=" * 50)
        self.log("Test Results Summary:")
        
        test_names = [
            "Connection",
            "Heartbeat", 
            "Play/Pause",
            "Next Audio",
            "Previous Audio",
            "Forward Audio",
            "Backward Audio",
            "Get Transcription"
        ]
        
        passed = sum(results)
        total = len(results)
        
        for i, (name, result) in enumerate(zip(test_names, results)):
            status = "✓ PASS" if result else "✗ FAIL"
            self.log(f"  {name}: {status}")
        
        self.log(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            self.log("🎉 All tests passed! Your WebSocket implementation is correct!")
        else:
            self.log("❌ Some tests failed. Check the errors above.")
            self.log("\nCommon issues:")
            self.log("- WebSocket server not running")
            self.log("- Wrong port (should be 8080)")
            self.log("- Missing command handlers")
            self.log("- Incorrect response format")
        
        return passed == total

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test WebSocket server implementation')
    parser.add_argument('--host', default='localhost', help='WebSocket server host')
    parser.add_argument('--port', type=int, default=8080, help='WebSocket server port')
    
    args = parser.parse_args()
    
    try:
        tester = WebSocketTester(args.host, args.port)
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()