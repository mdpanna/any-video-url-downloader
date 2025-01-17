from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QDialogButtonBox, QFrame, QApplication
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QPainter
from PyQt5.QtCore import QPointF,QTimer,Qt
from supabase import create_client, Client
import requests
import platform
import uuid
import socket

class StarRatingWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        self.stars = 0
        self.max_stars = 5
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        star_size = 40
        spacing = 10
        total_width = (star_size * self.max_stars) + (spacing * (self.max_stars - 1))
        start_x = (self.width() - total_width) / 2
        
        for i in range(self.max_stars):
            # Draw star outline
            painter.setPen(QColor(200, 200, 200))
            painter.setBrush(QColor(240, 240, 240))
            
            # Fill stars up to the current rating
            if i < self.stars:
                painter.setBrush(QColor(255, 215, 0))  # Gold color for filled stars
            
            # Star polygon
            star_points = [
                QPointF(start_x + i * (star_size + spacing) + star_size/2, star_size/2),
                QPointF(start_x + i * (star_size + spacing) + star_size * 0.8, star_size * 0.3),
                QPointF(start_x + i * (star_size + spacing) + star_size, star_size * 0.35),
                QPointF(start_x + i * (star_size + spacing) + star_size * 0.9, star_size * 0.7),
                QPointF(start_x + i * (star_size + spacing) + star_size, star_size),
                QPointF(start_x + i * (star_size + spacing) + star_size/2, star_size * 0.8),
                QPointF(start_x + i * (star_size + spacing), star_size),
                QPointF(start_x + i * (star_size + spacing) + 0.1 * star_size, star_size * 0.7),
                QPointF(start_x + i * (star_size + spacing), star_size * 0.35),
                QPointF(start_x + i * (star_size + spacing) + 0.2 * star_size, star_size * 0.3)
            ]
            
            painter.drawPolygon(star_points)
        
        # Always end the painter to prevent QBackingStore warning
        painter.end()

class RatingDialog(QDialog):
    def __init__(self, supabase_url, supabase_key, parent=None):
        super().__init__(parent)

        # Supabase setup
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key

        # Dialog setup
        self.setWindowTitle("Rate Your Experience")
        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowCloseButtonHint
        )
        self.setMinimumSize(400, 400)

        # Main layout
        layout = QVBoxLayout()

        # Title
        title_label = QLabel("How was your experience?")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title_label)

        # Star rating widget
        self.star_rating = StarRatingWidget()
        self.star_rating.setFixedHeight(80)
        layout.addWidget(self.star_rating)

        # Bind mouse events to star rating
        self.star_rating.mousePressEvent = self.on_star_press

        # Optional review text box
        self.review_box = QtWidgets.QTextEdit()
        self.review_box.setPlaceholderText("Write your review here (optional)...")
        self.review_box.setFixedHeight(100)
        layout.addWidget(self.review_box)

        # Buttons layout
        button_layout = QHBoxLayout()

        # Send button
        self.send_button = QPushButton("Send Rating")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.send_rating)

        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.send_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Styling
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px;
            }
        """)

    def on_star_press(self, event):
        star_width = self.star_rating.width() / self.star_rating.max_stars
        star_index = int(event.x() / star_width)

        # Ensure star_index is within range
        star_index = max(0, min(star_index + 1, self.star_rating.max_stars))

        self.star_rating.stars = star_index
        self.star_rating.update()

        # Enable send button when a rating is selected
        self.send_button.setEnabled(True)

    
    def get_system_info(self):
        """Collect system information for logging."""
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'device_type': self.get_device_type(),
            'ip_address': self.get_ip_address()
        }
    
    def get_device_type(self):
        """Determine device type based on screen size."""
        screen = QApplication.primaryScreen().geometry()
        width, height = screen.width(), screen.height()
        
        if width >= 1920:
            return 'Desktop'
        elif width >= 1024:
            return 'Tablet'
        else:
            return 'Mobile'
    
    def get_ip_address(self):
        """Get the user's IP address using the socket module."""
        try:
            # Get the hostname of the machine
            hostname = socket.gethostname()
            # Fetch the local IP address
            local_ip = socket.gethostbyname(hostname)
            return local_ip
        except Exception as e:
            print(f"Error getting IP address: {e}")
            return 'Unknown'

        
    
    def send_rating(self):
        """Send rating and optional review to Supabase."""
        try:
            # Initialize Supabase client
            supabase = create_client(self.supabase_url, self.supabase_key)

            # Collect system info
            system_info = self.get_system_info()

            # Prepare rating data
            rating_data = {
                'rating': self.star_rating.stars,
                'review': self.review_box.toPlainText().strip(),
                'platform': system_info['platform'],
                'ip_address': system_info['ip_address'],
                'user_id': str(uuid.uuid4()),  # Generate a unique user ID
                'os': f"{system_info['platform']} {system_info['platform_release']}",
                'device_type': system_info['device_type']
            }

            # Insert rating into Supabase
            response = supabase.table('ratings').insert(rating_data).execute()

            # Close dialog
            self.accept()

        except Exception as e:
            print(f"Error sending rating: {e}")
            self.reject()


def show_rating_dialog_after_delay(supabase_url, supabase_key, delay_ms=10000):
    """
    Show rating dialog after a specified delay.
    
    :param supabase_url: Supabase project URL
    :param supabase_key: Supabase API key
    :param delay_ms: Delay in milliseconds before showing dialog (default 10 seconds)
    """
    def show_dialog():
        if not check_previous_rating(supabase_url, supabase_key):
            dialog = RatingDialog(supabase_url, supabase_key)
            dialog.exec_()
        else:
            print("User has already provided a rating. Dialog will not be shown.")
    
    # Create a single shot timer to show dialog after delay
    QTimer.singleShot(delay_ms, show_dialog)
    
    
def check_previous_rating(supabase_url, supabase_key):
    """
    Check if the user has already provided a rating.

    :param supabase_url: Supabase project URL
    :param supabase_key: Supabase API key
    :return: Boolean indicating if a rating has been given
    """
    try:
        # Retrieve the user's IP address
        ip_address = socket.gethostbyname(socket.gethostname())

        # Initialize Supabase client
        supabase = create_client(supabase_url, supabase_key)

        # Query the Supabase table for the given IP address
        response = supabase.table('ratings').select('*').eq('ip_address', ip_address).execute()

        # Check if any records exist for this IP address
        data = response.data  # Extract the data from the response
        if data and len(data) > 0:
            return True
        return False

    except requests.exceptions.RequestException as req_err:
        print(f"Network error while checking previous rating: {req_err}")
        return False

    except Exception as e:
        print(f"Unexpected error while checking previous rating: {e}")
        return False
