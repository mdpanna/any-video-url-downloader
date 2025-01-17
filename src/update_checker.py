import os
import sys
import requests
from packaging import version
from PyQt5.QtWidgets import QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor

class VersionChecker:
    def __init__(self, current_version, api_url):
        self.current_version = current_version
        self.api_url = api_url
        self.update_info = None

    def check_for_updates(self):
        """
        Check for updates by calling the Next.js API endpoint
        Returns: (bool, dict) - (update_available, update_info)
        """
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                self.update_info = response.json()
                latest_version = self.update_info.get('version')
                
                if latest_version and version.parse(latest_version) > version.parse(self.current_version):
                    return True, self.update_info
                
            return False, None
        except Exception as e:
            print(f"Error checking for updates: {str(e)}")
            return False, None

    def download_update(self, download_url, save_dir, progress_dialog):
        """
        Download the new version of the software with detailed progress tracking
        Args:
            download_url: URL to download the update from
            save_dir: Directory to save the downloaded file
            progress_dialog: QProgressDialog instance for showing progress
        """
        try:
            # Make a streaming request to get the file
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            # Get file size and set up progress dialog
            total_size = int(response.headers.get('content-length', 0))
            progress_dialog.setMaximum(100)
            progress_dialog.setValue(0)
            
            # Prepare filename
            base_filename = "Any Video Url Downloader.exe"
            base_name, extension = os.path.splitext(base_filename)
            
            # Handle duplicate filenames
            counter = 0
            final_path = os.path.join(save_dir, base_filename)
            while os.path.exists(final_path):
                counter += 1
                final_path = os.path.join(save_dir, f"{base_name} ({counter}){extension}")
            
            # Download with progress tracking
            block_size = 1024  # 1 Kibibyte
            downloaded = 0
            
            with open(final_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    if progress_dialog.wasCanceled():
                        f.close()
                        os.remove(final_path)
                        return None
                        
                    downloaded += len(data)
                    f.write(data)
                    
                    # Update progress dialog
                    if total_size > 0:
                        percent = int((downloaded / total_size) * 100)
                        downloaded_mb = downloaded / (1024 * 1024)
                        total_mb = total_size / (1024 * 1024)
                        progress_dialog.setLabelText(
                            f"Downloading: {percent}% complete\n"
                            f"({downloaded_mb:.1f} MB / {total_mb:.1f} MB)"
                        )
                        progress_dialog.setValue(percent)
                    
                    # Process events to keep UI responsive
                    QTimer.singleShot(0, lambda: None)
            
            return final_path
        except Exception as e:
            if os.path.exists(final_path):
                try:
                    os.remove(final_path)
                except:
                    pass
            raise Exception(f"Failed to download update: {str(e)}")

def set_dark_theme(dialog):
    """Apply dark theme to the progress dialog"""
    palette = QPalette()
    
    # Set colors for different elements
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(42, 42, 42))
    palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    
    dialog.setPalette(palette)
    
    # Additional styling for progress bar and other elements
    dialog.setStyleSheet("""
        QProgressDialog {
            background-color: #353535;
            border: 1px solid #2a2a2a;
        }
        QProgressBar {
            border: 1px solid #2a2a2a;
            border-radius: 3px;
            text-align: center;
            padding: 1px;
            background: #2a2a2a;
        }
        QProgressBar::chunk {
            background: #4a90e2;
            border-radius: 2px;
        }
        QPushButton {
            background-color: #4a4a4a;
            border: 1px solid #2a2a2a;
            border-radius: 3px;
            padding: 5px 15px;
            color: white;
        }
        QPushButton:hover {
            background-color: #5a5a5a;
        }
        QPushButton:pressed {
            background-color: #404040;
        }
        QLabel {
            color: white;
            font-size: 12px;
        }
    """)

def check_and_update(main_window, current_version, api_url):
    """
    Main function to check for updates and handle the update process
    """
    version_checker = VersionChecker(current_version, api_url)
    update_available, update_info = version_checker.check_for_updates()
    
    if update_available and update_info:
        msg = QMessageBox(main_window)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Update Available")
        msg.setText(f"A new version ({update_info['version']}) is available!")
        msg.setInformativeText("Would you like to download the update?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        if msg.exec_() == QMessageBox.Yes:
            try:
                # Get download directory
                download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)
                
                # Create progress dialog with detailed information
                progress = QProgressDialog(main_window)
                progress.setWindowTitle("Downloading Update")
                progress.setLabelText("Preparing download...")
                progress.setCancelButtonText("Cancel")
                progress.setWindowModality(Qt.WindowModal)
                progress.setMinimumDuration(0)
                progress.setAutoClose(True)
                progress.setAutoReset(True)
                progress.setFixedSize(400, 150)  # Set fixed size for better appearance
                
                # Apply dark theme
                set_dark_theme(progress)
                
                # Download the update
                downloaded_path = version_checker.download_update(
                    update_info['download_url'], 
                    download_dir,
                    progress
                )
                
                if downloaded_path:
                    QMessageBox.information(
                        main_window,
                        "Update Downloaded",
                        f"Update has been downloaded to:\n{downloaded_path}\n\nPlease close the current version and run the new one."
                    )
                    
                    run_now = QMessageBox.question(
                        main_window,
                        "Run Update",
                        "Would you like to run the new version now?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    
                    if run_now == QMessageBox.Yes:
                        os.startfile(downloaded_path)
                        main_window.close()
                else:
                    QMessageBox.information(
                        main_window,
                        "Download Cancelled",
                        "The update download was cancelled."
                    )
                    
            except Exception as e:
                QMessageBox.warning(
                    main_window,
                    "Update Error",
                    f"Failed to download update: {str(e)}"
                )
    return update_available