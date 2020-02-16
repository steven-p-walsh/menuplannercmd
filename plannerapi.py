import requests

class PlannerAPI(object):

    base_url = 'http://localhost/api'

    def __init__(self, recipe_db):
        self.posted_ingredients = []
        self.recipe_db = recipe_db

    def post_category(self, user_id, category_name):
        url = '%s/category' % PlannerAPI.base_url
        response = requests.post(url, data = {'name': category_name})
        if response.status_code is not 200:
            print('failed to add %s, %s' % (category_name, response.reason))

    def post_ingredient_mapping(self, user_id, ingredient):
        ingredient_name = ingredient['name']
        recipe_name = ingredient['recipe'] if 'recipe' in ingredient else None
        points = ingredient['points'] if 'points' in ingredient else None
        grocery_section = ingredient['grocery_section'] if 'grocery_section' in ingredient else None
        group_penalty = ingredient['grouppenalty'] if 'grouppenalty' in ingredient else None

        # this ingredient has already been posted, don't try
        # to repost it
        if ingredient_name in self.posted_ingredients:
            return

        print('Adding ingredient %s' % ingredient_name)
       
        data = {
            'ingredient_name': ingredient_name,
            'recipe_name': recipe_name,
            'points': points,
            'group_penalty': group_penalty,
            'grocery_section': grocery_section,
            'user_id': user_id
        }

        url = '%s/ingredients' % PlannerAPI.base_url 
        response = requests.post(url, json = data)
        
        if response.status_code is not 200:
            print(data)
            #print('failed to add %s, %s' % (ingredient_name, response.reason))
            raise Exception('recipe import failed')

        self.posted_ingredients.append(ingredient_name)

    def post_pantry(self, user_id, items):
        url = '%s/pantry' % PlannerAPI.base_url
        print('adding user pantry items')
        mappings = self.recipe_db.mappings
        data = { 
            'items': list([mappings[i.lower()] for i in items]), 
            'user_id': user_id 
        }
        response = requests.post(url, json = data)
        if response.status_code is not 200:
            print(data)
            raise Exception('pantry import failed: %s' % response.text)

    def post_scheduled_item(self, user_id, day, availability):
        url = '%s/availability/%s' % (PlannerAPI.base_url, user_id);
        requests.post(url, json = {
            'dayofweek': day,
            'availability': availability
        });

    def post_histry(self, user_id, recipe_name, day):
        pass

    def post_recipe(self, user_id, name, slots, recipe_type, favorability, seasons, frequency, ingredients, category_name):
        
        print('Adding Recipe %s' % name)
        # first let's make sure all dependencies are posted
        #print(ingredients)
        
        for ingredient in ingredients:
            mapping = self.recipe_db.mappings[ingredient['name'].lower()]
            self.post_ingredient_mapping(user_id, mapping)

        url = '%s/recipes' % PlannerAPI.base_url
        data = {
            'recipe_name': name,
            'slots': slots,
            'type': recipe_type,
            'favorability': favorability,
            'season': seasons,
            'frequency': frequency,
            'ingredients': list([ingredient['name'] for ingredient in ingredients]),
            'user_id': user_id,
            'category_name': category_name
        }

        response = requests.post(url, json = data)
        
        if response.status_code is not 200:
            print('failed to add %s, %s' % (name, response.text))
            raise Exception('recipe import failed')
        