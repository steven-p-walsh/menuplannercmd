import itertools

def get_menu_ingredients(items):
    item_ingredients = [ x.ingredients for x in items ]
    all_ingredients = list(itertools.chain.from_iterable(item_ingredients))
    ingredient_names = [ x['name'] for x in all_ingredients ]
    final_set = list(set(ingredient_names))
    return final_set

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
