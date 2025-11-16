class Medicine:

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def sell(self, amount):
        """Дәрі сату"""
        if amount <= self.quantity:
            self.quantity -= amount
            total = amount * self.price
            print(f"{amount} дана {self.name} сатылды. Жалпы: {total} тг")
            return total
        else:
            print("Қорда жеткілікті дәрі жоқ!")
            return 0

    def info(self):
        """Дәрі туралы ақпарат"""
        print(f"{self.name}: {self.price} тг, қор: {self.quantity} дана")


class ResipeDariler(Medicine):

    def __init__(self, name, price, quantity, doctor_name):
        super().__init__(name, price, quantity)
        self.doctor_name = doctor_name

    def show_prescription(self):
        print(f"{self.name} дәрісін тек {self.doctor_name} рецептімен алуға болады.")
