# Voice Command System

A Kivy-based Android application that provides voice command functionality.

## Building the App

This project uses GitHub Actions to automatically build the Android APK. Here's how to get started:

1. Fork this repository to your GitHub account
2. Clone your forked repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Voice-command-system.git
   ```
3. Make your changes to the code
4. Push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
5. Go to your GitHub repository
6. Click on the "Actions" tab
7. Select the "Build Android App" workflow
8. Click "Run workflow"
9. Once the build is complete, you can download the APK from the "Artifacts" section

## Local Development

For local development, you'll need:
- Python 3.9 or higher
- Kivy
- Other dependencies listed in buildozer.spec

Install the dependencies:
```bash
pip install -r requirements.txt
```

## Features

- Voice command recognition
- Contact management
- WhatsApp integration
- Phone call functionality

## Requirements

The app requires the following Android permissions:
- INTERNET
- CALL_PHONE
- READ_CONTACTS
- RECORD_AUDIO

## License

This project is licensed under the MIT License - see the LICENSE file for details. 