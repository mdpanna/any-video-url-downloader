import sys
import re
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, 
     QDialog,QDesktopWidget, QDialog, QVBoxLayout, QLabel, QProgressBar, 
    QDialogButtonBox
)
from PyQt5.QtCore import  QPropertyAnimation, QEasingCurve,QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon


import yt_dlp
from update_checker import check_and_update
from progress_tracker import create_progress_tracker
from mainWindowColorScheme import setup_color_scheme
from utils import resource_path
from mainWindow_init import init_ui  # Import the function
from format_selection_dialog import FormatSelectionDialog  # Import the function

from rating_dialog import show_rating_dialog_after_delay
CURRENT_VERSION = "4.1.2"




class FormatFetchThread(QThread):
    """
    Background thread for fetching video formats to prevent UI freezing
    """
    formats_fetched = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        import yt_dlp
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                
                # Get all available formats
                formats = info_dict.get('formats', [])
                
                # Filter out duplicates and sort
                unique_formats = []
                format_ids = set()
                for fmt in formats:
                    if fmt['format_id'] not in format_ids:
                        unique_formats.append(fmt)
                        format_ids.add(fmt['format_id'])
                
                self.formats_fetched.emit(unique_formats)
        except Exception as e:
            self.error_occurred.emit(str(e))

