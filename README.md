# 🎨 AI-Powered PowerPoint Generator

**Created by LAKSHMAN SINGH**

An intelligent PowerPoint presentation generator that creates visually appealing presentations with AI-generated content, relevant images, and professional layouts. Transform your ideas into stunning presentations in minutes!

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- 🤖 **AI-powered content generation** - Intelligent slide creation with relevant content
- 🎨 **Multiple presentation styles** - Dark/light themes with professional layouts
- 📊 **Smart layouts with diagrams** - Automatic layout selection based on content
- 🖼️ **Automatic image selection** - Contextual background and supporting images
- 📝 **Table of contents generation** - Structured presentation flow
- 🎯 **Supporting images for each slide** - Visual enhancement for better engagement
- 📈 **Data visualization capabilities** - Charts and graphs integration
- 🌐 **Web-based interface** - Modern Streamlit GUI for easy access
- 💻 **Command-line interface** - Traditional CLI for automation
- 🖥️ **Desktop GUI** - Tkinter-based interface for offline use

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)
```bash
# Install Streamlit dependencies
pip install streamlit python-dotenv

# Run the web app
streamlit run streamlit_app.py
```
Access the beautiful web interface at `http://localhost:8501`

### Option 2: Command Line
```bash
python main.py "Your Topic" --slides 6 --style dark
```

### Option 3: Desktop GUI
```bash
python presentation_gui.py
```

## 🏗️ Project Structure

```
Ppt_generator/
├── 📁 assets/              # Static assets and resources
├── 📁 downloads/           # Temporary storage for downloaded images
├── 📁 fonts/              # Custom fonts for presentations
├── 📁 orchestration/      # Core presentation generation logic
│   ├── content_engine.py  # AI content generation
│   ├── visual_engine.py   # Slide layouts and visual elements
│   ├── image_engine.py    # Image processing and optimization
│   └── gemini_client.py   # AI integration
├── 📁 output/            # Generated presentations
├── 📁 templates/         # PowerPoint templates
├── 📁 tests/            # Test files
├── 📁 venv_py39/        # Python virtual environment
├── 📄 config.py         # Configuration settings
├── 📄 main.py           # CLI entry point
├── 📄 streamlit_app.py  # Web interface
├── 📄 presentation_gui.py # Desktop GUI
├── 📄 requirements.txt  # Python dependencies
├── 📄 utils.py          # Utility functions
└── 📄 .env              # Environment variables
```

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Ppt_generator.git
cd Ppt_generator
```

### 2. Set Up Virtual Environment
```bash
python3.9 -m venv venv_py39
source venv_py39/bin/activate  # On Linux/Mac
# or
.\venv_py39\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt

# For Streamlit web interface
pip install streamlit python-dotenv

# For desktop GUI (Ubuntu/Debian)
sudo apt-get install python3.9-tk
```

### 4. Configure API Keys
Create a `.env` file in the root directory:
```env
DEEPSEEK_API_KEY=your_deepseek_api_key
GEMINI_API_KEY=your_gemini_api_key
PEXELS_API_KEY=your_pexels_api_key
OPENAI_API_KEY=your_openai_api_key
```

#### 🔑 Getting API Keys:
- **Gemini API**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Pexels API**: [Pexels API](https://www.pexels.com/api/)
- **OpenAI API**: [OpenAI Platform](https://platform.openai.com/api-keys)
- **DeepSeek API**: [DeepSeek Platform](https://platform.deepseek.com/)

## 📖 Usage Guide

### 🌐 Streamlit Web Interface (Recommended)

The most user-friendly way to use the generator:

1. **Launch the web app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Features of the web interface:**
   - ✨ Beautiful, modern UI with gradient themes
   - 📊 Interactive sliders for slide count (3-15 slides)
   - 🎨 Style selector (dark/light themes)
   - 📈 Real-time progress tracking
   - ⬇️ Direct download functionality
   - 🎯 Sample topics for quick testing
   - 📱 Responsive design for all devices

3. **How to use:**
   - Enter your presentation topic
   - Select number of slides (3-15)
   - Choose your preferred style
   - Click "Generate Presentation"
   - Download your finished presentation!

### 💻 Command Line Interface

For automation and scripting:

```bash
# Basic usage
python main.py "Artificial Intelligence in Healthcare"

# With custom options
python main.py "Climate Change Solutions" --slides 10 --style light

# Available options
python main.py --help
```

**Parameters:**
- `topic`: The main topic of your presentation (required)
- `--slides`: Number of slides (default: 6, range: 3-15)
- `--style`: Presentation style ('dark' or 'light', default: 'dark')

### 🖥️ Desktop GUI

For offline use with a traditional desktop interface:

```bash
python presentation_gui.py
```

**Features:**
- Simple form-based interface
- Dropdown menus for options
- Progress indicators
- File save dialogs

## 🎯 Example Topics

Try these sample topics to see the generator in action:

- 📊 "Digital Marketing Strategies 2024"
- 🌍 "Climate Change Solutions"
- 🤖 "Machine Learning Fundamentals"
- 📈 "Project Management Best Practices"
- 💰 "Cryptocurrency and Blockchain"
- 🏠 "Remote Work Productivity"
- 🏥 "Healthcare Technology Innovations"
- 🎓 "Future of Education"

## 🔧 Development

### Key Components

#### Core Engines
- **`orchestration/content_engine.py`**: AI-powered content generation and slide structuring
- **`orchestration/visual_engine.py`**: Layout selection and visual design management
- **`orchestration/image_engine.py`**: Image search, download, and optimization
- **`orchestration/gemini_client.py`**: AI model integration and API management

#### User Interfaces
- **`streamlit_app.py`**: Modern web interface with real-time feedback
- **`presentation_gui.py`**: Desktop GUI using tkinter
- **`main.py`**: Command-line interface for automation

### Adding New Features

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow the existing architecture:**
   - Add new engines to `orchestration/`
   - Update interfaces as needed
   - Add comprehensive error handling

3. **Add tests:**
   ```bash
   # Add tests to tests/ directory
   python -m pytest tests/
   ```

4. **Submit a pull request**

### 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### 🐛 Bug Reports

Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)

### 💡 Feature Requests

Have an idea? We'd love to hear it! Open an issue with:
- Clear description of the feature
- Use case examples
- Possible implementation ideas

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for AI content generation capabilities
- **Google Gemini** for advanced language model integration
- **Pexels** for high-quality stock images
- **python-pptx** for PowerPoint generation functionality
- **Streamlit** for the beautiful web interface framework
- **The open-source community** for inspiration and tools

## 📞 Contact

**Lakshman Singh** - Creator and Maintainer

- 📧 Email: [your.email@example.com]
- 🐙 GitHub: [@yourusername]
- 💼 LinkedIn: [Your LinkedIn Profile]

---

### 🌟 Star this repository if you found it helpful!

**Made with ❤️ by Lakshman Singh**