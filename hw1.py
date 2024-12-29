import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QListWidget, QMessageBox)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class ItemManager(QWidget):
    def __init__(self):
        super().__init__()
        self.items = []
        self.initUI()
        self.load_items()

    def initUI(self):
        # Main Window Properties
        self.setWindowTitle("Item Revival Software")
        self.setStyleSheet("background-color: #f4f4f4;")
        self.resize(1200, 600)

        # Main Layout
        main_layout = QVBoxLayout()

        # Styling Fonts
        label_font = QFont("Arial", 12)
        input_font = QFont("Arial", 10)

        # Form for Adding Item
        form_layout = QVBoxLayout()

        self.name_label = QLabel("Item Name:")
        self.name_label.setFont(label_font)
        form_layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        self.name_input.setFont(input_font)
        self.name_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.name_input)

        self.desc_label = QLabel("Description:")
        self.desc_label.setFont(label_font)
        form_layout.addWidget(self.desc_label)
        self.desc_input = QLineEdit()
        self.desc_input.setFont(input_font)
        self.desc_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.desc_input)

        self.contact_label = QLabel("Contact Info:")
        self.contact_label.setFont(label_font)
        form_layout.addWidget(self.contact_label)
        self.contact_input = QLineEdit()
        self.contact_input.setFont(input_font)
        self.contact_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.contact_input)

        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Item")
        self.add_button.setStyleSheet(self.button_style())
        self.add_button.clicked.connect(self.add_item)
        button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete Item")
        self.delete_button.setStyleSheet(self.button_style())
        self.delete_button.clicked.connect(self.delete_item)
        button_layout.addWidget(self.delete_button)

        self.display_button = QPushButton("Display Items")
        self.display_button.setStyleSheet(self.button_style())
        self.display_button.clicked.connect(self.display_items)
        button_layout.addWidget(self.display_button)

        main_layout.addLayout(button_layout)

        # Search Field
        search_layout = QHBoxLayout()
        self.search_label = QLabel("Search Item:")
        self.search_label.setFont(label_font)
        search_layout.addWidget(self.search_label)

        self.search_input = QLineEdit()
        self.search_input.setFont(input_font)
        self.search_input.setStyleSheet(self.input_style())
        search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet(self.button_style())
        self.search_button.clicked.connect(self.search_item)
        search_layout.addWidget(self.search_button)

        main_layout.addLayout(search_layout)

        # Items List
        self.items_list = QListWidget()
        self.items_list.setFont(QFont("Arial", 10))
        self.items_list.setStyleSheet(self.list_style())
        main_layout.addWidget(self.items_list)

        self.setLayout(main_layout)

    # Method to Add Item
    def add_item(self):
        name = self.name_input.text()
        description = self.desc_input.text()
        contact = self.contact_input.text()

        if not name or not description or not contact:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        item = {"name": name, "description": description, "contact": contact}
        self.items.append(item)
        self.save_items()

        self.clear_inputs()
        self.display_items()
        QMessageBox.information(self, "Success", "Item added successfully!")

    # Method to Delete Item
    def delete_item(self):
        selected_item = self.items_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Delete Error", "No item selected!")
            return

        item_name = selected_item.text().split(",")[0].split(":")[1].strip()
        self.items = [item for item in self.items if item['name'] != item_name]
        self.save_items()
        self.display_items()

    # Method to Display Items
    def display_items(self):
        self.items_list.clear()
        for item in self.items:
            self.items_list.addItem(f"Name: {item['name']}, Desc: {item['description']}, Contact: {item['contact']}")

    # Method to Search Item
    def search_item(self):
        search_term = self.search_input.text()
        if not search_term:
            QMessageBox.warning(self, "Search Error", "Enter item name or description to search!")
            return

        self.items_list.clear()
        matching_items = [item for item in self.items if
                          search_term.lower() in item['name'].lower() or search_term.lower() in item[
                              'description'].lower()]
        if matching_items:
            for item in matching_items:
                self.items_list.addItem(
                    f"Name: {item['name']}, Desc: {item['description']}, Contact: {item['contact']}")
        else:
            QMessageBox.information(self, "No Results", "No matching items found")

    # Clear input fields
    def clear_inputs(self):
        self.name_input.clear()
        self.desc_input.clear()
        self.contact_input.clear()
        self.search_input.clear()

    # Save items to JSON file
    def save_items(self):
        with open('items.json', 'w') as file:
            json.dump(self.items, file)

    # Load items from JSON file
    def load_items(self):
        if os.path.exists('items.json'):
            with open('items.json', 'r') as file:
                self.items = json.load(file)
        else:
            self.items = []

    # Style for input fields
    def input_style(self):
        return """
            QLineEdit {
                border: 1px solid #c0c0c0;
                padding: 5px;
                border-radius: 5px;
            }
        """

    # Style for buttons
    def button_style(self):
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

    # Style for list widget
    def list_style(self):
        return """
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #c0c0c0;
                padding: 5px;
                border-radius: 5px;
            }
        """


def main():
    app = QApplication(sys.argv)
    window = ItemManager()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
