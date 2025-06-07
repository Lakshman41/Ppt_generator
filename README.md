# AI-Powered PowerPoint Generator

An intelligent PowerPoint presentation generator that creates visually appealing presentations with AI-generated content, relevant images, and professional layouts.

## Features

- 🤖 AI-powered content generation
- 🎨 Multiple presentation styles (dark/light themes)
- 📊 Smart layouts with diagrams and charts
- 🖼️ Automatic image selection and optimization
- 📝 Table of contents generation
- 🎯 Supporting images for each slide
- 📈 Data visualization capabilities

## Project Structure

```
Ppt_generator/
├── assets/              # Static assets and resources
├── downloads/           # Temporary storage for downloaded images
├── fonts/              # Custom fonts for presentations
├── orchestration/      # Core presentation generation logic
├── output/            # Generated presentations
├── templates/         # PowerPoint templates
├── tests/            # Test files
├── venv_py39/        # Python virtual environment
├── config.py         # Configuration settings
├── main.py           # Main entry point
├── requirements.txt  # Python dependencies
└── utils.py          # Utility functions
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Ppt_generator.git
cd Ppt_generator
```

2. Create and activate a virtual environment:
```bash
python3.9 -m venv venv_py39
source venv_py39/bin/activate  # On Linux/Mac
# or
.\venv_py39\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with your API keys:
```
DEEPSEEK_API_KEY=your_deepseek_api_key
GEMINI_API_KEY=your_gemini_api_key
PEXELS_API_KEY=your_pexels_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Usage

Generate a presentation with a specific topic and style:

```bash
python main.py "Your Topic" --style dark
```

Available options:
- `--style`: Choose between 'dark' or 'light' theme
- `--output`: Specify custom output directory
- `--template`: Use a custom PowerPoint template

## Interactive GUI

The project now includes an interactive GUI built with tkinter. To use it, ensure you have tkinter installed for your Python version (e.g., on Ubuntu, run `sudo apt-get install python3.9-tk` for Python 3.9). Then, activate your virtual environment and run:

```bash
python presentation_gui.py
```

This GUI allows you to input the presentation title, number of slides, and style, and then generate your presentation with a single click.

## Development

### Key Components

- `orchestration/`: Contains the main presentation generation logic
  - `visual_engine.py`: Handles slide layouts and visual elements
  - `image_engine.py`: Manages image processing and optimization
  - `gemini_client.py`: AI content generation integration

### Adding New Features

1. Create a new branch for your feature
2. Implement changes following the existing code structure
3. Add tests in the `tests/` directory
4. Submit a pull request

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for AI content generation
- Pexels for image resources
- python-pptx for PowerPoint generation