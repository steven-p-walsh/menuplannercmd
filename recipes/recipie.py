import json, random, itertools


class Recipe(object):

    def __init__(self, category_name, name, ingredients, slot, recipe_type, favorability, frequency):
        self.category_name = category_name
        self.name = name
        self.ingredients = ingredients
        self.slot = slot
        self.frequency = frequency
        self.recipe_type = recipe_type

        # if the item has no favorability score this will
        # Generate a random score, this
        # is necessary for un-rated recipes which might
        # want to make their way into the plan
        #
        # because I want to increase the likelyhood that new 
        # recipes will be bumped up, i'm starting at 50
        self.favorability_score = favorability if favorability is not None else random.randint(50,100)

    def __get_ingredient_score__(self, recipe_db, pantry_items, week_items):
        ingredient_names = [ x['name'] for x in self.ingredients ]
        total = 0
        for ingredient in ingredient_names:
            
            # skip if already in pantry
            if ingredient in pantry_items:
                continue

            # skip if another recipe has included
            if ingredient in week_items:
                continue

            if ingredient not in recipe_db.mappings:
                raise Exception('Could not find a mapping for %s as specified in %s' % (ingredient, self.name))

            mapping = recipe_db.mappings[ingredient]
            
            # this is not a mapped ingredient
            if 'points' in mapping:
                total = total + mapping['points']
        
        return total

    def calculate_score(self, context):
        score = 0
        pantry_items = context['pantry']
        recipe_db = context['recipe_db']
        week_list = [ x for x in context['items'] if x is not self ]
        week_items = list(set(list(week_list)))

        # STEP 1
        # let's sum the cost of all ingredients minus items in our pantry
        # or items which are duplicated from previous menu items.
        #
        # we're removing previously added items because there's an in-built
        # assumption that we can get discounts if we buy in greater quantities
        ing_names = [ x['name'] for x in self.ingredients ]
        unique_points = self.__get_ingredient_score__(recipe_db, pantry_items, week_items)
        ingredient_score = unique_points * 1.5
        
        # STEP 2
        # Let's adjust the favorability score to the unique ingredients score
        score = self.favorability_score - ingredient_score

        # STEP 3
        # lets sum the nutritional score from each ingredient
        # this should be from the full list, not the reduced list

        # STEP 4
        # Adjust based on frequency
        return score

            