import random


class MenuGenerator(object):

    def __init__(self, recipe_db, pantry_items, recipe_count, iteration_count):
        self.pantry = pantry_items
        self.recipe_db = recipe_db
        self.recipe_count = recipe_count
        self.iteration_count = iteration_count

    def ___mutate_iteration__(self, iteration):
        # try replacing one of the recipes
        new_recipe = None
        while new_recipe is None:
            new_recipe = self.recipe_db.get_random_recipe()
            if new_recipe in iteration['items']:
                new_recipe = None
        iteration['items'][random.randint(0, self.recipe_count - 1)] = new_recipe

        # try replacing an optional or replacable ingredient in a recipe
        return iteration

    def __setup_iteration__(self, best_iteration = None, first_items = []):
        context = { 
            'recipe_db': self.recipe_db, 
            'items': first_items if best_iteration is None else best_iteration['items'].copy(), 
            'pantry': self.pantry, 
            'score': -1 
        }
        return context
    
    def __run_iteration__(self, iteration):
        iteration = self.___mutate_iteration__(iteration)
        # calculate the individual score for each item
        total_score = sum(map(lambda x: x.calculate_score(iteration), iteration['items']))
        iteration['score'] = total_score
        return iteration

    def __fetch_items__(self, item_count):
        items = []
        while len(items) < item_count:
            random_recipe = self.recipe_db.get_random_recipe()
            if random_recipe not in items:
                items.append(random_recipe)
        return items

    def run(self):
        # don't try to build a menu larger than we have source recipes
        if self.recipe_db.entree_count() < self.recipe_count:
            raise Exception("Recipe database is too small for requested recipe count")

        # setup the initial menu, and iteration
        first_items = self.__fetch_items__(self.recipe_count)
        iteration = self.__setup_iteration__(None, first_items)
        best_iteration = self.__run_iteration__(iteration)

        # Run through several iterations
        for i in range(0, self.iteration_count):
            iteration = self.__setup_iteration__(best_iteration)
            iteration = self.__run_iteration__(iteration)
            # if the score of the new iteration is better, let's use it
            if iteration['score'] > best_iteration['score']:
                best_iteration = iteration
        
        # we've got our best menu
        return best_iteration