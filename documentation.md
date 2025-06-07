# AI-Powered PowerPoint Generator Documentation

## Overview

The AI-Powered PowerPoint Generator is a Python-based tool designed to automatically create visually appealing presentations using AI-generated content, smart layouts, and automatic image selection. This document provides a comprehensive guide to the project's architecture, features, and usage.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
   - [Command Line Interface](#command-line-interface)
   - [Interactive GUI](#interactive-gui)
5. [Features](#features)
   - [AI-Powered Content Generation](#ai-powered-content-generation)
   - [Multiple Presentation Styles](#multiple-presentation-styles)
   - [Smart Layouts](#smart-layouts)
   - [Automatic Image Selection](#automatic-image-selection)
   - [Data Visualization](#data-visualization)
6. [Development](#development)
   - [Code Structure](#code-structure)
   - [Adding New Features](#adding-new-features)
   - [Testing](#testing)
7. [Contributing](#contributing)
8. [Acknowledgments](#acknowledgments)

## Project Structure

The project is organized as follows:

```
Ppt_generator/
├── assets/          # Static assets like images and icons
├── downloads/       # Temporary storage for downloaded images
├── fonts/           # Custom fonts used in presentations
├── orchestration/   # Core logic for presentation generation
├── output/          # Generated presentations
├── templates/       # PowerPoint templates
├── tests/           # Unit and integration tests
├── config.py        # Configuration settings
├── main.py          # Entry point for the application
├── requirements.txt # Python dependencies
└── README.md        # Project overview and setup instructions
```

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/Ppt_generator.git
   cd Ppt_generator
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python3.9 -m venv venv_py39
   source venv_py39/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tkinter (for GUI):**
   On Ubuntu, run:
   ```bash
   sudo apt-get install python3.9-tk
   ```

## Configuration

The `config.py` file contains configuration settings for the project, including API keys and default settings. Ensure you have the necessary API keys for services like OpenAI and Pexels.

## Usage

### Command Line Interface

To generate a presentation using the command line, run:

```bash
python main.py --topic "Your Topic" --style dark --slides 5
```

Options:
- `--topic`: Presentation topic
- `--style`: Presentation style (dark or light)
- `--slides`: Number of slides
- `--output`: Specify custom output directory
- `--template`: Use a custom PowerPoint template

### Interactive GUI

The project includes an interactive GUI built with tkinter. To use it, ensure you have tkinter installed for your Python version. Then, activate your virtual environment and run:

```bash
python presentation_gui.py
```

This GUI allows you to input the presentation title, number of slides, and style, and then generate your presentation with a single click.

## Features

### AI-Powered Content Generation

The tool uses AI to generate presentation content, ensuring that the text is relevant and engaging.

### Multiple Presentation Styles

Choose between dark and light styles to suit your presentation needs.

### Smart Layouts

The tool automatically arranges content and images in a visually appealing manner.

### Automatic Image Selection

Images are automatically selected and downloaded from Pexels based on the presentation content.

### Data Visualization

The tool can generate diagrams and charts to visualize data.

## Development

### Code Structure

The core logic for presentation generation is located in the `orchestration/` directory. The `visual_engine.py` file contains functions for creating presentations, while `main.py` serves as the entry point.

### Adding New Features

To add new features, follow these steps:
1. Identify the area of the codebase where the feature should be implemented.
2. Write the necessary code and tests.
3. Update the documentation to reflect the new feature.

### Testing

Run tests using:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes.
4. Push to the branch.
5. Create a Pull Request.

## Acknowledgments

- OpenAI for AI content generation.
- Pexels for image resources.
- python-pptx for PowerPoint generation. 