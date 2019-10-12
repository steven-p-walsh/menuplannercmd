import json, random, itertools
from datetime import datetime

class Recipe(object):

    frequencies = {
        'weekly': 7,
        'semi-monthly': 14,
        'monthly': 30,
        'seasonally': 90,
    }

    def __init__(self, category_name, name, ingredients, slots, recipe_type, favorability, frequency):
        self.category_name = category_name
        self.name = name
        self.ingredients = ingredients
        self.slot_count = slots
        self.frequency = frequency
        self.recipe_type = recipe_type
        self.last_made = None

        # if the item has no favorability score this will
        # Generate a random score, this
        # is necessary for un-rated recipes which might
        # want to make their way into the plan
        #
        # because I want to increase the likelyhood that new 
        # recipes will be bumped up, i'm starting at 50
        self.favorability_score = favorability if favorability is not None else random.randint(50,100)

    def __get_ingredient_score__(self, recipe_db, pantry_items, week_items, boosted_ingredients):
        total = 0
        ingredient_names = [ x['name'] for x in self.ingredients ]
        for ingredient in ingredient_names:
            # we can't score the ingredient, if we don't have a mapping
            if ingredient not in recipe_db.mappings:
                raise Exception('Could not find a mapping for %s as specified in %s' % (ingredient, self.name))

            mapping = recipe_db.mappings[ingredient] 

            # this ingredient is in the boosted list, so we're going to give a discount
            # to this ingredient.  it does not necessairly need to be in the pantry
            # so we need to evaluate it before we evaluate the pantry
            if ingredient in boosted_ingredients:
                total = total - 10

            # skip if already in pantry
            if ingredient in pantry_items:
                continue

            # skip if another recipe has included
            if ingredient in week_items:
                # there is a penalty for having this appear more than once a menu
                if 'grouppenalty' in mapping:
                    total = total + mapping['grouppenalty']
                else:
                    # skip the rest
                    continue

            # this is not a mapped ingredient
            if 'points' in mapping:
                total = total + mapping['points']
        
        return total

    def __calculate_historical_adjustment__(self):
        # no historical data available
        if self.last_made is None:
            return 0

        days = (datetime.now() - self.last_made).days
        frequency_value = Recipe.frequencies[self.frequency]
        max_adjustment = 50
        min_adjustment = -30

        # this should calculate a simple negatively
        # sloped line.  The adjustment will be
        # removed from the score to reduce the chance of a recipe from
        # being picked more then the designated frequency linearly to how
        # much time  has passed since the last time it was picked
        #
        # however, it should also work the opposite direction.
        # if a recipe has gone awhile without coming up
        # the value will be negative, and should boost the score

        x1 = 1 
        y1 = max_adjustment

        x2 = frequency_value
        y2 = 0

        m = (y2 - y1) / (x2 - x1)
        adjustment = m * days + y1

        # check against the limits, and return
        return adjustment if adjustment > min_adjustment else min_adjustment

    def calculate_score(self, context):
        score = 0
        pantry_items = context['pantry']
        recipe_db = context['recipe_db']
        boosted_ingredients = context['boosted_ingredients']
        item_ingredients = [ x.ingredients for x in context['items'] if x is not self ]
        all_ingredients = list(itertools.chain.from_iterable(item_ingredients))
        week_ingredient_names = list(set([ x['name'] for x in all_ingredients ]))

        # STEP 1
        # let's sum the cost of all ingredients minus items in our pantry
        # or items which are duplicated from previously selected menu items.
        #
        # we're removing previously added items because there's an in-built
        # assumption that we can get discounts if we buy in greater quantities
        ingredient_score = self.__get_ingredient_score__(
            recipe_db, 
            pantry_items, 
            week_ingredient_names, 
            boosted_ingredients
        )
        
        # STEP 2
        # Let's adjust the favorability score to the unique ingredients score
        score = self.favorability_score - ingredient_score

        # STEP 3
        # lets sum the nutritional score from each ingredient
        # this should be from the full list, not the reduced list

        # STEP 4
        # Adjust based on frequency
        score = score - self.__calculate_historical_adjustment__()

        # we're done
        return score

            