#!/usr/bin/env python3

from recipes.recipedb import RecipeDb
from Jsonimporter import JsonImporter
from plannerapi import PlannerAPI

user_id = 1

def get_data(recipe_db):
    data_folder = './data'
    importer = JsonImporter(data_folder, recipe_db)
    importer.populate_recipe_db()
    return importer

# Categories
def sync_categories(api, recipe_db):
    for category in recipe_db.categories:
        print('Adding Category "%s"' % category)
        api.post_category(user_id, category)

def sync_recipes(api, recipe_db):
    graph = recipe_db.build_recipe_graph()
    recipes = graph.sorted_recipes()
    for recipe in recipes:
        api.post_recipe(
            user_id, 
            recipe.name,
            recipe.slot_count,
            recipe.recipe_type,
            recipe.raw_score,
            recipe.seasons,
            recipe.frequency,
            recipe.ingredients,
            recipe.category_name
        )

# Pantry
def sync_pantry(api, importer):
    pantry = importer.get_pantry()
    items = [ item['name'] for item in pantry ]
    api.post_pantry(user_id, items)

# Schedule
def sync_schedule(importer):
    days = importer.get_schedule()
    for day in days:
        PlannerAPI.post_scheduled_item(
            user_id, 
            day['day'], 
            day['availability']
        )

# History
def sync_history(importer):
    for recipe_name in importer.recipes:
        recipe = importer.recipes[recipe_name]
        if recipe.last_made is None:
            continue
        PlannerAPI.post_histry(user_id, recipe_name, recipe.last_made)


def sync_all():
    recipe_db = RecipeDb()
    importer = get_data(recipe_db)
    api = PlannerAPI(recipe_db)
    #sync_categories(api, recipe_db)
    #sync_recipes(api, recipe_db)
    
    sync_pantry(api, importer)
    #sync_history(importer)
    #sync_schedule(importer)


if __name__ == "__main__":
    sync_all()