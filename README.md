# Exam Question Generator UI

This project is a web application that allows users to generate exam questions based on specified parameters such as subject, grade level, and number of questions. It utilizes LLM as a backend service to create questions dynamically and presents them through a user-friendly interface.

## Project Structure

```
exam-question-ui
├── src
│   ├── app.py                # Main application file that sets up the web server and handles user input
│   ├── static
│   |   ├── css
│   |   │   └── styles.css    # CSS styles for the UI
│   |   └── js
│   |       └── scripts.js     # JavaScript for client-side interactivity
│   ├── templates
│   │   └── index.html        # HTML structure for the user interface
│   └── utils                 # Utility scripts for additional functionality
│       ├── claude_test.py    # Test script for Claude AI
│       ├── gemini_test.py    # Test script for Gemini AI
│       ├── mistral_test.py   # Test script for Mistral AI
│       └── openai_test.py    # Test script for OpenAI ChatGPT

├── requirements.txt           # Python dependencies required for the project
└── README.md                  # Documentation for the project
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sdet-tg/ExamQuestionGenerator
   cd ExamQuestionGenerator
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment. You can create one using:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Start the application by running:
   ```bash
   python3 src/app.py
   ```
   The application will be accessible at `http://127.0.0.1:5000`.

## Usage

- Open your web browser and navigate to `http://127.0.0.1:5000`.
- Fill in the form with the desired class, topic, grade level, and number of questions.
- Click the "Generate Questions" button to see the generated exam questions displayed on the page.

### Additional Features

After generating questions, the following options are available:

1. **Select AI Model**:
   - A dropdown menu allows users to choose between "Gemini" and "Mistral" AI models for generating questions.

2. **Print Questions**:
   - A "Print Questions" button appears on the bottom-left corner of the screen.
   - Clicking this button opens a print dialog where the questions are displayed without the correct answers.

3. **Download Questions (HTML)**:
   - A "Download Questions (HTML)" button appears on the bottom-right corner of the screen.
   - Clicking this button downloads an HTML file containing the questions without the correct answers.

## Exporting API Keys

To use the application, you need to set up API keys for the AI models. Follow these steps:

1. **Obtain API Keys**:
   - Sign up for the respective AI services (e.g., OpenAI, Gemini, Mistral) and obtain your API keys.

2. **Set Environment Variables**:
   - Export the API keys as environment variables in your terminal session:
     ```bash
     export GEMINI_API_KEY="your_gemini_api_key"
     export MISTRAL_API_KEY="your_mistral_api_key"
     ```

3. **Persist Environment Variables** (Optional):
   - To make the environment variables persistent, add the export commands to your shell configuration file (e.g., `~/.zshrc` or `~/.bashrc`):
     ```bash
     echo 'export GEMINI_API_KEY="your_gemini_api_key"' >> ~/.zshrc
     echo 'export MISTRAL_API_KEY="your_mistral_api_key"' >> ~/.zshrc
     ```
   - Reload the shell configuration:
     ```bash
     source ~/.zshrc
     ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
