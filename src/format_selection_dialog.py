from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QAbstractItemView, QHeaderView, QRadioButton, QButtonGroup, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont

# Import the stylesheet function
from formatWindow_init import get_dark_theme_stylesheet


class FormatSelectionDialog(QDialog):
    def __init__(self, formats, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Download Format")
        self.setGeometry(200, 200, 1200, 900)  # Slightly wider to accommodate radio buttons
        
        # Dark theme palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.Text, Qt.white)
        self.setPalette(palette)
        
        # Set the stylesheet from the external function
        self.setStyleSheet(get_dark_theme_stylesheet() + """
            QRadioButton {
                color: white;
                spacing: 10px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #4CAF50;
                background-color: #2a2a2a;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #4CAF50;
                background-color: #4CAF50;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Top section with search and filter options
        top_section = QHBoxLayout()
        
        # Search bar
        search_layout = QVBoxLayout()
        search_label = QLabel("Search Formats:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter formats by resolution, codec...")
        self.search_input.textChanged.connect(self.filter_formats)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        
        # Radio button group for format filtering
        filter_layout = QVBoxLayout()
        filter_label = QLabel("Filter by:")
        filter_layout.addWidget(filter_label)
        
        # Create radio button group
        self.filter_group = QButtonGroup()
        self.filter_group.setExclusive(True)
        
        # Radio button options
        filter_options = [
            ("All Formats", "all"),
            ("Video Only", "video"),
            ("Audio Only", "audio"),
            ("High Resolution", "high_res")
        ]
        
        for text, option in filter_options:
            radio_btn = QRadioButton(text)
            radio_btn.option = option  # Custom attribute to identify the filter type
            self.filter_group.addButton(radio_btn)
            filter_layout.addWidget(radio_btn)
        
        # Set default selection
        self.filter_group.buttons()[0].setChecked(True)
        self.filter_group.buttonClicked.connect(self.apply_radio_filter)
        
        # Add search and filter to top section
        top_section.addLayout(search_layout, 3)  # 3 parts of width
        top_section.addLayout(filter_layout, 1)  # 1 part of width
        
        layout.addLayout(top_section)
        
        # Create table for format selection
        self.format_table = QTableWidget()
        self.format_table.setColumnCount(7)
        self.format_table.setHorizontalHeaderLabels([
            "Code", "Extension", "Resolution", "FPS", 
            "Video Codec", "Media Type", "Audio Status"
        ])
        self.format_table.setSelectionMode(QTableWidget.SingleSelection)
        self.format_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.format_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.format_table.horizontalHeader().setStretchLastSection(True)
        self.format_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Populate table with formats
        self.original_formats = formats
        self.enhanced_formats = self.enhance_formats_with_audio(formats)
        self.populate_table(self.enhanced_formats)
        
        layout.addWidget(self.format_table)
        
        # Preview section
        preview_layout = QHBoxLayout()
        self.preview_label = QLabel("Selected Format: None")
        preview_layout.addWidget(self.preview_label)
        layout.addLayout(preview_layout)
        
        # Connect selection change to update preview
        self.format_table.itemSelectionChanged.connect(self.update_preview)
        
        # Confirm button
        confirm_layout = QHBoxLayout()
        confirm_button = QPushButton("Select Format")
        confirm_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        confirm_layout.addWidget(cancel_button)
        confirm_layout.addWidget(confirm_button)
        layout.addLayout(confirm_layout)
        
        # Store formats for retrieval
        self.available_formats = self.enhanced_formats

    def apply_radio_filter(self, button):
        """
        Apply filter based on selected radio button
        """
        filter_option = button.option
        
        for row in range(self.format_table.rowCount()):
            show_row = True
            row_format = self.enhanced_formats[row]
            
            if filter_option == 'video':
                show_row = row_format.get('media_type', '').startswith('Video')
            elif filter_option == 'audio':
                show_row = row_format.get('media_type', '') == 'Audio Only'
            elif filter_option == 'high_res':
                height = row_format.get('height', 0)
                show_row = height >= 720 if isinstance(height, int) else False
            
            self.format_table.setRowHidden(row, not show_row)


    # The rest of the methods remain the same as in the original implementation
    def enhance_formats_with_audio(self, formats):
        """
        Advanced format enhancement with comprehensive audio handling:
        1. Categorize formats into video, audio, mixed, and unknown streams
        2. Implement strategies for audio extraction and merging
        3. Add comprehensive audio status and merging information
        4. Include unknown formats with descriptive annotations
        """
        # [The implementation remains exactly the same as in the original code]
        # Separate formats into categories
        video_formats = [
            fmt for fmt in formats 
            if fmt.get('vcodec', 'none') != 'none'
        ]
        audio_formats = [
            fmt for fmt in formats 
            if fmt.get('acodec', 'none') != 'none' and fmt.get('vcodec', 'none') == 'none'
        ]
        mixed_formats = [
            fmt for fmt in formats 
            if fmt.get('vcodec', 'none') != 'none' and fmt.get('acodec', 'none') != 'none'
        ]
        unknown_formats = [
            fmt for fmt in formats 
            if (fmt.get('vcodec', 'none') == 'none' and 
                fmt.get('acodec', 'none') == 'none' and
                fmt.get('format_id', 'unknown') != 'unknown')
        ]

        # Enhanced format processing
        enhanced_formats = []

        # Process mixed formats first (video with built-in audio)
        for fmt in mixed_formats:
            enhanced_fmt = fmt.copy()
            enhanced_fmt['media_type'] = 'Video + Audio'
            enhanced_fmt['audio_status'] = 'Built-in Audio'
            enhanced_fmt['audio_extraction'] = True
            enhanced_formats.append(enhanced_fmt)

        # Process video formats without audio
        for fmt in video_formats:
            if fmt.get('acodec', 'none') == 'none':
                # Find compatible audio streams
                compatible_audio = [
                    a for a in audio_formats 
                    if a.get('ext') == fmt.get('ext')  # Prefer same extension
                ] or audio_formats

                enhanced_fmt = fmt.copy()
                
                if compatible_audio:
                    # Can merge audio
                    enhanced_fmt['media_type'] = 'Video (Add Audio)'
                    enhanced_fmt['audio_status'] = f'Merge with {len(compatible_audio)} audio streams'
                    enhanced_fmt['potential_audio'] = compatible_audio
                    enhanced_fmt['audio_merging'] = True
                else:
                    # No audio available
                    enhanced_fmt['media_type'] = 'Video (No Audio)'
                    enhanced_fmt['audio_status'] = 'No Audio Streams'
                    enhanced_fmt['audio_merging'] = False
                
                enhanced_formats.append(enhanced_fmt)

        # Add pure audio formats
        for fmt in audio_formats:
            enhanced_fmt = fmt.copy()
            enhanced_fmt['media_type'] = 'Audio Only'
            enhanced_fmt['audio_status'] = 'MP3/Audio Extraction'
            enhanced_fmt['is_audio_only'] = True
            enhanced_formats.append(enhanced_fmt)

        # Process unknown formats
        for fmt in unknown_formats:
            enhanced_fmt = fmt.copy()
            enhanced_fmt['media_type'] = 'Unknown Format'
            enhanced_fmt['audio_status'] = 'Unidentified Stream'
            enhanced_fmt['format_details'] = {
                'ext': fmt.get('ext', 'Unknown'),
                'height': fmt.get('height', 'N/A'),
                'fps': fmt.get('fps', 'N/A')
            }
            enhanced_formats.append(enhanced_fmt)

        return enhanced_formats

    def populate_table(self, formats):
        """
        Populate the table with format information.
        """
        # [The implementation remains exactly the same as in the original code]
        self.format_table.setRowCount(0)
        for row, format_info in enumerate(formats):
            self.format_table.insertRow(row)
            
            # Prepare resolution with fallback
            resolution = format_info.get('height', 'N/A')
            resolution = f"{resolution}p" if isinstance(resolution, int) else str(resolution)
            
            # Populate table items
            items = [
                format_info.get('format_id', 'N/A'),
                format_info.get('ext', 'N/A'),
                resolution,
                str(format_info.get('fps', 'N/A')),
                format_info.get('vcodec', 'N/A'),
                format_info.get('media_type', 'N/A'),
                format_info.get('audio_status', 'N/A')
            ]
            
            for col, item_text in enumerate(items):
                table_item = QTableWidgetItem(str(item_text))
                table_item.setTextAlignment(Qt.AlignCenter)
                
                # Color code audio status
                if col == 6:  # Audio Status column
                    if 'Add Audio' in str(item_text):
                        table_item.setBackground(QColor(100, 200, 100, 100))  # Light green
                    elif 'No Audio' in str(item_text):
                        table_item.setBackground(QColor(200, 100, 100, 100))  # Light red
                
                self.format_table.setItem(row, col, table_item)
    
    def filter_formats(self):
        """
        Filter formats based on search text.
        """
        # [The implementation remains exactly the same as in the original code]
        search_text = self.search_input.text().lower()
        
        for row in range(self.format_table.rowCount()):
            match = False
            for col in range(self.format_table.columnCount()):
                item = self.format_table.item(row, col)
                if search_text in item.text().lower():
                    match = True
                    break
            
            self.format_table.setRowHidden(row, not match)
    
    def update_preview(self):
        """
        Update preview label when selection changes.
        """
        # [The implementation remains exactly the same as in the original code]
        selected_rows = self.format_table.selectedIndexes()
        if selected_rows:
            row = selected_rows[0].row()
            format_details = self.original_formats[row]
            
            preview_text = (
                f"Code: {format_details.get('format_id', 'N/A')} | "
                f"Resolution: {format_details.get('height', 'N/A')}p | "
                f"Extension: {format_details.get('ext', 'N/A')} | "
                f"FPS: {format_details.get('fps', 'N/A')}"
            )
            self.preview_label.setText(preview_text)
        else:
            self.preview_label.setText("Selected Format: None")
    
    def get_selected_format(self):
        """
        Retrieve the selected format, considering audio merging.
        """
        # [The implementation remains exactly the same as in the original code]
        selected_rows = self.format_table.selectedIndexes()
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        selected_format = self.available_formats[row]
        
        return selected_format