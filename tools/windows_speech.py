"""
Windows Speech Recognition Alternative to Dragon NaturallySpeaking
Uses Windows built-in speech recognition for testing natlink functionality
"""

import speech_recognition as sr
import pyttsx3
import threading
import time
from typing import Optional, Callable

class WindowsSpeechRecognition:
    """Windows Speech Recognition implementation for natlink testing"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.mic_state = "off"  # "on", "off", "sleeping", "disabled"
        self.callbacks = {}
        
        # Text-to-speech engine
        self.tts = pyttsx3.init()
        
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("Ready for speech recognition!")
    
    def getMicState(self) -> str:
        """Get microphone state - mimics natlink.getMicState()"""
        return self.mic_state
    
    def setMicState(self, state: str) -> None:
        """Set microphone state"""
        if state in ["on", "off", "sleeping", "disabled"]:
            self.mic_state = state
            print(f"Microphone state changed to: {state}")
            
            if state == "on":
                self.start_listening()
            else:
                self.stop_listening()
    
    def start_listening(self):
        """Start continuous listening"""
        if not self.is_listening:
            self.is_listening = True
            self.mic_state = "on"
            
            # Start listening in background thread
            self.listen_thread = threading.Thread(target=self._listen_continuously, daemon=True)
            self.listen_thread.start()
            print("🎤 Started listening for speech commands...")
    
    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False
        if self.mic_state != "disabled":
            self.mic_state = "off"
        print("🔇 Stopped listening")
    
    def _listen_continuously(self):
        """Continuous listening loop"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                try:
                    # Recognize speech using Windows Speech Recognition
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"🗣️  Heard: '{text}'")
                    
                    # Process the command
                    self._process_command(text)
                    
                except sr.UnknownValueError:
                    # Could not understand audio
                    pass
                except sr.RequestError as e:
                    print(f"Error with speech recognition: {e}")
                    
            except sr.WaitTimeoutError:
                # No speech detected within timeout
                pass
            except Exception as e:
                print(f"Listening error: {e}")
                time.sleep(0.1)
    
    def _process_command(self, text: str):
        """Process recognized speech command"""
        # Built-in commands
        if "microphone off" in text or "mic off" in text:
            self.setMicState("off")
            self.speak("Microphone off")
            return
        
        if "microphone on" in text or "mic on" in text:
            self.setMicState("on")
            self.speak("Microphone on")
            return
        
        if "sleep" in text:
            self.setMicState("sleeping")
            self.speak("Going to sleep")
            return
        
        # Call registered callbacks
        for pattern, callback in self.callbacks.items():
            if pattern in text:
                try:
                    callback(text)
                except Exception as e:
                    print(f"Error in callback: {e}")
                return
        
        # Default response
        print(f"✅ Command recognized: '{text}'")
        self.speak(f"I heard {text}")
    
    def speak(self, text: str):
        """Text-to-speech output"""
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def register_command(self, pattern: str, callback: Callable):
        """Register a voice command callback"""
        self.callbacks[pattern.lower()] = callback
        print(f"Registered command: '{pattern}'")
    
    def getDNSVersion(self) -> int:
        """Mock Dragon version"""
        return 0  # Windows Speech Recognition version


def demo_commands():
    """Demo function showing how to use the speech recognition"""
    
    # Create speech recognition instance
    speech = WindowsSpeechRecognition()
    
    # Register some demo commands
    def hello_command(text):
        print("Hello command triggered!")
        speech.speak("Hello there!")
    
    def time_command(text):
        import datetime
        now = datetime.datetime.now().strftime("%H:%M")
        speech.speak(f"The time is {now}")
    
    def calculator_command(text):
        speech.speak("Opening calculator")
        import subprocess
        subprocess.run("calc.exe")
    
    # Register commands
    speech.register_command("hello", hello_command)
    speech.register_command("what time", time_command)
    speech.register_command("open calculator", calculator_command)
    
    # Start listening
    speech.setMicState("on")
    
    # Keep running
    try:
        print("\n" + "="*60)
        print("VOICE COMMANDS ACTIVE")
        print("="*60)
        print("Try saying:")
        print("  - 'Hello'")
        print("  - 'What time is it'")
        print("  - 'Open calculator'")
        print("  - 'Microphone off' (to stop)")
        print("="*60)
        
        while speech.getMicState() == "on":
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nStopping...")
        speech.stop_listening()


if __name__ == "__main__":
    demo_commands()
