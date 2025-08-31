# Resume Customizer Tool

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![LaTeX](https://img.shields.io/badge/LaTeX-required-green.svg)
![Gemini AI](https://img.shields.io/badge/Gemini-AI%20Powered-orange.svg)

An intelligent resume customization tool that uses Google's Gemini AI to automatically tailor your LaTeX resume for specific job applications. Simply provide a job description, and the tool will analyze your resume content and optimize it to highlight relevant skills and experiences while maintaining your professional formatting.

## 🚀 Features

- **🤖 AI-Powered Customization**: Uses Gemini AI to intelligently match your resume to job requirements
- **📝 LaTeX Support**: Works with your existing `.tex` and `.cls` resume files
- **🎯 Smart Optimization**: Highlights relevant skills and reorders content for maximum impact  
- **📋 PDF Generation**: Automatically compiles customized resumes to professional PDFs
- **🗂️ Organized Output**: Saves files with timestamps and job titles for easy management
- **⚡ Multiple Input Methods**: Job descriptions via text file or direct input
- **🔧 Easy Setup**: Automated installation and configuration scripts

## Features

- 📝 **Flexible Input**: Job descriptions via direct text or text file
- 🤖 **AI-Powered**: Uses Gemini AI to intelligently customize your resume
- 📄 **LaTeX Support**: Works with your existing `.tex` and `.cls` files
- 🎯 **Smart Matching**: Highlights relevant skills and experiences for each job
- 📋 **PDF Generation**: Automatically compiles customized resume to PDF
- 🗂️ **Organized Output**: Saves files with timestamps and job titles

## Setup

### 1. Install Dependencies & Set Up Environment

Run the setup script to install LaTeX and configure the API key:
```bash
./setup_api_key.sh
```

Or manually:
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install LaTeX
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended

# Set your Gemini API key
export GEMINI_API_KEY="your_api_key_here"
```

### 2. Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account  
3. Click "Create API Key"
4. Copy the generated key

### 3. Your Resume Files Are Ready!

✅ Your `resume.tex` and `resume.cls` files are already in the `templates/` directory
✅ Your job description is in `job_description.txt`

## Quick Start

### Test with Your Actual Job Description
```bash
# Set up API key (one time only)
./setup_api_key.sh

# Run the demo with your ExxonMobil job description
python demo.py
```

### Create New Job Description Files
```bash
# Interactive job description creator
python quick_job.py

# Or manually create a .txt file in job_descriptions/ folder
```

### Customize Resume for Any Job

The tool is now fully configurable through configuration files:

```bash
# Show current configuration
python resume_customizer.py --show-config

# Use custom configuration directory
python resume_customizer.py --config-dir /path/to/config --job-file job.txt

# Use specific AI model
python resume_customizer.py --model gemini-1.5-pro --job-file job.txt

# Using your existing job_description.txt
python resume_customizer.py --job-file job_description.txt --job-title "ExxonMobil Software Engineer"

# Using a different job file
python resume_customizer.py --job-file job_descriptions/another_job.txt --job-title "Job Title"

# Direct text input (for quick tests)
python resume_customizer.py --job-description "Your job description text here" --job-title "Job Title"
```

## Configuration Management

The tool uses a flexible configuration system for better maintainability:

### Configuration Files
- `config.ini`: Main configuration settings (AI model, paths, LaTeX settings, output preferences)
- `prompts.ini`: AI prompt templates and customization instructions

### Configuration Tool
Use the included configuration utility to manage settings:

```bash
# Show current configuration
python config_tool.py show

# Set a configuration value
python config_tool.py set ai.model gemini-1.5-pro

# Show available models
python config_tool.py models

# Validate configuration
python config_tool.py validate

# Reset to defaults
python config_tool.py reset

# Show current prompt template
python config_tool.py prompt

# Edit prompt section
python config_tool.py edit-prompt customization focus_areas "technical skills, project experience, leadership"
```

## Project Structure

```
resume_io/
├── resume_customizer.py          # Main application
├── config_manager.py             # Configuration management system
├── config_tool.py                # Configuration utility
├── config.ini                    # Main configuration settings
├── prompts.ini                   # AI prompt templates
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .env.example                  # Environment variables template
├── templates/                    # Your resume template files
│   ├── resume.tex               # Your LaTeX resume (you provide)
│   └── resume.cls               # Your LaTeX class file (you provide)
├── job_descriptions/            # Store job description text files
│   └── example_job.txt          # Example job description file
└── output/                      # Generated customized resumes
    ├── resume_Frontend_Developer_20250831_143022.tex
    ├── resume_Frontend_Developer_20250831_143022.pdf
    └── resume.cls               # Copied class file for compilation
```

## Command Line Options

- `--job-description, -d`: Job description as direct text input
- `--job-file, -f`: Path to text file containing job description  
- `--job-title, -t`: Job title for better file naming (optional)
- `--api-key, -k`: Gemini API key (optional if set as environment variable)
- `--config-dir`: Custom configuration directory (optional)
- `--show-config`: Display current configuration settings
- `--model`: Override AI model for this run (optional)

## Examples

### Example 1: Tech Job
```bash
python resume_customizer.py \
  --job-file job_descriptions/senior_python_dev.txt \
  --job-title "Senior Python Developer"
```

### Example 2: Marketing Role
```bash
python resume_customizer.py \
  --job-description "Marketing Manager position focusing on digital marketing, social media strategy, and data analytics. Requires 3+ years experience in marketing automation tools." \
  --job-title "Marketing Manager"
```

## Troubleshooting

### LaTeX Compilation Issues
- Ensure all required LaTeX packages are installed
- Check that your `resume.cls` file doesn't have syntax errors
- Review the compilation logs in the output directory

### API Issues
- Verify your Gemini API key is correct and active
- Check your internet connection
- Ensure you haven't exceeded API rate limits

### File Path Issues
- Use absolute paths if having issues with relative paths
- Ensure all template files exist in the `templates/` directory

## Tips

1. **Job Description Files**: Save job descriptions in the `job_descriptions/` folder for easy reuse
2. **Backup**: Keep a backup of your original resume template
3. **Review**: Always review the AI-generated content before using
4. **Iterate**: You can run the tool multiple times with different prompts for the same job

## License

MIT License - Feel free to modify and distribute as needed.
