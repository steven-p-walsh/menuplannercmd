from menu.utils import get_menu_ingredients, color

class ShoppingPlanner(object):

    def __init__(self, menu, mappings, pantry):
        self.menu = menu
        self.mappings = mappings
        self.pantry = [ item['name'] for item in pantry ]

    def __pick_mappings__(self):
        items = self.menu['items']
        # get distinct list of mappings
        menu_ingredients = get_menu_ingredients(items)
        missing_ingredients = [item for item in menu_ingredients if item not in self.pantry]
        mappings = [ self.mappings[ingredient] for ingredient in missing_ingredients ]
        filtered_mappings = [ x for x in mappings if 'recipe' not in x ]
        
        # organize in groups
        groups = {}
        for mapping in filtered_mappings:
            section = mapping['grocery_section']
            if section not in groups:
                groups[section] = []
            groups[section].append(mapping)

        # return the groups
        return groups
    
    def print_list(self):
        mappings = self.__pick_mappings__()
        groups = mappings.keys()

        for group in groups:
            ingredients = mappings[group]
            
            # skip if there is nothing to buy
            if len(ingredients) == 0:
                continue

            # print the list
            print(color.BOLD + group + color.END)
            for ingredient in ingredients:
                ingredient_name = ingredient['name']
                print(color.CYAN + ingredient_name + color.END)
                
            
