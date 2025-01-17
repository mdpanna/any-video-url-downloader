from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget

def setup_color_scheme(widget):
    """
    Apply a modern, dark-themed color palette to the given widget
    with dynamically adjusted font sizes based on screen size.
    """
    # Determine screen size
    screen = QDesktopWidget().screenGeometry()
    screen_width = screen.width()

    # Adjust font sizes based on screen size
    base_font_size = 18
    heading_font_size = 22
    button_font_size = 18
    

    # Create color palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    widget.setPalette(palette)
    widget.setStyleSheet(f"""
        QMainWindow {{
            background-color: #353535;
            color: white;
        }}
        QLabel {{
            color: white;
            font-size: {heading_font_size}px;
        }}
        QLineEdit {{
            padding: 10px;
            border: 2px solid #4a4a4a;
            border-radius: 8px;
            background-color: #2a2a2a;
            color: white;
            font-size: {base_font_size}px;
        }}
        QPushButton {{
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
            font-size: {button_font_size}px;
        }}
        QPushButton:hover {{
            background-color: #45a049;
        }}
        QPushButton:disabled {{
            background-color: #888888;
        }}
        QProgressBar {{
            border: none;
            background-color: #2c3e50;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: {base_font_size}px;
        }}
        QProgressBar::chunk {{
            background-color: #4CAF50;
            border-radius: 10px;
            margin: 2px;
        }}
        QMessageBox {{
            background-color: #353535;
        }}
        QMessageBox QLabel {{
            color: white;
            font-size: {base_font_size}px;
        }}
        QMessageBox QPushButton {{
            background-color: #4a4a4a;
            color: white;
            min-width: 80px;
            font-size: {button_font_size}px;
        }}
        QMessageBox QPushButton:hover {{
            background-color: #5a5a5a;
        }}
        QTableWidget {{
            background-color: #2a2a2a;
            color: white;
            alternate-background-color: #353535;
            font-size: {base_font_size}px;
        }}
        QTableWidget::item {{
            color: white;
            border: 1px solid #4a4a4a;
        }}
        QTableWidget::item:selected {{
            background-color: #4CAF50;
        }}
    """)