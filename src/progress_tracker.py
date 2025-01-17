from PyQt5.QtWidgets import QMessageBox, QApplication

class ProgressTracker:
    def __init__(self, progress_bar, status_label):
        """
        Initialize the progress tracker with UI components.
        
        :param progress_bar: QProgressBar to show download progress
        :param status_label: QLabel to show download status
        """
        self.progress_bar = progress_bar
        self.status_label = status_label

    def progress_hook(self, d):
        """
        Track download progress and update UI.
        
        :param d: Dictionary containing download status information
        """
        try:
            status = d.get('status')

            if status == 'downloading':
                # Extract download progress information
                downloaded_bytes = d.get('downloaded_bytes', 0)
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                
                # Calculate progress percentage
                if total_bytes > 0:
                    percent = min(100, (downloaded_bytes / total_bytes) * 100)
                else:
                    percent = 0

                # Get download speed
                speed = d.get('_speed_str', 'N/A').strip()
                
                # Get estimated time remaining
                eta = d.get('_eta_str', 'N/A').strip()

                # Update progress bar
                self.progress_bar.setValue(int(percent))

                # Update status label with detailed information
                status_text = f"Downloading: {percent:.1f}% | Speed: {speed} | ETA: {eta}"
                self.status_label.setText(status_text)
                QApplication.processEvents()

            elif status == 'finished':
                # Download complete
                self.progress_bar.setValue(100)
                self.status_label.setText("Download complete!")
                QMessageBox.information(None, "Success", "Download completed successfully!")

            elif status == 'error':
                # Handle download errors
                error_msg = d.get('error', 'Unknown error')
                self.status_label.setText(f"Download error: {error_msg}")
                QMessageBox.warning(None, "Download Error", str(error_msg))
                self.progress_bar.setValue(0)
        
        except Exception as e:
            # Catch and log any unexpected errors in progress tracking
            print(f"Progress hook error: {e}")
            self.status_label.setText("Error in progress tracking")

def create_progress_tracker(progress_bar, status_label):
    """
    Factory function to create a progress tracker.
    
    :param progress_bar: QProgressBar to show download progress
    :param status_label: QLabel to show download status
    :return: A progress_hook function
    """
    tracker = ProgressTracker(progress_bar, status_label)
    return tracker.progress_hook