class LoadingDialog(QDialog):
    """
    Custom loading dialog for format fetching
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fetching Formats")
        self.setModal(True)
        
        # Set dark background and white text
        self.setStyleSheet("""
            QDialog {
                background-color: #333333;
            }
            QLabel {
                color: white;
                font-size: 20px;
            }
            
        """)
        layout = QVBoxLayout()
        
        # Loading message
        self.loading_label = QLabel("Fetching available video formats...")
        layout.addWidget(self.loading_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
        
        # Center the dialog
        self.setGeometry(
            parent.geometry().center().x() - 150, 
            parent.geometry().center().y() - 50, 
            500, 
            200
        )

class StyledVideoDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Any Video URL Downloader")

        # Set window size based on device type
        self.set_window_size()

        # Center the window on the screen
        self.center_window()

        window_logo_path = resource_path("assets/logo.png")
        self.setWindowIcon(QIcon(window_logo_path))

        # Apply the color scheme
        setup_color_scheme(self)
        init_ui(self,CURRENT_VERSION)

    def set_window_size(self):
        """
        Set window size dynamically based on device type.
        """
        # Get the screen geometry
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        # Determine device type and set appropriate window size
        if screen_width >= 1920:  # Desktop
            fixed_width = 600
            fixed_height = 800
        elif screen_width >= 1024:  # Tablet (landscape)
            fixed_width = 500
            fixed_height = 700
        else:  # Small tablet or mobile
            fixed_width = 400
            fixed_height = 600

        # Set the fixed size for the window
        self.setFixedSize(fixed_width, fixed_height)

    def center_window(self):
        """
        Center the window on the screen.
        """
        # Get the window geometry
        window_geometry = self.frameGeometry()
        
        # Get the screen center point
        screen_center = QDesktopWidget().availableGeometry().center()
        
        # Move the window center to the screen center
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

    def select_output_directory(self):
        """
        Open a file dialog to select the output directory with animation.
        """
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir = dir_path
            # Animate the label change
            self.output_label.setText(f"Output: {dir_path}")
            
            # Optional: Add a subtle animation to draw attention
            animation = QPropertyAnimation(self.output_label, b"geometry")
            animation.setDuration(200)
            animation.setStartValue(self.output_label.geometry())
            animation.setEndValue(self.output_label.geometry().adjusted(-10, 0, 10, 0))
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.start()

    def show_format_selection(self):
        """
        Retrieve and show available formats for download with a loading popup.
        """
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a valid URL.")
            return

        # Create and show loading dialog
        loading_dialog = LoadingDialog(self)
        loading_dialog.show()

        # Create background thread for format fetching
        self.fetch_thread = FormatFetchThread(url)
        
        def handle_formats_fetched(formats):
            loading_dialog.close()
            # Store available formats
            self.available_formats = formats
            
            # Open format selection dialog
            format_dialog = FormatSelectionDialog(formats, self)
            
            if format_dialog.exec_() == QDialog.Accepted:
                # Get selected format
                self.selected_format = format_dialog.get_selected_format()
                
                # Update label with selected format details
                if self.selected_format:
                    format_text = (
                        f"Code: {self.selected_format.get('format_id', 'N/A')} | "
                        f"Resolution: {self.selected_format.get('height', 'N/A')}p | "
                        f"Ext: {self.selected_format.get('ext', 'N/A')}"
                    )
                    self.selected_format_label.setText(format_text)

        def handle_fetch_error(error):
            loading_dialog.close()
            QMessageBox.warning(self, "Error", f"Could not retrieve formats: {error}")

        # Connect thread signals
        self.fetch_thread.formats_fetched.connect(handle_formats_fetched)
        self.fetch_thread.error_occurred.connect(handle_fetch_error)
        
        # Start the thread
        self.fetch_thread.start()

    def sanitize_filename(self, filename):
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = re.sub(r'[^\x00-\x7F]+', '', filename)
        max_length = 100
        if len(filename) > max_length:
            filename = filename[:max_length]
        filename = filename.strip('. ')
        return filename or 'video'

    def ensure_directory_exists(self, path):
        """
        Ensure the directory exists, create it if it doesn't.
        """
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not create directory: {str(e)}")
            return False
        return True


    def download_video(self):
        # Modify download method to use selected format
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a valid URL.")
            return

        if not self.output_dir:
            QMessageBox.warning(self, "Error", "Please select an output directory.")
            return

        if not self.selected_format:
            QMessageBox.warning(self, "Error", "Please select a format to download.")
            return

        # Create progress tracker hook
        progress_hook = create_progress_tracker(self.progress_bar, self.status_label)
         # Disable the button and change its color
        self.download_button.setEnabled(False)
        self.download_button.setStyleSheet("background-color: #FF6347; color: white;")  # Tomato color
        self.status_label.setText("Starting download...")

        # Prepare yt-dlp options with selected format
        ydl_opts = {
            'format': self.selected_format['format_id'],
            'outtmpl': f"{self.output_dir}/%(title).100s.%(ext)s",
            'progress_hooks': [progress_hook],
            # Key addition: Merge audio if no audio stream exists
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # or another preferred format
            }] if 'potential_audio' in self.selected_format else []
        }
        if 'potential_audio' in self.selected_format:
            # Select the best audio format
            best_audio = max(
                self.selected_format['potential_audio'], 
                key=lambda x: x.get('abr', 0)  # Choose by audio bitrate
            )
            ydl_opts['format'] = f"{self.selected_format['format_id']}+{best_audio['format_id']}"



        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    video_info = ydl.extract_info(url, download=False)
                    if video_info:
                        video_title = self.sanitize_filename(video_info.get('title', 'Unknown Title'))
                        self.status_label.setText(f"Downloading: {video_title}")
                        QApplication.processEvents()

                        # Start downloading
                        ydl.download([url])
                    else:
                        raise Exception("Video information could not be retrieved.")
                except yt_dlp.utils.DownloadError as e:
                    if "private video" in str(e).lower() or "not available" in str(e).lower():
                        QMessageBox.warning(self, "Error", "The video is private or not available for download.")
                    else:
                        QMessageBox.warning(self, "Error", f"Download failed: {str(e)}")
                    self.status_label.setText("Download failed")
        except Exception as e:
            error_message = re.sub(r'\x1b\[[0-9;]*m', '', str(e))  # Strip ANSI color codes
            QMessageBox.warning(self, "Error", f"An unexpected error occurred: {error_message}")
            self.status_label.setText("Error occurred")
        finally:
            # Re-enable the button and reset its color
            self.download_button.setEnabled(True)
            self.download_button.setStyleSheet("")  # Reset to default
            self.status_label.setText("Download complete or failed.")

    
    
if __name__ == "__main__":
    # Replace with your actual Supabase credentials
    SUPABASE_URL = ""
    SUPABASE_KEY = ""
    # Print details for verification
            
    app = QApplication(sys.argv)
    
    # Optional: Set application-wide font
    font = QFont("Arial", 10)
    app.setFont(font)
    
    icon_path = resource_path("assets/logo.ico")
    app.setWindowIcon(QIcon(icon_path))
    
    window = StyledVideoDownloader()
    window.show()
    
    # Add these constants for update checking
    API_URL = ""  # Replace with your actual API endpoint
    
    # Check for updates
    check_and_update(window, CURRENT_VERSION, API_URL)
    # Pass the required arguments to check_for_update
    show_rating_dialog_after_delay(SUPABASE_URL, SUPABASE_KEY)

    sys.exit(app.exec_())