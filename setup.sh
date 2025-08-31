#!/bin/bash

# Setup script for Resume Customizer Tool

echo "🚀 Setting up Resume Customizer Tool..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if LaTeX is installed
if ! command -v pdflatex &> /dev/null; then
    echo "⚠️  LaTeX (pdflatex) is not installed."
    echo "📚 To install LaTeX:"
    echo "   Ubuntu/Debian: sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended"
    echo "   macOS: brew install --cask mactex"
    echo "   Windows: Download MiKTeX from https://miktex.org/"
    echo ""
    echo "❓ Do you want to install LaTeX now? (Ubuntu/Debian only) [y/N]"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        sudo apt-get update && sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
    fi
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✏️  Please edit .env file and add your Gemini API key"
fi

# Make scripts executable
chmod +x resume_customizer.py
chmod +x create_job_file.py

echo ""
echo "✅ Setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Get your Gemini API key from: https://makersuite.google.com/app/apikey"
echo "2. Add your API key to .env file OR set GEMINI_API_KEY environment variable"
echo "3. Replace templates/resume.tex with your actual resume"
echo "4. Replace templates/resume.cls with your actual class file (if you have one)"
echo "5. Test the tool:"
echo "   python3 resume_customizer.py --job-file job_descriptions/example_fullstack_job.txt --job-title \"Full Stack Engineer\""
echo ""
echo "📖 For more information, see README.md"
