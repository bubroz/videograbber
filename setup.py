from setuptools import setup, find_packages

setup(
    name="videograbber",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "yt-dlp>=2023.0.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "websockets>=12.0",
        "brotli>=1.1.0",
        "mutagen>=1.47.0",
        "pycryptodomex>=3.19.0"
    ],
    entry_points={
        'console_scripts': [
            'videograbber=videograbber.social_media_dl:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to download videos from various social media platforms with simplified metadata",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/videograbber",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 