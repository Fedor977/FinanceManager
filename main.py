import os
import csv
from datetime import datetime

FINANCES_FILE = "finances.csv"


class FinanceManager:
    def __init__(self, data_file=FINANCES_FILE):
        self.data_file = data_file
        self.records = []
        self.load_records()

    def load_records(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                reader = csv.DictReader(file)
                self.records = list(reader)
        else:
            print(f"Файл {self.data_file} не найден.")

    def save_records(self):
        with open(self.data_file, "w", encoding='utf-8') as file:
            headers = ["date", "category", "amount", "description"]
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.records)

    def add_record(self, category, amount, description):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.records.append({"date": date, "category": category, "amount": amount, "description": description})
        self.save_records()

    def edit_record(self, index, category, amount, description):
        if 0 <= index < len(self.records):
            self.records[index]["category"] = category
            self.records[index]["amount"] = amount
            self.records[index]["description"] = description
            self.save_records()
            print("Запись успешно отредактирована.")
        else:
            print("Индекс записи недействителен.")

    def show_balance(self):
        incomes = sum(float(record["amount"]) for record in self.records if record["category"] == "доход")
        expenses = sum(float(record["amount"]) for record in self.records if record["category"] == "расход")
        balance = incomes - expenses
        print(f"Текущий баланс: {balance}")
        print(f"Всего доходов: {incomes}")
        print(f"Всего расходов: {expenses}")

    def search_records(self, category=None, date=None, amount=None):
        results = []
        for record in self.records:
            date_match = date is None or record["date"].split()[0] == date
            category_match = category is None or record["category"] == category
            amount_match = amount is None or float(record["amount"]) == float(amount)
            if date_match and category_match and amount_match:
                results.append(record)
        return results

    def print_records(self):
        for i, record in enumerate(self.records):
            print(
                f"{i + 1}. Дата: {record['date']}, Категория: {record['category']}, Сумма: {record['amount']}, Описание: {record['description']}")


if __name__ == "__main__":
    manager = FinanceManager()

    while True:
        print("\n1. Показать баланс")
        print("2. Добавить запись")
        print("3. Редактировать запись")
        print("4. Поиск записей")
        print("5. Выход")
        choice = input("Выберите опцию: ")

        if choice == "1":
            manager.show_balance()
        elif choice == "2":
            category = input("Введите категорию (доход/расход): ")
            amount = input("Введите сумму: ")
            description = input("Введите описание: ")
            manager.add_record(category, amount, description)
            print("Запись успешно добавлена.")
        elif choice == "3":
            manager.print_records()
            index = int(input("Введите номер записи для редактирования: ")) - 1
            category = input("Введите новую категорию (доход/расход): ")
            amount = input("Введите новую сумму: ")
            description = input("Введите новое описание: ")
            manager.edit_record(index, category, amount, description)
        elif choice == "4":
            category = input("Введите категорию (доход/расход) или оставьте пустым: ")
            date = input("Введите дату (ГГГГ-ММ-ДД) или оставьте пустым: ")
            amount = input("Введите сумму или оставьте пустым: ")
            if date:
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    print("Неверный формат даты. Используйте формат ГГГГ-ММ-ДД.")
                    continue
            results = manager.search_records(category, date, amount)
            if results:
                print("Результаты поиска:")
                for record in results:
                    print(record)
            else:
                print("Записи не найдены.")
        elif choice == "5":
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
