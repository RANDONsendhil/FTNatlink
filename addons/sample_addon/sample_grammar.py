"""
Sample Grammar for Testing
This demonstrates how to create a voice command grammar for natlink
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.fake_natlink_runtime import natlinkmain

class SampleGrammar(natlinkmain.GrammarBase):
    """Sample grammar that responds to voice commands"""
    
    def __init__(self):
        super().__init__(name="SampleGrammar")
        print("🎤 Sample Grammar initialized")
    
    def gotResults(self, words, fullResults):
        """Called when speech is recognized"""
        print(f"✅ Recognized: {' '.join(words)}")
        
        # Handle specific commands
        if "hello" in words:
            print("👋 Hello command received!")
        elif "test" in words:
            print("🧪 Test command received!")

# Create the grammar instance
grammar = SampleGrammar()
