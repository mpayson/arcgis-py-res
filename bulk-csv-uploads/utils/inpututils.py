"""utils for getting user input"""
from utils.searchutils import get_closest_match_list

def get_num_input(prompt):
    """get and force numeric input"""
    while True:
        u_in = input(prompt)
        try:
            num = int(u_in)
            return num
        except ValueError:
            print('WARN: Not a valid number')

def get_bool_input(prompt):
    """get and force boolean input"""
    while True:
        u_in = input(prompt)
        if u_in == 'Y' or u_in == 'y':
            return True
        if u_in == 'N' or u_in == 'n':
            return False
        print("WARN: Unknown input")

def get_list_input_smart(name, prompt, items, guesses, min_ratio=0.6, min_input_ratio=0.95):
    """get input item from a list with smart guesses"""
    closest, ratio = get_closest_match_list(items, guesses, min_ratio)
    if ratio > min_input_ratio:
        print("USING ({0}): {1} for `{2}`".format(ratio, closest, name))
        return closest
    if closest:
        print("FOUND ({0}): {1} for `{2}`".format(ratio, closest, name))
        b_in = get_bool_input("Use? (Y/N) ")
        if b_in:
            return closest
    return get_list_input(prompt, items)


def get_list_input(prompt, items):
    """get an item from a list, empty is acceptable"""

    while True:
        u_in = input(prompt)
        if u_in == '-L':
            return get_list_input_index(items)
        if u_in == '':
            return None
        if u_in in items:
            return u_in

def get_list_input_index(items):
    """get and force an item from a list using the index"""
    print_str = ""
    for i, item in enumerate(items):
        print_str += "[{0}]: {1} ".format(i, item)
    print(print_str)

    while True:
        i_in = get_num_input("index: ")
        if i_in and i_in < len(items) and i_in >= 0:
            return items[i_in]
        else:
            print("WARN: Index out of bounds")

