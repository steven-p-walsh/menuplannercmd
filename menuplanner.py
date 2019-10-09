#!/usr/bin/env python

import os, json
from recipes.recipedb import RecipeDb
from menugenerator import MenuGenerator
from Jsonimporter import JsonImporter


if __name__ == "__main__":
    data_folder = './data'
    recipe_count = 5
    iteration_count = 10000
    recipe_db = RecipeDb()
    
    importer = JsonImporter(data_folder, recipe_db)
    importer.populate_recipe_db()
    pantry = importer.get_pantry()
    schedule = importer.get_schedule()
 
    # run the generator
    generator = MenuGenerator(recipe_db, pantry, schedule, recipe_count, iteration_count)
    best_menu = generator.run()
    names = [  '%s: %s - %s (%s)' % (
        schedule[i]['day'],
        x.category_name, 
        x.name, 
        x.calculate_score(best_menu)) 
        for i,x in enumerate(best_menu['items'])
    ]
    for name in names:
        print(name)

