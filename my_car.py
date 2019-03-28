from car import ElectricCar
# my_new_car = Car('audo','a4',2016)
# print(my_new_car.get_descriptive_name())
# my_new_car.odometer_reading=23
# my_new_car.read_odometer()

my_car = ElectricCar('tesila','model s','2016')
print(my_car.get_descriptive_name())
my_car.battery.get_range()
my_car.battery.describe_battery()
my_car.battery.get_range()