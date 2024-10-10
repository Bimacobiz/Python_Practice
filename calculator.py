#!/usr/bin/env python3

import sys
import math
import re
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
    QGridLayout  # Add QGridLayout import here
)

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simple Calculator')
        self.setGeometry(100, 100, 400, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create the display for the calculator
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)

        # Create buttons for the calculator
        self.create_buttons()
        
        # Show the window
        self.show()

    def create_buttons(self):
        # Create a grid layout for the buttons
        button_layout = QGridLayout()

        # Button labels
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+',
            'sin', 'cos', 'tan', 'sqrt',
            'pi', 'e', '(', ')'
        ]

        # Create buttons and add to the layout
        for i, button in enumerate(buttons):
            btn = QPushButton(button)
            btn.clicked.connect(lambda _, b=button: self.on_button_click(b))
            button_layout.addWidget(btn, i // 4, i % 4)

        self.layout.addLayout(button_layout)

    def on_button_click(self, button):
        if button == '=':
            self.evaluate_expression()
        elif button == 'C':
            self.display.clear()
        else:
            current_text = self.display.text()
            self.display.setText(current_text + button)

    def evaluate_expression(self):
        expression = self.display.text()
        processed_input = self.preprocess_input(expression)

        try:
            result = self.calculator(processed_input)
            self.display.setText(str(result))
        except Exception as e:
            self.show_error_message(f"Error in evaluating expression: {e}")

    def calculator(self, expression):
        # Allowed functions and constants
        allowed_names = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'log': math.log,
            'pi': math.pi,
            'e': math.e
        }

        # Input sanitization
        expression = expression.replace(' ', '')

        return eval(expression, {"__builtins__": None}, allowed_names)

    def preprocess_input(self, user_input):
        # Regular expression to match function names followed by a space and a number
        pattern = re.compile(r'(sin|cos|tan|sqrt|log)\s*(-?\d+\.?\d*)')
        processed_input = re.sub(pattern, r'\1(\2)', user_input)
        return processed_input

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    sys.exit(app.exec_())

