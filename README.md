
# On-Screen Smart Assistant for Solving Question Papers

## Overview

This application is an on-screen smart assistant designed to take screenshots of question papers and generate responses using LLM. The tool allows users to easily capture questions and receive solutions, making it a handy utility for students and professionals alike.

## Features

- **Floating Button:** A floating round window that can be dragged around the screen for easy access.
- **Screenshot Capture:** Capture screenshots of the entire screen and display them in a separate window.
- **Response Generation:** Send the captured screenshot to the LLM to generate answers to the questions in the image.
- **User-Friendly Interface:** Simple and intuitive interface for capturing screenshots and generating responses.
- **Close Functionality:** Easily close the response and screenshot windows.

## Requirements

- Python 3.x
- Tkinter
- Pillow (PIL)
- Google Generative AI SDK
- Python-dotenv

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/on-screen-smart-assistant.git
   cd on-screen-smart-assistant
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory and add your Google Generative AI API key:
   ```plaintext
   API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. A floating button will appear on your screen. Click on it to capture a screenshot of the question paper.
3. After capturing, a new window will open showing the screenshot along with a button to generate responses.
4. Click on "Generate Response" to send the screenshot to the AI for analysis and receive answers.
5. Close the screenshot and response windows as needed.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Google Generative AI API for providing the AI capabilities.
- Pillow for image processing.
- Tkinter for GUI development.
