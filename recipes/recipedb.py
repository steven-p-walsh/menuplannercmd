import random, json


class RecipeDb(object):

    def __init__(self):
        self.recipes = {}
        self.entrees = {} # we do not want to suggest sauces and stocks

    def add_recipe(self, recipe):
        key = '%s.%s' % (recipe.category_name, recipe.name)
        if key not in self.recipes:
            self.recipes[key] = recipe
            if recipe.recipe_type == 'entree':
                self.entrees[key] = recipe
        else:
            raise Exception('Error adding recipe, duplicate recipe %s' % key)

    def entree_count(self):
        return len(self.entrees.keys())

    def get_random_recipe(self):
        key = random.choice(list(self.entrees.keys()))
        return self.entrees[key]