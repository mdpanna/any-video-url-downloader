from PyQt5.QtWidgets import (
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QProgressBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

from utils import resource_path


def init_ui(self,CURRENT_VERSION):
    # Central widget and main layout
    central_widget = QWidget()
    main_layout = QVBoxLayout()
    central_widget.setLayout(main_layout)
    self.setCentralWidget(central_widget)
    
    # Logo
    logo_label = QLabel()
    logo_resource_path = resource_path("assets/logo.png")
    logo_pixmap = QPixmap(logo_resource_path)
    logo_pixmap = logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    logo_label.setPixmap(logo_pixmap)
    logo_label.setAlignment(Qt.AlignCenter)
    main_layout.insertWidget(0, logo_label)

    # Title
    title_label = QLabel("Any Video Url Downloader")
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setFont(QFont('Arial', 20, QFont.Bold))
    main_layout.addWidget(title_label)
    main_layout.addSpacing(20)

    # URL Input Section
    url_layout = QVBoxLayout()
    url_label = QLabel("Enter Any Video URL/Link:")
    self.url_input = QLineEdit()
    self.url_input.setPlaceholderText("Paste URL here")
    url_layout.addWidget(url_label)
    url_layout.addWidget(self.url_input)

    # Format Selection Section
    format_layout = QVBoxLayout()
    format_label = QLabel("Selected Format:")
    self.selected_format_label = QLabel("No format selected")
    self.select_format_button = QPushButton("Select Format")
    self.select_format_button.clicked.connect(self.show_format_selection)
    format_layout.addWidget(format_label)
    format_layout.addWidget(self.selected_format_label)
    format_layout.addWidget(self.select_format_button)

    # Output Directory Section
    output_layout = QHBoxLayout()
    self.output_label = QLabel("Output: Not Selected")
    self.output_button = QPushButton("Select Folder")
    self.output_button.clicked.connect(self.select_output_directory)
    output_layout.addWidget(self.output_label)
    output_layout.addWidget(self.output_button)

    # Download Button
    self.download_button = QPushButton("Download")
    self.download_button.clicked.connect(self.download_video)

    # Progress Section
    self.progress_bar = QProgressBar()
    self.progress_bar.setTextVisible(True)
    self.progress_bar.setFormat("%p% | %v/%m")
    
    self.status_label = QLabel("Ready to download")
    self.status_label.setAlignment(Qt.AlignCenter)


    self.version_label = QLabel(f"Version {CURRENT_VERSION}", self)
    self.version_label.setAlignment(Qt.AlignCenter)
    self.version_label.setStyleSheet("""
        QLabel {
            color: #666666;
            font-size: 18px;
            padding: 5px;
        }
    """)
    # Add all layouts to main layout
    main_layout.addLayout(url_layout)
    main_layout.addSpacing(10)
    main_layout.addLayout(format_layout)
    main_layout.addSpacing(10)
    main_layout.addLayout(output_layout)
    main_layout.addSpacing(10)
    main_layout.addWidget(self.download_button)
    main_layout.addSpacing(10)
    main_layout.addWidget(self.progress_bar)
    main_layout.addWidget(self.status_label)
    main_layout.addWidget(self.version_label)

    # Additional setup
    self.output_dir = ""
    self.selected_format = None
    self.available_formats = []
