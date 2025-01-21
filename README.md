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
- Automatic cleanup of temporary files
- Detailed error reporting and handling

## Prerequisites

Before installing VideoGrabber, make sure you have:

1. Python 3.9 or higher installed
2. FFmpeg installed on your system:
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)
3. A supported web browser (Brave, Chrome, or Firefox)
4. Git (for installation from source)

## Installation

```bash
# Clone the repository
git clone https://github.com/bubroz/videograbber.git
cd videograbber

# Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .
```

## Quick Start

1. Download a video in best quality:
```bash
videograbber "https://www.youtube.com/watch?v=..."
```

2. List available formats for a video:
```bash
videograbber "https://www.youtube.com/watch?v=..." --list-formats
```

3. Download with specific format:
```bash
videograbber "https://www.youtube.com/watch?v=..." --format "137+251"  # 1080p video + high quality audio
```

## Advanced Usage

### Browser Selection and Authentication
```bash
# Use Chrome instead of default Brave
videograbber "https://www.youtube.com/watch?v=..." --browser chrome

# Use specific browser profile (useful for accounts)
videograbber "https://www.youtube.com/watch?v=..." --browser brave --profile "Profile 1"
```

The tool automatically handles authentication by:
1. Extracting cookies from your browser
2. Using them for the download
3. Supporting geo-restricted and age-restricted content
4. Cleaning up cookie files after use

#### Browser Profiles Explained
Browser profiles are separate browser instances with their own:
- Cookies and login sessions
- Bookmarks and history
- Extensions and settings

Each profile has two names:
1. **Display Name**: What you see in the browser UI (e.g., "Work", "Personal")
2. **Directory Name**: The actual folder name on your system (e.g., "Default", "Profile 1")

To see available profiles:
```bash
# List profiles for the default browser (Brave)
videograbber --list-profiles

# List profiles for a specific browser
videograbber --browser chrome --list-profiles
```

Example output:
```
Available brave profiles:
- Display name: 'Default'
  Directory:    'Default'
- Display name: 'Work'
  Directory:    'Profile 1'
- Display name: 'Personal'
  Directory:    'Profile 2'
```

When using the `--profile` option, you can use either:
- The display name: `--profile "Work"`
- The directory name: `--profile "Profile 1"`

Profile locations by OS:
1. **Brave & Chrome**:
   - macOS: `~/Library/Application Support/BraveSoftware/Brave-Browser/`
   - Linux: `~/.config/BraveSoftware/Brave-Browser/`
   - Windows: `%LOCALAPPDATA%\BraveSoftware\Brave-Browser\`

2. **Firefox**:
   - Uses a different profile system with random directory names
   - Profile names are stored in `profiles.ini`
   - Use `--list-profiles` to see available profiles

Tips for using profiles:
- List available profiles first to see the correct names
- The default profile is usually named "Default"
- Renaming a profile in the browser only changes its display name
- The directory name stays the same for compatibility

### Format Selection
- `--list-formats`: Show all available formats
- `--format FORMAT`: Choose specific format
  - `bestvideo+bestaudio`: Best quality (default)
  - `137+251`: 1080p video with high quality audio
  - `136+251`: 720p video with high quality audio
  - `18`: 360p video with audio (single file)

## Output Files

The tool creates two files in the `downloads` directory for each video:

1. Video File: `{title} [{video_id}].mkv`
   - Uses MKV container for maximum compatibility
   - Automatically merges video and audio tracks
   - Example: `My Video [abc123].mkv`

2. Metadata File: `{title} [{video_id}].info.json`
   ```json
   {
     "title": "Video Title",
     "creator": "Channel Name",
     "upload_date": "January 21, 2024",
     "duration": "10:30",
     "resolution": "1920x1080",
     "view_count": 12345,
     "url": "https://www.youtube.com/watch?v=..."
   }
   ```

## Supported Platforms

VideoGrabber supports all platforms that yt-dlp can handle, including:
- YouTube
- Vimeo
- Twitter/X
- Instagram
- Facebook
- TikTok
- And many more!

## Requirements

- Python 3.9 or higher
- FFmpeg
- A supported web browser (Brave, Chrome, Firefox)
- Python packages (automatically installed):
  - yt-dlp >= 2023.0.0
  - requests >= 2.31.0
  - beautifulsoup4 >= 4.12.0
  - websockets >= 12.0
  - brotli >= 1.1.0
  - mutagen >= 1.47.0
  - pycryptodomex >= 3.19.0

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   ```
   Error: FFmpeg not found. Please install FFmpeg first.
   ```
   Solution: Install FFmpeg using your system's package manager.

2. **Browser cookies not accessible**
   ```
   Error: Could not find browser cookies
   ```
   Solution: 
   - Make sure the specified browser is installed
   - Check if you're logged into the site you're downloading from
   - Verify the browser profile path

3. **Format selection error**
   ```
   Error: Requested format not available
   ```
   Solution: Use `--list-formats` to see available formats first

### Best Practices

1. Always use a virtual environment
2. Keep yt-dlp updated: `pip install -U yt-dlp`
3. Use format selection for better quality control
4. Check available formats before downloading

## License

MIT License - See LICENSE file for details.

## Acknowledgments

- Built on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Developed using [Cursor](https://cursor.sh/) 