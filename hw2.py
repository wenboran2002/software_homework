import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QListWidget, QMessageBox, QComboBox, QFormLayout)
from PyQt5.QtGui import QFont


class ItemManager(QWidget):
    def __init__(self):
        super().__init__()
        self.items = []
        self.initUI()
        self.load_items()

    def initUI(self):
        # 主窗口设置
        self.setWindowTitle("物品复活软件")
        self.setStyleSheet("background-color: #f4f4f4;")
        self.resize(1200, 600)

        # 主布局
        main_layout = QVBoxLayout()

        # 字体样式
        label_font = QFont("Arial", 12)
        input_font = QFont("Arial", 10)

        # 添加物品表单
        form_layout = QVBoxLayout()

        self.name_label = QLabel("物品名称：")
        self.name_label.setFont(label_font)
        form_layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        self.name_input.setFont(input_font)
        self.name_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.name_input)

        self.desc_label = QLabel("描述：")
        self.desc_label.setFont(label_font)
        form_layout.addWidget(self.desc_label)
        self.desc_input = QLineEdit()
        self.desc_input.setFont(input_font)
        self.desc_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.desc_input)

        self.contact_label = QLabel("联系方式：")
        self.contact_label.setFont(label_font)
        form_layout.addWidget(self.contact_label)
        self.contact_input = QLineEdit()
        self.contact_input.setFont(input_font)
        self.contact_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.contact_input)

        # 新增：类别选择器
        self.category_label = QLabel("类别：")
        self.category_label.setFont(label_font)
        form_layout.addWidget(self.category_label)
        self.category_input = QComboBox()
        self.category_input.setFont(input_font)
        self.category_input.setStyleSheet(self.input_style())
        self.category_input.addItems(["食品", "书籍", "工具", "服装", "电子产品"])
        self.category_input.currentIndexChanged.connect(self.update_category_fields)  # 连接到更新字段
        form_layout.addWidget(self.category_input)

        # 动态表单布局，用于类别特定的输入项
        self.dynamic_form_layout = QFormLayout()
        form_layout.addLayout(self.dynamic_form_layout)

        main_layout.addLayout(form_layout)

        # 按钮
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("添加物品")
        self.add_button.setStyleSheet(self.button_style())
        self.add_button.clicked.connect(self.add_item)
        button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("删除物品")
        self.delete_button.setStyleSheet(self.button_style())
        self.delete_button.clicked.connect(self.delete_item)
        button_layout.addWidget(self.delete_button)

        self.display_button = QPushButton("显示物品")
        self.display_button.setStyleSheet(self.button_style())
        self.display_button.clicked.connect(self.display_items)
        button_layout.addWidget(self.display_button)

        main_layout.addLayout(button_layout)

        # 搜索框
        search_layout = QHBoxLayout()
        self.search_label = QLabel("搜索物品：")
        self.search_label.setFont(label_font)
        search_layout.addWidget(self.search_label)

        self.search_input = QLineEdit()
        self.search_input.setFont(input_font)
        self.search_input.setStyleSheet(self.input_style())
        search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("搜索")
        self.search_button.setStyleSheet(self.button_style())
        self.search_button.clicked.connect(self.search_item)
        search_layout.addWidget(self.search_button)

        main_layout.addLayout(search_layout)

        # 物品列表
        self.items_list = QListWidget()
        self.items_list.setFont(QFont("Arial", 10))
        self.items_list.setStyleSheet(self.list_style())
        main_layout.addWidget(self.items_list)

        self.setLayout(main_layout)

    # 添加物品方法
    def add_item(self):
        name = self.name_input.text()
        description = self.desc_input.text()
        contact = self.contact_input.text()
        category = self.category_input.currentText()
        additional_info = self.get_additional_info()

        if not name or not description or not contact:
            QMessageBox.warning(self, "输入错误", "所有字段都是必填的！")
            return

        item = {"name": name, "description": description, "contact": contact, "category": category}
        print('add',additional_info)
        # 添加类别特定的属性
        print('cat',category)
        if category == "食品":
            item["保质期"] = additional_info.get("保质期", "")
            item["数量"] = additional_info.get("数量", "")
        elif category == "书籍":
            item["作者"] = additional_info.get("作者", "")
            item["出版社"] = additional_info.get("出版社", "")
            item["页数"] = additional_info.get("页数", "")
        elif category == "工具":
            print('in')
            print(additional_info["状态"])
            item["状态"] = additional_info.get("状态", "")
        elif category == "服装":

            item["尺寸"] = additional_info.get("尺寸", "")
        elif category == "电子产品":
            item["保修期"] = additional_info.get("保修期", "")

        self.items.append(item)
        print(self.items)
        self.save_items()

        self.clear_inputs()
        self.display_items()
        QMessageBox.information(self, "成功", "物品添加成功！")

    # 删除物品方法
    def delete_item(self):
        selected_item = self.items_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "删除错误", "没有选中物品！")
            return

        item_name = selected_item.text().split(",")[0].split(":")[1].strip()
        self.items = [item for item in self.items if item['name'] != item_name]
        self.save_items()
        self.display_items()

    # 显示物品方法
    def display_items(self):
        self.items_list.clear()
        for item in self.items:
            item_display = f"名称: {item['name']}, 描述: {item['description']}, 联系方式: {item['contact']}, 类别: {item['category']}"

            # Add category-specific attributes to the display
            if item['category'] == "食品":
                item_display += f", 保质期: {item.get('保质期', '')}, 数量: {item.get('数量', '')}"
            elif item['category'] == "书籍":
                item_display += f", 作者: {item.get('作者', '')}, 出版社: {item.get('出版社', '')}, 页数: {item.get('页数', '')}"
            elif item['category'] == "工具":
                item_display += f", 状态: {item.get('状态', '')}"
            elif item['category'] == "服装":
                item_display += f", 尺寸: {item.get('尺寸', '')}"
            elif item['category'] == "电子产品":
                item_display += f", 保修期: {item.get('保修期', '')}"

            # Add the formatted item to the list
            self.items_list.addItem(item_display)

    # 搜索物品方法
    def search_item(self):
        search_term = self.search_input.text()
        if not search_term:
            QMessageBox.warning(self, "搜索错误", "请输入物品名称或描述进行搜索！")
            return

        self.items_list.clear()
        matching_items = [item for item in self.items if
                          search_term.lower() in item['name'].lower() or search_term.lower() in item['description'].lower()]
        if matching_items:
            for item in matching_items:
                self.items_list.addItem(
                    f"名称: {item['name']}, 描述: {item['description']}, 联系方式: {item['contact']}, 类别: {item['category']}")
        else:
            QMessageBox.information(self, "无结果", "未找到匹配的物品")

    # 更新类别特定字段
    def update_category_fields(self):
        category = self.category_input.currentText()
        # 清除现有的动态字段
        for i in range(self.dynamic_form_layout.count()):
            item = self.dynamic_form_layout.itemAt(i).widget()
            if item is not None:
                item.deleteLater()

        # 添加类别特定字段
        if category == "食品":
            self.dynamic_form_layout.addRow("保质期:", QLineEdit())
            self.dynamic_form_layout.addRow("数量:", QLineEdit())
        elif category == "书籍":
            self.dynamic_form_layout.addRow("作者:", QLineEdit())
            self.dynamic_form_layout.addRow("出版社:", QLineEdit())
            self.dynamic_form_layout.addRow("页数:", QLineEdit())
        elif category == "工具":
            self.dynamic_form_layout.addRow("状态:", QLineEdit())
        elif category == "服装":
            self.dynamic_form_layout.addRow("尺寸:", QLineEdit())
        elif category == "电子产品":
            self.dynamic_form_layout.addRow("保修期:", QLineEdit())

    # 获取类别特定的附加信息
    def get_additional_info(self):
        additional_info = {}
        for i in range(self.dynamic_form_layout.count()):
            item = self.dynamic_form_layout.itemAt(i).widget()
            if isinstance(item, QLineEdit):

                label = self.dynamic_form_layout.itemAt(i - 1).widget()
                if isinstance(label, QLabel):
                    additional_info[label.text()[:-1]] = item.text()

        return additional_info

        # 清空输入字段
    def clear_inputs(self):
        self.name_input.clear()
        self.desc_input.clear()
        self.contact_input.clear()
        self.search_input.clear()
        self.category_input.setCurrentIndex(0)
        self.update_category_fields()

    # 将物品保存到 JSON 文件
    def save_items(self):
        with open('items.json', 'w') as file:
            json.dump(self.items, file)

    # 从 JSON 文件加载物品
    def load_items(self):
        if os.path.exists('items.json'):
            with open('items.json', 'r') as file:
                self.items = json.load(file)
        else:
            self.items = []

    # 输入框的样式
    def input_style(self):
        return """
                    QLineEdit {
                        border: 1px solid #c0c0c0;
                        padding: 5px;
                        border-radius: 5px;
                    }
                """

    # 按钮的样式
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

    # 列表框的样式
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
