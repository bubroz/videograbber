#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime

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

def read_info_json(file_path):
    """Read and extract essential information from info.json file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Extract only the essential information
        info = {
            "Title": data.get("title", "Unknown"),
            "Creator": data.get("uploader", "Unknown"),
            "Upload Date": format_date(data.get("upload_date")),
            "Duration": format_duration(data.get("duration")),
            "Resolution": f"{data.get('width', '?')}x{data.get('height', '?')}",
            "View Count": data.get("view_count", "Unknown"),
            "URL": data.get("webpage_url", "Unknown")
        }
        
        return info
    except Exception as e:
        return {"Error": f"Failed to read file: {str(e)}"}

def main():
    if len(sys.argv) < 2:
        print("Usage: python json_info_reader.py <path_to_info.json>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    
    info = read_info_json(file_path)
    
    # Print information in a clean format
    print("\n=== Video Information ===")
    for key, value in info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main() 