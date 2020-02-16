#!/usr/bin/env python3

import argparse, json
from recipes.recipedb import RecipeDb
from menu.menugenerator import MenuGenerator
from menu.shoppingplanner import ShoppingPlanner
from menu.utils import color
from Jsonimporter import JsonImporter


p = argparse.ArgumentParser(description='Generates a plan for a weekly menu', add_help=True)
p.add_argument('-n', help='print the recipe names only', action='store_true')
p.add_argument('-i', help='Number of iterations to test', type=int, default=1000)
p.add_argument('-c', help='The number of recipes to generate', type=int, default=5)
p.add_argument('-d', help='The location of the data folder', default='./data')
p.add_argument('-bi', help="List of ingredients to boost", default=None)
p.add_argument('-sl', help="Print the shopping list as well", action="store_true")
p.add_argument('-e', help="Explain the score", action="store_true")
p.add_argument('-j', help="Print output in JSON format", action="store_true")
args = p.parse_args()

names_only = args.n
print_shopping_list = args.sl
data_folder = args.d
recipe_count = args.c
iteration_count = args.i
boosted_list = [] if args.bi is None else args.bi.split(',')
explain_score = args.e
json_out = args.j

def print_text(generator, best_menu):
    names = []

    if names_only:
        names = [ x.name for x in best_menu['items'] ] 
    else:
        names = [  '%s: %s - %s (%s)' % (
            schedule[i]['day'],
            x.category_name, 
            x.name, 
            x.calculate_score(best_menu)) 
            for i,x in enumerate(best_menu['items'])
        ]


    if print_shopping_list:
        print(color.BOLD + color.BLUE + '\r\nRecipes\r\n' + color.END)
    
    for name in names:
        print(color.GREEN + name + color.END)
    
    if print_shopping_list:
        print('\r\n' + color.BOLD + color.BLUE + 'Shopping List' + color.END + '\r\n')
        planner = ShoppingPlanner(best_menu, recipe_db.mappings, pantry)
        planner.print_list()
        print('\r\n')
    
    if explain_score:
        generator.print_explain_menu_score(best_menu)

def print_json(generator, best_menu):
    plan = {}

    plan['items'] = generator.menu_details(best_menu)

    if print_shopping_list:
        planner = ShoppingPlanner(best_menu, recipe_db.mappings, pantry)
        plan['shopping_list'] = planner.ingredient_groups()
    
    jsonstr = json.dumps(plan)
    print(jsonstr)

if __name__ == "__main__":

    recipe_db = RecipeDb()
    
    importer = JsonImporter(data_folder, recipe_db)
    importer.populate_recipe_db()
    pantry = importer.get_pantry()
    schedule = importer.get_schedule()
 
    # run the generator
    generator = MenuGenerator(recipe_db, pantry, schedule, recipe_count, iteration_count, boosted_list)
    best_menu = generator.run()

    if json_out:
        print_json(generator, best_menu)
    else:
        print_text(generator, best_menu)

