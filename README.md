# VideoGrabber

A simple tool to download videos from various social media platforms with simplified metadata and browser integration.

## Features

- Downloads videos from YouTube and other platforms supported by yt-dlp
- Creates simplified metadata files with essential information
- Automatically uses browser cookies for authenticated downloads
- Supports multiple browsers (Brave, Chrome, Firefox) and profiles
- Smart retry mechanisms for reliable downloads
- Merges video and audio into MKV format for maximum compatibility
- Handles geo-restricted and age-restricted content (when logged in)
- Browser extension support for direct downloads
- Automatic cleanup of temporary files
- Detailed error reporting and handling

## Installation

```bash
# Install from PyPI (once published)
pip install videograbber

# Or install from source
git clone https://github.com/yourusername/videograbber.git
cd videograbber
pip install -e .

# Install browser extension (optional)
# Follow instructions in extension/README.md
```

## Usage

```bash
# Basic usage (uses default browser - Brave)
videograbber "https://www.youtube.com/watch?v=..."

# Specify a different browser
videograbber "https://www.youtube.com/watch?v=..." --browser chrome

# Specify a browser profile
videograbber "https://www.youtube.com/watch?v=..." --browser brave --profile "Profile 1"

# List available video formats
videograbber "https://www.youtube.com/watch?v=..." --list-formats

# Download specific format
videograbber "https://www.youtube.com/watch?v=..." --format "bestvideo+bestaudio"

# Download with specific browser cookies
videograbber "https://www.youtube.com/watch?v=..." --browser firefox --profile "default"
```

## Output

The tool will create files in the `downloads` directory:
1. The video file (in .mkv format by default)
   - Named as `{title} [{video_id}].mkv`
   - Automatically merges best video and audio quality
2. A simplified .info.json file containing:
   - Title
   - Creator
   - Upload date (in human-readable format, e.g., "January 1, 2024")
   - Duration (in HH:MM:SS format)
   - Resolution (e.g., "1920x1080")
   - View count
   - Original URL

## Requirements

- Python 3.9 or higher
- A supported web browser (Brave, Chrome, Firefox)
- FFmpeg (for video/audio processing)
- Required Python packages (automatically installed):
  - yt-dlp >= 2023.0.0
  - requests >= 2.31.0
  - beautifulsoup4 >= 4.12.0
  - websockets >= 12.0
  - brotli >= 1.1.0
  - mutagen >= 1.47.0
  - pycryptodomex >= 3.19.0

## Browser Extension

The tool includes a browser extension that allows for direct downloads from your browser. See the `extension/` directory for installation instructions.

## Error Handling

The tool provides detailed error messages for common issues:
- Browser cookie access problems
- Network connectivity issues
- Format selection errors
- File system permissions
- Missing dependencies

## Why VideoGrabber?

- **Local Control**: All downloads happen directly on your machine
- **Privacy**: No data passing through third-party servers
- **Browser Integration**: Automatically handles cookies and authentication
- **Clean Metadata**: Simplified, readable metadata files
- **Reliable Downloads**: Smart retry mechanisms and fallbacks
- **Quality Control**: Supports format selection and quality preferences

## License

MIT License

Copyright (c) 2024 VideoGrabber Contributors

This project is licensed under the MIT License - see below for details. Note that while this project uses yt-dlp, which is licensed under the Unlicense (public domain), we have chosen the MIT License for our additional code and modifications.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgments

- This project was developed entirely using [Cursor](https://cursor.sh/), an AI-first IDE
- Built on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp) (Unlicense), the powerful media downloader
- Special thanks to the open-source community for their invaluable tools and libraries 