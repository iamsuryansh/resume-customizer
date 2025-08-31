#!/bin/bash

# Quick setup script to set environment variable and test the tool

echo "🔑 Resume Customizer - API Key Setup"
echo "=================================="
echo ""
echo "To get your Gemini API key:"
echo "1. Go to: https://makersuite.google.com/app/apikey"
echo "2. Sign in with your Google account"
echo "3. Click 'Create API Key'"
echo "4. Copy the generated key"
echo ""
echo -n "Please paste your Gemini API key: "
read -r api_key

if [ -z "$api_key" ]; then
    echo "❌ No API key provided"
    exit 1
fi

# Set the environment variable for this session
export GEMINI_API_KEY="$api_key"

# Add to .bashrc for future sessions
echo "export GEMINI_API_KEY=\"$api_key\"" >> ~/.bashrc

echo "✅ API key set successfully!"
echo ""
echo "🧪 Running setup test..."
/home/mawzir/Desktop/Demo/resume_io/.venv/bin/python test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Ready to test! Try running:"
    echo "python resume_customizer.py --job-file job_description.txt --job-title 'ExxonMobil Software Engineer'"
fi
