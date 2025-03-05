import sys
import subprocess
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QComboBox, QPushButton

# Function to run DeepSeek and get the response with timeout
def get_deepseek_response(text):
    try:
        # Adjusted input prompt to encourage text enhancement
        prompt = f"Improve the following sentence: '{text}'"
        
        # Run the Ollama DeepSeek model with a timeout (e.g., 10 seconds)
        result = subprocess.run(
    ['ollama', 'run', 'deepseek-r1', prompt],
    capture_output=True, text=True, timeout=30  # Increased timeout to 30 seconds
)
        
        if result.returncode == 0:
            # Clean the response to remove <think> tags and everything inside them
            cleaned_response = clean_deepseek_output(result.stdout.strip())
            return cleaned_response
        else:
            return f"Error: {result.stderr.strip()} 😕"
    except subprocess.TimeoutExpired:
        return "Error: DeepSeek took too long to respond. ⏳"
    except Exception as e:
        return f"Error: {e} 😔"

# Function to clean the DeepSeek output
def clean_deepseek_output(text):
    # Remove everything inside the <think> tags, not just the tags themselves
    cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    # Return cleaned response
    return cleaned_text

# Main Window Setup using PyQt5
class SpeechImproverApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Echo++: AI Language Coach 🤖")
        self.setGeometry(100, 100, 600, 500)

        # Layout
        layout = QVBoxLayout(self)

        # Input Text Label and Text Box
        self.input_label = QLabel("Enter your sentence:", self)
        layout.addWidget(self.input_label)

        self.input_text = QTextEdit(self)
        self.input_text.setFixedHeight(100)  # Size the input box
        layout.addWidget(self.input_text)

        # Enhance Button
        self.enhance_button = QPushButton("Enhance Text ✨", self)
        self.enhance_button.clicked.connect(self.enhance_text)
        layout.addWidget(self.enhance_button)

        # Output Text Label and Text Box
        self.output_label = QLabel("Improved Sentence:", self)
        layout.addWidget(self.output_label)

        self.output_text = QTextEdit(self)
        self.output_text.setFixedHeight(100)  # Size the output box
        self.output_text.setReadOnly(True)  # Make it read-only
        layout.addWidget(self.output_text)

        # Set the layout of the window
        self.setLayout(layout)

    def enhance_text(self):
        user_input = self.input_text.toPlainText().strip()
        if not user_input:
            self.output_text.setPlainText("Please enter some text. ✨")
            return
        
        # Get DeepSeek response
        deepseek_response = get_deepseek_response(user_input)
        
        # Display the response in the output box
        self.output_text.setPlainText(deepseek_response)

# Running the application
def main():
    app = QApplication(sys.argv)
    window = SpeechImproverApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()