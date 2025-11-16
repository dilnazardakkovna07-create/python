
def add_record(database, name, qty):
    database[name] = qty
    print(f"{name} дәрісі {qty} данамен қосылды.")
    return database


def delete_record(database, name):
    if name in database:
        del database[name]
        print(f"{name} дәрісі жойылды.")
    else:
        print("Мұндай дәрі табылмады.")
    return database


def search_record(database, name):
    for med in database:
        if name.lower() in med.lower():
            print(f"{med} дәріханада бар.")
            return True
    print("Мұндай дәрі табылмады.")
    return False