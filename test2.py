# class Dog():
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def sit(self):
#         print(self.name.title() + " is now sitting")

#     def roll_over(self):
#         print(self.name.title() + " rolled over")

# my_dog = Dog('willine',6)
# your_dog = Dog('lili',7)

# class Resturant():
#     def __init__(self, resturant_name, cuisine_type):
#         self.resturant_name = resturant_name
#         self.cuisine_type = cuisine_type
#         self.number_served = 0

#     def describe_resturant(self):
#         print("Resturant name is " + self.resturant_name)
#         print("Resturant type is " + self.cuisine_type)

#     def open_resturant(self):
#         print(self.resturant_name + "is opening")

#     def set_number_served(self, number):
#         self.number_served = number
#         print(self.number_served)

#     def increment_number_served(self,increment_number):
#         if increment_number >= 0:
#             self.number_served += increment_number
#         else:
#             print('Error')
#         print(self.number_served)

# resturant = Resturant("KFC", "open")
# resturant.number_served = 20
# resturant.set_number_served(40)
# resturant.increment_number_served(20)
# resturant.increment_number_served(-20)

# resturant1 = Resturant("lalala", "open")
# resturant2 = Resturant("bibibi", "close")
# resturant3 = Resturant("qqqeqe", "open")

# resturant1.describe_resturant()
# resturant2.describe_resturant()
# resturant3.describe_resturant()

# class User():
#     def __init__(self, first_name, last_name):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.login_attempts = 0

#     def describe_user(self):
#         print("Username is " + self.first_name.title() +
#               self.last_name.title())

#     def greet_user(self):
#         print("Welcome " + self.last_name.title())

#     def increment_login_attempts(self):
#         self.login_attempts += 1
#         print(self.login_attempts)

#     def reset_login_attempts(self):
#         self.login_attempts = 0
#         print(self.login_attempts)

# user1 = User("gu", "jin")
# user1.describe_user()
# user1.greet_user()
# user1.increment_login_attempts()
# user1.increment_login_attempts()
# user1.reset_login_attempts()


class Car():
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_descriptive_name(self):
        long_name = str(self.year) + ' ' + self.make + ' ' + self.model
        return long_name.title()

    def read_odometer(self):
        print("This car has " + str(self.odometer_reading) + " miles on it")

    def update_odometer(self, mileage):
        # self.odometer_reading = mileage
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't roll back an odometer!")

    def increment_odometer(self, miles):
        # self.odometer_reading += miles
        if miles >= 0:
            self.odometer_reading += miles
        else:
            print("You can't roll back an odometer!")

    def test(self):
        print("test")


class Battery():
    def __init__(self, battery_size=70):
        self.battery_size = battery_size

    def describe_battery(self):
        print("This car has a {}-Kwh battery".format(self.battery_size))


class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        self.battery = Battery()


# my_new_car = Car('audi', 'a4', '2016')
# print(my_new_car.get_descriptive_name())

# my_new_car.update_odometer(23500)
# my_new_car.read_odometer()
# my_new_car.increment_odometer(100)
# my_new_car.read_odometer()
my_car = ElectricCar('tesila', 'model s', 2018)
print(my_car.get_descriptive_name())
my_car.battery.describe_battery()
