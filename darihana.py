import sqlite3

conn = sqlite3.connect("darihana.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_name TEXT UNIQUE,
    country TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category_id INTEGER,
    manufacturer_id INTEGER,
    price INTEGER,
    quantity INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)
)
""")

conn.commit()


def insert_initial_data():
    categories = [
        "Ауырсынуды басатын",
        "Қызу түсіретін",
        "Антибиотик",
        "Жүрек дәрілері",
    ]
    manufacturers = [
        ("Bayer", "Germany"),
        ("Pfizer", "USA"),
        ("Novartis", "Switzerland"),
        ("SANTO", "Kazakhstan"),
    ]
    medicines = [
        ("Парацетамол", "Қызу түсіретін", "SANTO", 850, 40),
        ("Ибупрофен", "Ауырсынуды басатын", "Pfizer", 950, 30),
        ("Аспирин", "Ауырсынуды басатын", "Bayer", 600, 25),
        ("Амоксициллин", "Антибиотик", "Novartis", 2500, 20),
        ("Нитроглицерин", "Жүрек дәрілері", "SANTO", 700, 15),
    ]

    for c in categories:
        cursor.execute("INSERT OR IGNORE INTO categories(category_name) VALUES (?)", (c,))

    for m in manufacturers:
        cursor.execute(
            "INSERT OR IGNORE INTO manufacturers(manufacturer_name, country) VALUES (?, ?)",
            m,
        )

    for name, cat, man, price, qty in medicines:
        cursor.execute("SELECT id FROM medicines WHERE name=?", (name,))
        if cursor.fetchone():
            continue

        cursor.execute("SELECT id FROM categories WHERE category_name=?", (cat,))
        cat_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM manufacturers WHERE manufacturer_name=?", (man,))
        man_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO medicines(name, category_id, manufacturer_id, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (name, cat_id, man_id, price, qty))

    conn.commit()


insert_initial_data()


def show_categories():
    cursor.execute("SELECT * FROM categories")
    for row in cursor.fetchall():
        print(row)


def show_manufacturers():
    cursor.execute("SELECT * FROM manufacturers")
    for row in cursor.fetchall():
        print(row)


def show_all_medicines():
    cursor.execute("""
        SELECT medicines.name, categories.category_name, manufacturers.manufacturer_name,
               price, quantity
        FROM medicines
        JOIN categories ON medicines.category_id = categories.id
        JOIN manufacturers ON medicines.manufacturer_id = manufacturers.id
    """)
    rows = cursor.fetchall()
    print("\n=== Аптекадағы барлық дәрілер ===")
    for row in rows:
        print(f"{row[0]} | Категория: {row[1]} | Өндіруші: {row[2]} | Баға: {row[3]} | Қор: {row[4]} дана")


def add_medicine():
    name = input("Дәрі атауы: ")
    category = input("Категория: ")
    manufacturer = input("Өндіруші: ")
    price = int(input("Баға: "))
    quantity = int(input("Саны: "))

    cursor.execute("SELECT id FROM categories WHERE category_name=?", (category,))
    cat = cursor.fetchone()
    if not cat:
        cursor.execute("INSERT INTO categories(category_name) VALUES (?)", (category,))
        cat_id = cursor.lastrowid
    else:
        cat_id = cat[0]

    cursor.execute("SELECT id FROM manufacturers WHERE manufacturer_name=?", (manufacturer,))
    man = cursor.fetchone()
    if not man:
        country = input("Ел: ")
        cursor.execute("INSERT INTO manufacturers(manufacturer_name, country) VALUES (?, ?)", (manufacturer, country))
        man_id = cursor.lastrowid
    else:
        man_id = man[0]

    cursor.execute("""
        INSERT INTO medicines(name, category_id, manufacturer_id, price, quantity)
        VALUES (?, ?, ?, ?, ?)
    """, (name, cat_id, man_id, price, quantity))

    conn.commit()
    print("Дәрі қосылды!")


def delete_medicine():
    name = input("Жойылатын дәрі: ")
    cursor.execute("DELETE FROM medicines WHERE name=?", (name,))
    conn.commit()
    print("Дәрі жойылды!")


def sell_medicine():
    name = input("Сатылатын дәрі: ")
    qty = int(input("Саны: "))

    cursor.execute("SELECT quantity, price FROM medicines WHERE name=?", (name,))
    med = cursor.fetchone()

    if not med:
        print("Мұндай дәрі жоқ!")
        return

    if qty > med[0]:
        print("Қорда жеткілікті дәрі жоқ!")
        return

    new_qty = med[0] - qty
    total = qty * med[1]

    cursor.execute("UPDATE medicines SET quantity=? WHERE name=?", (new_qty, name))
    conn.commit()

    print(f"{qty} дана сатылды. Жалпы: {total} тг")


while True:
    print("\n=========== М Е Н Ю ===========")
    print("1 — Барлық дәрілер")
    print("2 — Категориялар")
    print("3 — Өндірушілер")
    print("4 — Дәрі қосу")
    print("5 — Дәрі жою")
    print("6 — Дәрі сату")
    print("0 — Шығу")

    choice = input("Таңдау: ")

    if choice == "1":
        show_all_medicines()
    elif choice == "2":
        show_categories()
    elif choice == "3":
        show_manufacturers()
    elif choice == "4":
        add_medicine()
    elif choice == "5":
        delete_medicine()
    elif choice == "6":
        sell_medicine()
    elif choice == "0":
        print("Бағдарлама аяқталды.")
        break
    else:
        print("Қате таңдау!")

conn.close()     