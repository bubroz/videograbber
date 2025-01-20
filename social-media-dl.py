import subprocess
import json
import os
import tempfile
import time  # Add import for time.sleep
from pathlib import Path
from typing import Optional, Dict, List, Union
from dataclasses import dataclass
from datetime import datetime
import argparse

@dataclass
class DownloadResult:
    success: bool
    file_path: Optional[Path]
    error: Optional[str]
    metadata: Optional[Dict]

def format_duration(duration_secs):
    """Convert seconds to HH:MM:SS format"""
    if not duration_secs:
        return "Unknown"
    hours = int(duration_secs // 3600)
    minutes = int((duration_secs % 3600) // 60)
    seconds = int(duration_secs % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"

def format_date(date_str):
    """Format date string to be more readable"""
    if not date_str:
        return "Unknown"
    try:
        date = datetime.strptime(date_str, "%Y%m%d")
        return date.strftime("%B %d, %Y")
    except:
        return date_str

class SocialMediaDL:
    def __init__(
        self,
        output_dir: str = "~/Downloads/social_media",
        cookies_file: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        self.output_dir = Path(output_dir).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cookies_file = Path(cookies_file).expanduser() if cookies_file else None
        self.username = username
        self.password = password
        self._temp_dir = None

    def __enter__(self):
        """Context manager entry to create temp directory"""
        self._temp_dir = tempfile.mkdtemp()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit to cleanup temp files"""
        if self._temp_dir and os.path.exists(self._temp_dir):
            # Clean up any cookie files
            for file in Path(self._temp_dir).glob("*.txt"):
                try:
                    file.unlink()
                except:
                    pass
            try:
                os.rmdir(self._temp_dir)
            except:
                pass

    def _build_auth_args(self) -> List[str]:
        """Build authentication arguments for yt-dlp"""
        args = []
        if self.cookies_file and self.cookies_file.exists():
            args.extend(["--cookies", str(self.cookies_file)])
        if self.username and self.password:
            args.extend(["--username", self.username, "--password", self.password])
        return args

    def _run_command(self, command: List[str]) -> subprocess.CompletedProcess:
        """Run a yt-dlp command and handle output"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False  # Don't raise exception, we'll handle errors
            )
            return result
        except Exception as e:
            raise Exception(f"Command execution failed: {str(e)}")

    def export_browser_cookies(self, url: str, browser: str = "brave", profile: Optional[str] = None) -> Path:
        """
        Export cookies from browser to a file using best practices from yt-dlp documentation
        
        Args:
            url: URL of the site to validate cookies against
            browser: Browser to export from (default is 'brave')
            profile: Browser profile to use (e.g. 'Profile 1', 'Default', etc.)
        """
        if not self._temp_dir:
            self._temp_dir = tempfile.mkdtemp()
            
        cookies_path = Path(self._temp_dir) / f"cookies_{browser}.txt"
        
        # Handle browser paths and profiles
        browser_spec = browser
        if browser == "brave":
            base_path = "~/Library/Application Support/BraveSoftware/Brave-Browser"
            if profile:
                browser_spec = f"brave:{base_path}/{profile}"
            elif os.path.exists(os.path.expanduser(f"{base_path}/Default")):
                browser_spec = f"brave:{base_path}/Default"
            else:
                browser_spec = f"brave:{base_path}"
            print(f"Using browser at: {browser_spec}")
        
        # Use a modern macOS Brave user agent
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        # Export cookies without domain filter to support all sites
        command = [
            "yt-dlp",
            "--cookies-from-browser",
            browser_spec,  # No domain filter - get all cookies
            "--user-agent",
            user_agent,
            "--cookies",
            str(cookies_path),
            "--skip-download",
            url  # Use the target URL for validation
        ]
        
        result = self._run_command(command)
        if result.returncode != 0:
            print(f"Cookie export error output: {result.stderr}")
            if "could not find" in result.stderr:
                raise Exception(f"Could not find browser cookies. Please make sure:\n"
                              f"1. You have {browser} browser installed\n"
                              f"2. You're logged into the site you're trying to download from\n"
                              f"3. Your browser profile path is correct: {browser_spec}")
            raise Exception(f"Failed to export cookies: {result.stderr}")
            
        if not cookies_path.exists():
            raise Exception("Cookies file was not created")
            
        return cookies_path

    def download_video(
        self,
        url: str,
        browser: str = "brave",
        profile: str = None,
        format: str = "bestvideo+bestaudio/best",
        metadata_only: bool = False
    ) -> DownloadResult:
        """
        Download a video from a supported platform using yt-dlp.
        
        Args:
            url (str): The URL of the video to download
            browser (str): The browser to export cookies from (default: brave)
            profile (str): The browser profile to use (default: None)
            format (str): The format to download (default: bestvideo+bestaudio/best)
            metadata_only (bool): Whether to only download metadata (default: False)
        """
        try:
            # Export browser cookies
            cookies_file = self.export_browser_cookies(url, browser, profile)
            
            # Prepare output directory - now relative to the project directory
            output_dir = Path("downloads")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Build yt-dlp command
            command = ["yt-dlp"]
            if cookies_file:
                command.extend(["--cookies", str(cookies_file)])
            
            # Create a temporary file for the full metadata
            temp_info_json = Path(self._temp_dir) / "temp_info.json"
            
            # Add output template and other options
            command.extend([
                "-o", str(output_dir / "%(title)s [%(id)s].%(ext)s"),
                "-f", format,  # Use specified format
                "--write-info-json",
                "--print-json",  # Print JSON to stdout for immediate access
                "--merge-output-format", "mkv",  # Merge into MKV to support any codec combination
                "--no-check-certificate",
                "--geo-bypass",
                "--no-playlist",
                "--no-cache-dir",
                "--force-ipv4",
                "--retries", "10",
                "--file-access-retries", "10",
                "--fragment-retries", "10",
                "--retry-sleep", "3",
                "--progress",
                "--newline",
                "--verbose",
                "--ignore-errors",
                "--no-warnings",
                "--prefer-insecure",
                url  # Add URL at the end
            ])
            
            # Run the command
            print("Running download command:", " ".join(command))
            result = self._run_command(command)
            
            if result.returncode != 0:
                print(f"Download error output: {result.stderr}")
                return DownloadResult(
                    success=False,
                    file_path=None,
                    error=result.stderr,
                    metadata=None
                )
            
            # Try to parse the JSON output for metadata
            try:
                # Find the JSON line in the output
                json_lines = [line for line in result.stdout.split('\n') if line.strip().startswith('{')]
                if not json_lines:
                    raise Exception("No JSON data found in output")
                    
                full_metadata = json.loads(json_lines[-1])  # Use the last JSON line
                
                # Extract only the essential information
                simplified_metadata = {
                    "title": full_metadata.get("title", "Unknown"),
                    "creator": full_metadata.get("uploader", "Unknown"),
                    "upload_date": format_date(full_metadata.get("upload_date")),
                    "duration": format_duration(full_metadata.get("duration")),
                    "resolution": f"{full_metadata.get('width', '?')}x{full_metadata.get('height', '?')}",
                    "view_count": full_metadata.get("view_count", "Unknown"),
                    "url": full_metadata.get("webpage_url", "Unknown")
                }
                
                # Save simplified metadata
                video_id = full_metadata.get("id", "unknown")
                info_json_path = output_dir / f"{full_metadata['title']} [{video_id}].info.json"
                with open(info_json_path, 'w', encoding='utf-8') as f:
                    json.dump(simplified_metadata, f, indent=2, ensure_ascii=False)
                
                # Find the media file
                if not metadata_only:
                    # Give the filesystem a moment to sync
                    time.sleep(0.5)
                    
                    # Try to find the video file
                    video_files = list(output_dir.glob(f"*[{video_id}].*"))
                    video_files = [f for f in video_files if f.suffix.lower() in ['.mkv', '.mp4', '.webm']]
                    
                    if video_files:
                        video_path = video_files[0]
                        # Check if file existed before this run by comparing modification time
                        file_existed = (time.time() - video_path.stat().st_mtime) > 5
                        if file_existed:
                            print(f"File already exists: {video_path}")
                        else:
                            print(f"Downloaded to: {video_path}")
                        print(f"Creator: {simplified_metadata['creator']}")
                        return DownloadResult(
                            success=True,
                            file_path=video_path,
                            error=None,
                            metadata=simplified_metadata
                        )
                    else:
                        # Just list the files without warnings
                        all_files = list(output_dir.glob("*"))
                        video_files = [f for f in all_files if f.suffix.lower() in ['.mkv', '.mp4', '.webm']]
                        if video_files:
                            print(f"File location: {video_files[0]}")
                            print(f"Creator: {simplified_metadata['creator']}")
                            return DownloadResult(
                                success=True,
                                file_path=video_files[0],
                                error=None,
                                metadata=simplified_metadata
                            )
                
                return DownloadResult(
                    success=True,
                    file_path=None,
                    error=None,
                    metadata=simplified_metadata
                )
                
            except Exception as e:
                print(f"Error processing metadata: {e}")
                return DownloadResult(
                    success=False,
                    file_path=None,
                    error=str(e),
                    metadata=None
                )
                
        except Exception as e:
            print(f"Error: {e}")
            return DownloadResult(
                success=False,
                file_path=None,
                error=str(e),
                metadata=None
            )

    def list_formats(self, url: str) -> None:
        """
        List all available formats for a video URL
        
        Args:
            url: Video URL to check formats for
        """
        command = [
            "yt-dlp",
            "--list-formats",  # Show all available formats
            "--no-warnings",
            url
        ]
        
        result = self._run_command(command)
        if result.returncode == 0:
            print("\nAvailable formats:")
            print(result.stdout)
        else:
            raise Exception(f"Failed to list formats: {result.stderr}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Download videos from sites supported by yt-dlp')
    parser.add_argument('url', help='URL of the video to download')
    parser.add_argument('--browser', default='brave', help='Browser to export cookies from (default: brave)')
    parser.add_argument('--profile', help='Browser profile to use (e.g. "Profile 1", "Default")')
    parser.add_argument('--list-formats', action='store_true', help='List available video formats instead of downloading')
    parser.add_argument('--format', help='Video format code or quality (e.g. "best", "bestvideo+bestaudio", "137+140", "mp4")')
    args = parser.parse_args()
    
    # Use context manager to ensure cleanup
    with SocialMediaDL() as dl:
        try:
            # Export cookies from specified browser and profile
            cookies_path = dl.export_browser_cookies(url=args.url, browser=args.browser, profile=args.profile)
            
            if args.list_formats:
                # Just list formats and exit
                dl_with_cookies = SocialMediaDL(cookies_file=str(cookies_path))
                dl_with_cookies.list_formats(args.url)
            else:
                # Create new instance with the exported cookies
                dl_with_cookies = SocialMediaDL(cookies_file=str(cookies_path))
                
                # Download content from provided URL with specified format
                format_spec = args.format if args.format else "bestvideo+bestaudio"
                result = dl_with_cookies.download_video(args.url, format=format_spec)
                
                if result.success:
                    print(f"Downloaded to: {result.file_path}")
                    if result.metadata:
                        print(f"Creator: {result.metadata['creator']}")
                else:
                    print(f"Download failed: {result.error}")
                
        except Exception as e:
            print(f"Error: {e}")
            exit(1)