"""
Notepad Command Grammar
Opens Notepad when you say "open notepad"
"""

from fake_natlink_runtime import natlinkmain
import subprocess

class NotepadGrammar(natlinkmain.GrammarBase):
    """Grammar to open Notepad via voice command"""
    
    def __init__(self):
        super().__init__(name="NotepadGrammar")
        print("📝 Notepad Grammar initialized")
        
        # Define the voice commands this grammar responds to
        self.commands = {
            "open notepad": self.open_notepad,
            "launch notepad": self.open_notepad,
            "start notepad": self.open_notepad,
        }
    
    def open_notepad(self):
        """Open Notepad application"""
        print("📝 Opening Notepad...")
        try:
            subprocess.Popen("notepad.exe")
            print("✅ Notepad launched successfully!")
        except Exception as e:
            print(f"❌ Failed to open Notepad: {e}")
    
    def gotResults(self, words, fullResults):
        """Called when speech is recognized"""
        recognized_text = ' '.join(words).lower()
        print(f"🎤 Heard: '{recognized_text}'")
        
        # Check if the recognized text matches any of our commands
        for command, action in self.commands.items():
            if command in recognized_text:
                action()
                return
        
        print(f"⚠️  No matching command found for: '{recognized_text}'")
    
    def load(self):
        """Load the grammar (called by natlink)"""
        super().load()
        print("✅ Notepad commands active:")
        for cmd in self.commands.keys():
            print(f"   - '{cmd}'")

# Create the grammar instance
grammar = NotepadGrammar()
