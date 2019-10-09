
import os, json
from datetime import datetime
from recipes.recipie import Recipe


class JsonImporter(object):

    def __init__(self, data_folder, recipe_db):
        self.data_folder = data_folder
        self.recipe_db = recipe_db

    def get_pantry(self):
        path = '%s/pantry.json' % self.data_folder
        with open(path, 'r') as f:
            return json.load(f)

    def get_schedule(self):
        path = '%s/schedule.json' % self.data_folder
        with open(path, 'r') as f:
            schedule = json.load(f)
            return schedule

    def import_history(self):
        path = '%s/history.json' % self.data_folder
        with open(path, 'r') as f:
            history = json.load(f)
            for recipe in history:
                date = recipe['history'][0]
                self.recipe_db.update_history(
                    recipe['name'], 
                    recipe['category'], 
                    datetime.strptime(date, '%m-%d-%y')
                ) 

    def import_ingredient_mappings(self):
        path = '%s/ingredientmappings.json' % self.data_folder
        with open(path, 'r') as f:
            mappings = json.load(f)
            for mapping in mappings:
                self.recipe_db.add_mapping(mapping)

    def __recipe_json__(self, file, category_name):
        with open(file, 'r') as f:
                recipe_json = json.load(f)
                recipe = Recipe(
                    category_name,
                    recipe_json['name'],
                    recipe_json['ingredients'],
                    recipe_json['slots'],
                    recipe_json['type'],
                    recipe_json['favorability'] if 'favorability' in recipe_json else None,
                    recipe_json['frequency'] if 'frequency' in recipe_json else None
                )
                self.recipe_db.add_recipe(recipe)

    def __import_category_recipe_json__(self, category_name):
        path = '%s/%s' % (self.data_folder, category_name)
        
        # don't try to import if the path does not exist
        if not os.path.exists(path):
            return

        category_contents = os.listdir(path)
        for recipe_file in category_contents:
            full_path = '%s/%s' % (path, recipe_file)
            self.__recipe_json__(full_path, category_name)

    def import_category_manifest(self):
        file = '%s/categories.json' % self.data_folder
        with open(file, 'r') as f:
            category_json = json.load(f)
            for category in category_json:
                self.__import_category_recipe_json__(category['name'])

    def populate_recipe_db(self):
        self.import_category_manifest()
        self.import_ingredient_mappings()
        self.import_history()