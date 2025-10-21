"""
Fake Runtime Grammar Development Script
Use this to develop and test voice grammars without full natlink DLL registration
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.fake_natlink_runtime import natlinkmain


class SimpleTestGrammar(natlinkmain.GrammarBase):
    """Simple grammar for testing voice commands"""

    def __init__(self):
        super().__init__(name="SimpleTestGrammar")
        print("🎤 Simple Test Grammar initialized")

        # Define voice commands
        self.commands = {
            "hello world": self.say_hello,
            "open calculator": self.open_calculator,
            "test command": self.test_function,
            "show time": self.show_time,
        }

    def say_hello(self):
        """Simple hello response"""
        print("👋 Hello! Voice command recognized!")

    def open_calculator(self):
        """Open Windows calculator"""
        print("🧮 Opening Calculator...")
        try:
            import subprocess

            subprocess.Popen("calc.exe")
            print("✅ Calculator opened successfully!")
        except Exception as e:
            print(f"❌ Failed to open calculator: {e}")

    def test_function(self):
        """Test function for development"""
        print("🧪 Test command executed successfully!")
        print("💡 You can add your custom logic here")

    def show_time(self):
        """Show current time"""
        import datetime

        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"🕐 Current time: {current_time}")

    def gotResults(self, words, fullResults):
        """Called when speech is recognized (simulated)"""
        recognized_text = " ".join(words).lower()
        print(f"🎤 Heard: '{recognized_text}'")

        # Check if the recognized text matches any commands
        for command, action in self.commands.items():
            if command in recognized_text:
                action()
                return

        print(f"⚠️  No matching command found for: '{recognized_text}'")

    def load(self):
        """Load the grammar"""
        super().load()
        print("✅ Simple Test Grammar loaded successfully!")
        print("📋 Available commands:")
        for cmd in self.commands.keys():
            print(f"   - '{cmd}'")


def simulate_voice_input():
    """Simulate voice input for testing"""
    print("\n🎯 Voice Input Simulation")
    print("=" * 40)

    # Create and load grammar
    grammar = SimpleTestGrammar()
    grammar.load()

    # Simulate some voice commands
    test_commands = [
        ["hello", "world"],
        ["open", "calculator"],
        ["test", "command"],
        ["show", "time"],
        ["unknown", "command"],  # This should not match
    ]

    print("\n🎬 Simulating voice commands...")
    for words in test_commands:
        print(f"\n🎤 Simulating: {' '.join(words)}")
        grammar.gotResults(words, None)


def create_new_grammar_template():
    """Create a template for a new grammar"""
    template = '''"""
New Grammar Template
Replace this with your grammar description
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.fake_natlink_runtime import natlinkmain
import subprocess


class MyNewGrammar(natlinkmain.GrammarBase):
    """Your custom grammar description"""

    def __init__(self):
        super().__init__(name="MyNewGrammar")
        print("🎤 My New Grammar initialized")

        # Define your voice commands here
        self.commands = {
            "your command": self.your_function,
            "another command": self.another_function,
        }

    def your_function(self):
        """Your custom function"""
        print("✅ Your command executed!")
        # Add your logic here

    def another_function(self):
        """Another custom function"""
        print("✅ Another command executed!")
        # Add your logic here

    def gotResults(self, words, fullResults):
        """Called when speech is recognized"""
        recognized_text = " ".join(words).lower()
        print(f"🎤 Heard: '{recognized_text}'")

        # Check if the recognized text matches any commands
        for command, action in self.commands.items():
            if command in recognized_text:
                action()
                return

        print(f"⚠️  No matching command found for: '{recognized_text}'")

    def load(self):
        """Load the grammar"""
        super().load()
        print("✅ My New Grammar loaded!")
        for cmd in self.commands.keys():
            print(f"   - '{cmd}'")


# Create the grammar instance
grammar = MyNewGrammar()
'''

    new_grammar_path = project_root / "grammars" / "new_grammar_template.py"
    new_grammar_path.parent.mkdir(exist_ok=True)

    with open(new_grammar_path, "w", encoding="utf-8") as f:
        f.write(template)

    print(f"📄 New grammar template created: {new_grammar_path}")
    print("✏️  Edit this file to create your custom voice commands")


def main():
    """Main function"""
    print("🚀 Fake Runtime Grammar Development")
    print("=" * 50)
    print("This script helps you develop voice grammars using the fake runtime")
    print("Perfect for testing without full Dragon integration!\n")

    while True:
        print("\n📋 Choose an option:")
        print("1. Run simulation test")
        print("2. Create new grammar template")
        print("3. List existing grammars")
        print("4. Test notepad grammar")
        print("5. Exit")

        choice = input("\n👉 Enter your choice (1-5): ").strip()

        if choice == "1":
            simulate_voice_input()
        elif choice == "2":
            create_new_grammar_template()
        elif choice == "3":
            list_existing_grammars()
        elif choice == "4":
            test_notepad_grammar()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


def list_existing_grammars():
    """List existing grammar files"""
    print("\n📁 Existing Grammar Files:")
    print("=" * 30)

    # Check grammars directory
    grammars_dir = project_root / "grammars"
    if grammars_dir.exists():
        for grammar_file in grammars_dir.glob("*.py"):
            if grammar_file.name != "__init__.py":
                print(f"📄 {grammar_file.name}")

    # Check addons
    addons_dir = project_root / "addons"
    if addons_dir.exists():
        for addon_dir in addons_dir.iterdir():
            if addon_dir.is_dir() and not addon_dir.name.startswith("__"):
                for grammar_file in addon_dir.glob("*grammar*.py"):
                    print(f"📦 {addon_dir.name}/{grammar_file.name}")


def test_notepad_grammar():
    """Test the existing notepad grammar"""
    print("\n📝 Testing Notepad Grammar...")
    try:
        sys.path.insert(0, str(project_root / "addons" / "notepad_addon"))
        from notepad_grammar import NotepadGrammar

        grammar = NotepadGrammar()
        grammar.load()

        # Simulate voice command
        print("\n🎤 Simulating 'open notepad' command...")
        grammar.gotResults(["open", "notepad"], None)

    except Exception as e:
        print(f"❌ Error testing notepad grammar: {e}")


if __name__ == "__main__":
    main()
