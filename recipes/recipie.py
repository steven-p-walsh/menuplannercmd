import json, random


class Recipe(object):

    def __init__(self, category_name, name, ingredients, slot, recipe_type):
        self.category_name = category_name
        self.name = name
        self.ingredients = ingredients
        self.slot = slot
        self.recipe_type = recipe_type

        # Generate a random favorability score, this
        # is necessary for un-rated recipes which might
        # want to make their way into the plan
        #
        # because I want to increase the likelyhood that new 
        # recipes will be bumped up, i'm starting at 50 instead of 1
        self.favorability_score = random.randint(50,100)

    def calculate_score(self, context):
        # STEP 1
        # let's sum the cost of all ingredients minus items in our pantry
        # or items which are duplicated from previous menu items.
        #
        # we're removing previously added items because there's an in-built
        # assumption that we can get discounts if we buy in greater quantities

        # STEP 2
        # Let's add the favorability socre to the ingredients score

        # STEP 3
        # lets sum the nutritional score from each ingredient
        # this should be from the full list, not the reduced list
        return self.favorability_score
            