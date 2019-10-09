#!/usr/bin/env python

import os, json
from datetime import datetime
from recipes.recipie import Recipe
from recipes.recipedb import RecipeDb
from menugenerator import MenuGenerator

recipe_db = RecipeDb()

def recipe_json(file, category_name):
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
            recipe_db.add_recipe(recipe)

def pantry_json(data_folder):
    path = '%s/pantry.json' % data_folder
    with open(path, 'r') as f:
        return json.load(f)

def import_history(data_folder):
    path = '%s/history.json' % data_folder
    with open(path, 'r') as f:
        history = json.load(f)
        for recipe in history:
            date = recipe['history'][0]
            recipe_db.update_history(
                recipe['name'], 
                recipe['category'], 
                datetime.strptime(date, '%m-%d-%y')
            ) 

def import_ingredient_mappings(data_folder):
    path = '%s/ingredientmappings.json' % data_folder
    with open(path, 'r') as f:
        mappings = json.load(f)
        for mapping in mappings:
            recipe_db.add_mapping(mapping)

def import_category_recipe_json(data_folder, category_name):
    path = '%s/%s' % (data_folder, category_name)
    
    # don't try to import if the path does not exist
    if not os.path.exists(path):
        return

    category_contents = os.listdir(path)
    for recipe_file in category_contents:
        full_path = '%s/%s' % (path, recipe_file)
        recipe_json(full_path, category_name)

def import_category_manifest_json(data_folder):
    file = '%s/categories.json' % data_folder
    with open(file, 'r') as f:
        category_json = json.load(f)
        for category in category_json:
            import_category_recipe_json(data_folder, category['name'])

if __name__ == "__main__":
    data_folder = './data'
    recipe_count = 5
    iteration_count = 1000
    pantry = pantry_json(data_folder)
    
    # this will load the recipe db
    import_category_manifest_json(data_folder)
    import_ingredient_mappings(data_folder)
    import_history(data_folder)

    # combined list of all ingredients
    #names = recipe_db.get_ingredients_list()
    #names = list(set(names))
    #names.sort()
    
    # run the generator
    generator = MenuGenerator(recipe_db, pantry, recipe_count, iteration_count)
    best_menu = generator.run()
    names = map(lambda x: '%s - %s (%s)' % (x.category_name, x.name, x.calculate_score(best_menu)), best_menu['items'])
    for name in names:
        print(name)

