import os, json
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
                recipe_json['type']
            )
            recipe_db.add_recipe(recipe)

def pantry_json(data_folder):
    path = '%s/pantry.json' % data_folder
    with open(path, 'r') as f:
        return json.load(f)

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
    # run the generator
    generator = MenuGenerator(recipe_db, pantry, 5, 1000)
    best_menu = generator.run()
    names = list(map(lambda x: '%s %s' % (x.category_name, x.name), best_menu['items']))
    print(names)

