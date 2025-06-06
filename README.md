# Smart PPT Generator

![Project Status](https://img.shields.io/badge/status-in%20development-yellow)

A powerful, streamlined Python tool that automatically generates professional-quality PowerPoint presentations from a single topic. This project leverages Large Language Models (LLMs) for intelligent content structuring and high-quality stock photo APIs for stunning visuals.

The core philosophy is **quality over quantity**—creating fewer, more impactful slides with premium visuals and compelling narratives.

## Core Features (Current)

- **AI-Powered Content:** Utilizes the DeepSeek API to generate a structured and logical slide outline based on a user-provided topic.
- **Automated Visuals:** Fetches high-quality, relevant, landscape-oriented images from the Pexels API to serve as full-bleed slide backgrounds.
- **Professional Formatting:** Assembles the content and images into a clean, 16:9 widescreen `.pptx` file with readable titles.
- **Efficient Caching:** Caches downloaded images to speed up subsequent runs and reduce API calls.

## Setup & Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

- Python 3.9+
- A virtual environment (recommended)

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/smart-ppt-generator.git
cd smart-ppt-generator
```
### 3. Set Up a Virtual Environment

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
Install all the required Python packages from the requirements.txt file.
pip install -r requirements.txt
```
### 5. Configure API Keys

The application requires API keys for DeepSeek (content generation) and Pexels (image search).
Find the .env.example file in the root directory and rename it to .env.
Open the .env file and add your personal API keys:

```bash
# Get your DeepSeek API key from: https://platform.deepseek.com/api_keys
DEEPSEEK_API_KEY="your_deepseek_api_key"

# Get your Pexels API key from: https://www.pexels.com/api/
PEXELS_API_KEY="your_pexels_api_key"
```

## How to Use

Run the script from your terminal using the `main.py` entry point. Provide the desired presentation topic, and optionally specify the number of slides and a visual style.

### Basic Usage

```bash
python main.py "The Evolution of Artificial Intelligence"
```

### Advanced Usage

## Specify Slide Count:
Use the --slides flag to control the number of content slides.

```bash
python main.py "The History of Ancient Rome" --slides 8
```
## Specify Visual Style:
Use the --style flag to choose a theme. Options are dark (default), light, and corporate.

```bash
python main.py "Principles of Graphic Design" --style light
```

## Combine Options:

```bash
python main.py "The Future of Renewable Energy" --slides 6 --style corporate
```

### Future Development

This is the foundational version of the project. Future enhancements will include:

AI-powered selection of the best image from multiple candidates.
Support for more slide layouts and visual styles.
Advanced content generation for speaker notes and transition text.
Robust error handling and fallback mechanisms.