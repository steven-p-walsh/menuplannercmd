from menu.utils import get_menu_ingredients, color
from functools import reduce

class ShoppingPlanner(object):

    def __init__(self, menu, mappings, pantry):
        self.menu = menu
        self.mappings = mappings
        self.pantry = [ item['name'] for item in pantry ]

    def ingredient_groups(self):
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
    
    def print_columns(self, headers, columns):
        max_length = max([ len(x) for x in columns ])
        rows = []

        # pivot the data, and fill in gaps
        for i in range(0, max_length):
            row = []
            for col in columns:
                value = col[i] if i < len(col) else ''
                row.append(value)
            rows.append(row)
        
        # build the format string
        format_str = ''
        for col in columns:
            format_str = format_str + '{:<25s}'
        
        # print headers
        print(color.BOLD + format_str.format(*headers) + color.END)

        # print body
        for row in rows:
            print(color.CYAN + format_str.format(*row) + color.END)

    def print_list(self):
        mappings = self.ingredient_groups()
        groups = mappings.keys()

        columns = []
        headers = []

        for group in groups:
            ingredients = mappings[group]
            
            # skip if there is nothing to buy
            if len(ingredients) == 0:
                continue

            headers.append(group)
            columns.append([ing['name'] for ing in ingredients])

        self.print_columns(headers, columns)
                
            
