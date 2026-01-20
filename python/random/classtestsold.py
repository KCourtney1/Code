import datetime

class account:

    interest = 0.02

    def __init__(self,name):
        self.holder = name
        self.balance = 0
        self.account_type = account
    
    def deposit(self, amount):
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount):
        if amount > self.balance:
            return "you a broke ass bitch"
        self.balance -= amount
        return self.balance
    
class checkingAccount(account):

    withdraw_fee = 1
    interest = 0.01

    def __init__(self, name, birthdate= "01/01/1999"):
        super().__init__(name)
        self.account_type = checkingAccount

    @property
    def age(self):
        today = datetime.date.today()
        month,day,year = self.birthdate.split("/")
        age = today.year - int(year)

        if today < datetime.dat(today.year,int(month),int(day)):
            age-=1
        return age

    def withdraw(self, amount):
        if self.age >21:
            return account.withdraw(self, amount+self.withdraw_fee)
        return "not old enough"
    
class bankAccount:

    def __init__(self):
        self.accounts = []
    
    def openAcount(self, name, amount, account_type = account):
        customer = account_type(name) #creating instance of selected account type
        customer.deposit(amount)
        self.accounts.append(customer)
        return customer
    
    def payinterest(self):
        for customers in self.accounts:
            customers.deposit(customers.balance*customers.interest)

class pet:
    def __init__(self,name):
        self.name = name
        self.is_alive = True
    
    def eat(self, item = "thing"):
        return f"{self.name} is eating {item}(s)."
    
    def talk(self):
        return f"{self.name} can't talk"
    
    def pet(self):
        return f"you pet {self.name}"
    
class dog(pet):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed 

    def talk(self):
        return "woof woof"
    
class time:
    def __init__(self, hour=0, minute=0, second=0):
        self.__hour = hour
        self.minute = minute
        self.second = second
    def __str__(self) -> str:
        return f'{self.__hour}:{self.minute}:{self.second}'
    def sethour(self,hour):
        self.__hour = hour
    
class food:
    def __init__(self, name, price_per_unit):
        self.name = name
        self.price_per_unit = price_per_unit
    def cost(self):
        return self.price_per_unit
    
class Tray:
    def __init__(self):
        self.items = []
    
    def add_to_tray(self, food_item):
        self.items.append(food_item)
    
    def __str__(self):
        str_repr = [] 
        for food_item in self.items:
            str_repr.append(food_item.name)
        return 'Tray contents: ' + ', '.join(str_repr)
    __repr__ = __str__
    
class main_dishes(food):
    def __init__(self, name, price_per_unit, is_seasonal = False):
        super().__init__(name, price_per_unit)
        self.is_seasonal = is_seasonal

    def cost(self):
        if self.is_seasonal:
            return self.price_per_unit*0.85
        return self.price_per_unit
    
class snack(food):
    def __init__(self, name, price_per_unit, type=""):
        super().__init__(name, price_per_unit)
        self.type = type

class drink(food):
    def __init__(self, name, price_per_unit):
        super().__init__(name, price_per_unit)

class hot_drinks(food):
    def __init__(self, name, price_per_unit,HOT_CUP_PRICE=0):
        super().__init__(name, price_per_unit)
        self.HOT_CUP_PRICE = HOT_CUP_PRICE

    def cost(self):
        return self.price_per_unit + self.HOT_CUP_PRICE
    
class plate:
    def __init__(self,item) -> None:
        self.items = []

    def add_to_plate(self,food_item):
        if len(self.items) < 2:
            self.items.append(food_item)
            return "added succesfully"
        return "your plate is full"



def main():
    # pnc = bankAccount() #creates a new back with no customers
    # pnc.openAcount("allen",1000) #opens an new account in the bank created
    # pnc.openAcount("filop",1000, checkingAccount)
    #print(f"{pnc.accounts[0].holder} : {pnc.accounts[0].balance}: {pnc.accounts[0].account_type}")
    #print(f"{pnc.accounts[1].holder} : {pnc.accounts[1].balance}: {pnc.accounts[1].account_type}")
    #pnc.payinterest()
    #print(f"{pnc.accounts[0].holder} : {pnc.accounts[0].balance}")
    #print(f"{pnc.accounts[1].holder} : {pnc.accounts[1].balance}")

    # a = dog("yoda","chuwawa")
    # print(a.talk())
    # print(a.eat("shoe"))
    # print(a.pet())

    steak = main_dishes("steak",)
    print(issubclass(plate,food))


main()