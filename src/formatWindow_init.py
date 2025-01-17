def get_dark_theme_stylesheet():
    """
    Returns a comprehensive dark theme stylesheet for the Format Selection Dialog.
    
    This stylesheet provides a consistent dark theme with custom styling for 
    various Qt widgets used in the dialog.
    
    Returns:
        str: A stylesheet string with dark theme styling
    """
    return """
    QDialog {
        background-color: #353535;
    }
    QLabel {
        color: white;
        font-size: 14px;
    }
    QTableWidget {
        background-color: #2a2a2a;
        color: white;
        alternate-background-color: #353535;
        selection-background-color: #4CAF50;
        gridline-color: #4a4a4a;
        border: 2px solid #4a4a4a;
        border-radius: 10px;
    }
    QTableWidget::item {
        padding: 5px;
        border: 1px solid #4a4a4a;
        color: white;
    }
    QTableWidget::item:selected {
        background-color: #4CAF50;
        color: black;
    }
    QHeaderView::section {
        background-color: #4a4a4a;
        color: white;
        padding: 5px;
        border: 1px solid #353535;
        font-weight: bold;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QLineEdit {
        padding: 8px;
        border: 2px solid #4a4a4a;
        border-radius: 8px;
        background-color: #2a2a2a;
        color: white;
    }
    """