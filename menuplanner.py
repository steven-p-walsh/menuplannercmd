#!/usr/bin/env python3

import os, json, argparse
from recipes.recipedb import RecipeDb
from menugenerator import MenuGenerator
from Jsonimporter import JsonImporter


p = argparse.ArgumentParser(description='Generates a plan for a weekly menu', add_help=True)
p.add_argument('-n', help='print the recipe names only', action='store_true')
p.add_argument('-i', help='Number of iterations to test', type=int, default=1000)
p.add_argument('-c', help='The number of recipes to generate', type=int, default=5)
p.add_argument('-d', help='The location of the data folder', default='./data')
p.add_argument('-bi', help="List of ingredients to boost", default=None)
args = p.parse_args()

data_folder = args.d
recipe_count = args.c
iteration_count = args.i
boosted_list = [] if args.bi is None else args.bi.split(',')

if __name__ == "__main__":

    recipe_db = RecipeDb()
    
    importer = JsonImporter(data_folder, recipe_db)
    importer.populate_recipe_db()
    pantry = importer.get_pantry()
    schedule = importer.get_schedule()
 
    # run the generator
    generator = MenuGenerator(recipe_db, pantry, schedule, recipe_count, iteration_count, boosted_list)
    best_menu = generator.run()
    names = []

    if args.n:
        names = [ x.name for x in best_menu['items'] ] 
    else:
        names = [  '%s: %s - %s (%s)' % (
            schedule[i]['day'],
            x.category_name, 
            x.name, 
            x.calculate_score(best_menu)) 
            for i,x in enumerate(best_menu['items'])
        ]

    for name in names:
        print(name)

