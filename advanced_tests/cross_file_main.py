from cross_file_utils import validate_age

class Person:
    def __init__(self, age):
        self.age = validate_age(age)