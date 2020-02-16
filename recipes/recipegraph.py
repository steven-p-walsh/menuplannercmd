from utils.graph import Graph

class RecipeGraph(object):

    def __init__(self, recipe_db):
        self.recipe_db = recipe_db
        self.graph = self.__build_recipe_graph__()
    
    def __build_recipe_graph__(self):
        recipe_dict = self.recipe_db.recipes
        mappings = self.recipe_db.mappings
        recipes = list(recipe_dict.values())
        graph = Graph(len(recipes))
        
        for recipe in recipes:
            recipe_index = recipes.index(recipe)
            recipe_mappings = map(lambda i: mappings[i['name'].lower()], recipe.ingredients)
            recipe_ingredients = filter(lambda i: 'recipe' in i, recipe_mappings)
            
            for recipe_ingredient in recipe_ingredients:
                key = '%s.%s' % (recipe_ingredient['category'], recipe_ingredient['name'])
                ingredient_recipe = recipe_dict[key.lower()]
                ingredient_index = recipes.index(ingredient_recipe)
                graph.addEdge(ingredient_index, recipe_index)

        return graph
    
    def sorted_recipes(self):
        recipe_dict = self.recipe_db.recipes
        recipes = list(recipe_dict.values())
        sorted_nodes = self.graph.topologicalSort()
        sorted_recipe_array = []
        for index in sorted_nodes:
            sorted_recipe_array.append(recipes[index])
        return sorted_recipe_array


