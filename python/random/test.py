
class animal:
    def __init__(self):
        self.animalName = 'animal'
        self.sound = 'generic animal name'

    def what_is_animal(self):
        return 'an animal is a mammal'

class dog(animal):
    def __init__(self):
        super().__init__()
        self.animalName = 'dog'
        self.sound = 'woof'

cat = dog()
animal_cat: animal = cat


print(cat.what_is_animal())