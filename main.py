import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

FILE_NAME = "expenses.json"


class ExpenseTrackerApp(App):
    title = "Expense Tracker"

    def build(self):
        self.expenses = self.load_expenses()
        self.index = 0

        self.layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        self.total_label = Label(
            text="Total Expense: ₹0",
            font_size=24
        )

        self.expense_label = Label(font_size=22)
        self.category_label = Label(font_size=20)

        self.layout.add_widget(self.total_label)
        self.layout.add_widget(self.expense_label)
        self.layout.add_widget(self.category_label)

        self.add_btn = Button(text="Add Expense")
        self.delete_btn = Button(text="Delete Expense")
        self.prev_btn = Button(text="Previous")
        self.next_btn = Button(text="Next")

        self.add_btn.bind(on_press=self.add_expense)
        self.delete_btn.bind(on_press=self.delete_expense)
        self.prev_btn.bind(on_press=self.previous_expense)
        self.next_btn.bind(on_press=self.next_expense)

        self.layout.add_widget(self.add_btn)
        self.layout.add_widget(self.delete_btn)
        self.layout.add_widget(self.prev_btn)
        self.layout.add_widget(self.next_btn)

        self.update_expense()

        return self.layout

    def load_expenses(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        return []

    def save_expenses(self):
        with open(FILE_NAME, "w") as f:
            json.dump(self.expenses, f, indent=4)

    def get_total(self):
        total = 0
        for item in self.expenses:
            total += float(item["amount"])
        return total

    def update_expense(self):
        self.total_label.text = f"Total Expense: ₹{self.get_total():.2f}"

        if self.expenses:
            self.expense_label.text = (
                "Amount: ₹" + str(self.expenses[self.index]["amount"])
            )
            self.category_label.text = (
                "Category: " + self.expenses[self.index]["category"]
            )
        else:
            self.expense_label.text = "No Expenses Available"
            self.category_label.text = ""

    def add_expense(self, instance):
        amount = TextInput(
            hint_text="Amount",
            multiline=False
        )

        category = TextInput(
            hint_text="Category (Food/Travel/Shopping/Other)",
            multiline=False
        )

        box = BoxLayout(
            orientation="vertical",
            spacing=10
        )

        box.add_widget(amount)
        box.add_widget(category)

        save_btn = Button(text="Save Expense")
        box.add_widget(save_btn)

        popup = Popup(
            title="Add Expense",
            content=box,
            size_hint=(0.9, 0.7)
        )

        def save_data(btn):
            if not amount.text or not category.text:
                return

            try:
                float(amount.text)
            except:
                return

            self.expenses.append({
                "amount": amount.text,
                "category": category.text
            })

            self.save_expenses()
            self.index = len(self.expenses) - 1
            self.update_expense()
            popup.dismiss()

        save_btn.bind(on_press=save_data)
        popup.open()

    def delete_expense(self, instance):
        if not self.expenses:
            return

        self.expenses.pop(self.index)

        if self.index >= len(self.expenses):
            self.index = 0

        self.save_expenses()
        self.update_expense()

    def next_expense(self, instance):
        if self.expenses:
            self.index = (self.index + 1) % len(self.expenses)
            self.update_expense()

    def previous_expense(self, instance):
        if self.expenses:
            self.index = (self.index - 1) % len(self.expenses)
            self.update_expense()


ExpenseTrackerApp().run()