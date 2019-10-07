import json


class Recipe(object):

    def __init__(self, name, ingredients, slot):
        self.name = name
        self.ingredients = ingredients
        self.slot = slot

    def calculate_score(self):
        pass

    @staticmethod
    def load_json(file):
        with open(file, 'r') as f:
            recipe_json = json.load(f)
            recipe = Recipe(
                recipe_json['name'],
                recipe_json['ingredients'],
                recipe_json['slot']
            )
            return recipe
            