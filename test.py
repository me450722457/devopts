class Person():
    def __init__(self,person_list):
        self.person_list=person_list
    
    def __str__(self):
        return str(self.person_list)

person_list=["andy","xiuwu","maggie"]
person=Person(person_list)
print(person)