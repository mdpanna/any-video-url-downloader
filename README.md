# Any Video URL Downloader  
A powerful and versatile video downloader that allows you to download videos from virtually any website, including YouTube, Vimeo, Twitter, Instagram, Facebook, and thousands more. Built with **PyQt5** for a modern interface and powered by **yt-dlp** for maximum compatibility.  

![Project Banner - Add your logo here]  

---

## 🚀 Key Features  
- **Universal URL Support**: Download videos from almost any website.  
- **Multiple Format Options**: Choose from available video qualities and formats.  
- **Smart Format Selection**: Automatically detects all available formats for each video.  
- **Progress Tracking**: Real-time download progress with speed and ETA.  
- **Dark Mode**: Easy on the eyes with a built-in dark theme.  
- **User-Friendly Interface**: Simple and intuitive PyQt5-based GUI.  
- **Auto-Updates**: Stays current with the latest website changes.  
- **Download Rating System**: Track and rate your downloads.  
- **Color Scheme Customization**: Personalize your experience.  

---

## 🎯 Supported Websites  
Download from thousands of websites, including:  
- **YouTube**  
- **Vimeo**  
- **Facebook**  
- **Instagram**  
- **Twitter**  
- **TikTok**  
- **Dailymotion**  
- **And many more!**  

---

## 🚀 Quick Start  

1. Clone the repository:  
   ```bash
   git clone https://github.com/mdpanna/any-video-url-downloader.git  
   cd any-video-url-downloader  
   ```  

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt  
   ```  

4. Run the application:  
   ```bash
   python src/main.py  
   ```  

---

## 📥 How to Use  

1. Launch the application.  
2. Copy and paste any video URL.  
3. Select your preferred format and quality.  
4. Choose the download location.  
5. Click download and watch the progress!  

---

## 🔧 Project Structure  

```
any-video-url-downloader/  
├── assets/                  # Icons and images  
│   ├── logo.ico  
│   └── logo.png  
└── src/                    # Source code  
    ├── main.py            # Main application entry  
    ├── formatWindow_init.py  
    ├── format_selection_dialog.py  
    ├── mainWindowColorScheme.py  
    ├── mainWindow_init.py  
    ├── progress_tracker.py  
    ├── rating_dialog.py  
    ├── update_checker.py  
    └── utils.py  
```  

---

## ⚙️ Requirements  
- **Python 3.6 or higher**  
- **PyQt5**  
- **yt-dlp**  
- Additional dependencies listed in `requirements.txt`.  

---

## 📝 License  
This project is licensed under the terms specified in the [LICENSE](LICENSE) file.  

---

## ⚠️ Note  
Please ensure you have the right to download content before using this tool. Respect copyright laws and the terms of service of the websites you download from.