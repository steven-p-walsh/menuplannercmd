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

    def get_ingredients_list(self):
        all_ingredients = []
        for ingredient_list in map(lambda x: x.ingredients, self.recipes.values()):
            all_ingredients = all_ingredients + list(map(lambda x: x['name'], ingredient_list))
        return all_ingredients

    def entree_count(self):
        return len(self.entrees.keys())

    def get_random_recipe(self):
        key = random.choice(list(self.entrees.keys()))
        return self.entrees[key]