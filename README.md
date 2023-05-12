<h1 align="center">
    <img src="https://em-content.zobj.net/thumbs/240/facebook/355/film-frames_1f39e-fe0f.png" alt="Markdownify" width="200">
    <br>
    YouTube Clips Markdown Generator
</h1>

<h4 align="center">The YouTube Clips Markdown Generator is a Python-based tool that simplifies the process of creating markdown files from YouTube video clips. This tool allows you to extract relevant information from YouTube videos, including clip titles, URLs, and transcripts, and generate organized markdown files for easy reference and sharing.

</h4>

## Features

- Extract clip information: Retrieve clip titles, URLs, and transcripts from YouTube video clips.
- Generate markdown files: Automatically generate well-structured markdown files with video details and clip information.
- Organize clips: Create nested bullet points to represent the hierarchical structure of clips within a video.
- Download video transcripts: Automatically download and process video transcripts for accurate clip transcriptions.
- Customize output: Modify the generated markdown files to fit your specific needs or styling preferences.
- Time-saving and efficient: Automate the tedious process of manually extracting and formatting information from YouTube videos.

## File Structure

The repository has the following file structure:
```
├── export-markdown
│ ├── clipTranscript.py
│ └── utils.py
└── export-youtube-clips
├── clipCheckboxes.js
├── export.js
├── icons
│ ├── icon128.png
│ ├── icon16.png
│ └── icon48.png
└── manifest.json
```
- The `export-markdown` directory contains the Python scripts for extracting clip information and generating markdown files.
- The `export-youtube-clips` directory contains the chrome extentsion's JavaScript files responsible for adding checkboxes to YouTube video thumbnails and exporting clips to markdown.

## Usage

Chrome extension:

1. Install the chrome extentsion in the export-youtube-clips
2. Load the browser extension (Chrome, Firefox, etc.) using the provided manifest file.
3. Navigate to a YouTube Clips page (https://www.youtube.com/feed/clips) and wait for the page to fully load.
4. Select the clips that you want to export by checking the boxes (you can use shift click)
5. Click the "Copy Clip Links" button to export the selected clip URLs as markdown.

Clip Transcripts:

1. Install the python requirements
   `pip install -r export-markdown/requirements.txt`
2. Run get the transcripts and export to markdown.
   `python3 export-markdown/clipTrancsript.py <clip_url> <clip_url>`
   the `<clip_url>` can just be pasted from the extension
   Example: `python clipTranscript.py https://www.youtube.com/clip/clip1 https://www.youtube.com/clip/clip2`
3. The come directory should have the markdown files for each video

## Contributing

Contributions to the YouTube Clips Markdown Generator are welcome! If you find any issues, have suggestions for improvements, or want to add new features, please feel free to submit a pull request or open an issue on the repository.

Before contributing, please familiarize yourself with the [contribution guidelines](CONTRIBUTING.md) of the project.

## License

The YouTube Clips Markdown Generator is open-source software licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this tool for personal or commercial purposes.

## Acknowledgements

The YouTube Clips Markdown Generator is based on the work of several contributors. We would like to thank them for their efforts and contributions to the project.
