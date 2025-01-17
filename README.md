# Any Video URL Downloader

A feature-rich PyQt5-based video downloader with format selection, dark mode, and progress tracking capabilities. Powered by yt-dlp and designed for a seamless user experience.

## Features

- **Format Selection**: Choose your preferred video format and quality
- **Dark Mode Support**: Easy on the eyes with built-in dark theme
- **Progress Tracking**: Real-time download progress monitoring
- **Update Checker**: Stays up-to-date with the latest features
- **Rating System**: Rate and manage your downloads
- **Color Scheme Customization**: Personalize your experience

## Project Structure

```
any-video-url-downloader/
├── assets/
│   ├── logo.ico
│   └── logo.png
├── src/
│   ├── formatWindow_init.py
│   ├── format_selection_dialog.py
│   ├── main.py
│   ├── mainWindowColorScheme.py
│   ├── mainWindow_init.py
│   ├── progress_tracker.py
│   ├── rating_dialog.py
│   ├── update_checker.py
│   └── utils.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── version.txt
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mdpanna/any-video-url-downloader.git
cd any-video-url-downloader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python src/main.py
```

2. Paste the video URL you want to download
3. Select your preferred format and quality
4. Click download and monitor the progress

## Requirements

The project requires the following main dependencies:
- PyQt5
- yt-dlp
- Additional dependencies are listed in `requirements.txt`

## Development

The project is structured into several key components:
- `main.py`: Application entry point
- `formatWindow_init.py`: Format selection interface
- `progress_tracker.py`: Download progress monitoring
- `mainWindowColorScheme.py`: UI theme management
- `utils.py`: Helper functions and utilities

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the terms specified in the `LICENSE` file.

