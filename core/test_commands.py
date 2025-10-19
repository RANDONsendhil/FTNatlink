"""
Test voice commands without actual speech recognition
Simulates what Dragon would send to your grammars
"""

import sys, os
sys.path.append(os.path.abspath("packages/natlink/pythonsrc"))
sys.path.append(os.path.abspath("packages/natlinkcore"))

import natlink
from fake_natlink_runtime import natlinkmain
from grammar_loader import load_all_grammars

def test_command(grammar_name, command_text):
    """Simulate a voice command being recognized"""
    print(f"\n{'='*60}")
    print(f"🎤 Simulating voice command: '{command_text}'")
    print(f"   Target grammar: {grammar_name}")
    print(f"{'='*60}")
    
    grammars = load_all_grammars()
    
    if grammar_name in grammars:
        module = grammars[grammar_name]
        if hasattr(module, 'grammar'):
            # Simulate the grammar receiving recognized words
            words = command_text.split()
            module.grammar.gotResults(words, None)
        else:
            print(f"❌ Grammar '{grammar_name}' has no grammar object")
    else:
        print(f"❌ Grammar '{grammar_name}' not found")
        print(f"Available grammars: {list(grammars.keys())}")

if __name__ == "__main__":
    print("🎯 Voice Command Test Suite")
    print("="*60)
    
    # Test 1: Open Notepad
    test_command("notepad_grammar", "open notepad")
    
    # Test 2: Launch Notepad (alternative command)
    test_command("notepad_grammar", "launch notepad")
    
    # Test 3: Sample grammar
    test_command("sample_grammar", "hello test")
    
    # Test 4: Unknown command
    test_command("notepad_grammar", "close notepad")
    
    print(f"\n{'='*60}")
    print("✅ All tests completed!")
    print(f"{'='*60}")
