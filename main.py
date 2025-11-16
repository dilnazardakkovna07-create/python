from utils import add_record, delete_record, search_record
from darihana_class import Medicine, ResipeDariler

import numpy as np
import matplotlib.pyplot as plt


dariler = {
    "Парацетамол": Medicine("Парацетамол", 850, 20),
    "Аспирин": Medicine("Аспирин", 600, 15),
    "Ибупрофен": Medicine("Ибупрофен", 1000, 12),
    "Морфин": ResipeDariler("Морфин", 5000, 5, "Дәрігер Айдана")
}


def show_recursive(data, keys, index=0):
    """Рекурсивті түрде дәрілерді шығару"""
    if index < len(keys):
        med = data[keys[index]]
        print(f"{med.name}: {med.quantity} дана")
        show_recursive(data, keys, index + 1)


while True:
    print("\n=== Дәріхана мәзірі ===")
    print("1. Дәрі қосу")
    print("2. Дәріні жою")
    print("3. Дәріні іздеу")
    print("4. Қорды көру (рекурсивті)")
    print("5. Дәрі сату (класс арқылы)")
    print("6. Файлға сақтау")
    print("7. Файлдан оқу")
    print("8. Шығу")
    print("9. NumPy сатылым анализі")
    print("10. Matplotlib график салу")

    choice = input("Таңдауыңызды енгізіңіз (1-10): ")

    try:
        if choice == "1":
            name = input("Қосылатын дәрі атауы: ")
            price = int(input("Бағасы: "))
            qty = int(input("Саны: "))

            dariler[name] = Medicine(name, price, qty)
            print(f"{name} базада тіркелді.")

        elif choice == "2":
            name = input("Жойылатын дәрі атауы: ")
            if name in dariler:
                del dariler[name]
                print(f"{name} жойылды.")
            else:
                print("Мұндай дәрі жоқ.")

        elif choice == "3":
            name = input("Іздейтін дәрі атауы: ")
            found = False
            for med in dariler.values():
                if name.lower() in med.name.lower():
                    med.info()
                    found = True
            if not found:
                print("Мұндай дәрі табылмады.")

        elif choice == "4":
            print("\n=== Қордағы дәрілер ===")
            show_recursive(dariler, list(dariler.keys()))

        elif choice == "5":
            name = input("Сатылатын дәрі атауы: ")
            if name in dariler:
                amount = int(input("Саны: "))
                drug = dariler[name]

                if isinstance(drug, ResipeDariler):
                    drug.show_prescription()

                drug.sell(amount)
            else:
                print("Мұндай дәрі жоқ.")

        elif choice == "6":
            with open("dariler.txt", "w", encoding="utf-8") as f:
                for med in dariler.values():
                    f.write(f"{med.name}: {med.quantity} дана, баға: {med.price}\n")
            print("Файлға сақталды.")

        elif choice == "7":
            try:
                with open("dariler.txt", "r", encoding="utf-8") as f:
                    print(f.read())
            except FileNotFoundError:
                print("Файл табылмады.")

        elif choice == "8":
            print("Бағдарлама аяқталды.")
            break

        elif choice == "9":
            print("\n=== NumPy көмегімен сатылым анализі ===")

            sales = np.array([120, 150, 170, 160, 200, 230])

            print("6 айдағы сатылым:", sales)
            print("Орташа мән:", np.mean(sales))
            print("Максимум:", np.max(sales))
            print("Минимум:", np.min(sales))
            print("Стандартты ауытқу:", np.std(sales))

        elif choice == "10":
            print("\nГрафик салынуда...")

            months = ["Қаңт", "Ақп", "Наур", "Сәу", "Мам", "Мау"]
            sales = np.array([120, 150, 170, 160, 200, 230])

            plt.plot(months, sales, marker='o')
            plt.title("Айлар бойынша Парацетамол сатылым динамикасы")
            plt.xlabel("Айлар")
            plt.ylabel("Сатылым саны")
            plt.grid(True)
            plt.show()

        else:
            print("Қате таңдау!")

    except ValueError:
        print("Қате енгізу! Сан енгізіңіз.")
