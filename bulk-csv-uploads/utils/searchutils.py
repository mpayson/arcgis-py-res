"""fuzzy search functions"""
from difflib import SequenceMatcher

def get_closest_match(value, guesses, min_ratio=0.6):
    """find the closest guess to a value"""
    v_low = value.lower()
    closest = None
    for guess in guesses:
        g_low = guess.lower()
        c_ratio = SequenceMatcher(None, v_low, g_low).ratio()
        if c_ratio > min_ratio:
            min_ratio = c_ratio
            closest = guess

    min_ratio = round(min_ratio, 3)
    return (closest, min_ratio) if closest else (None, None)

def get_closest_match_list(options, guesses, min_ratio=0.6):
    """find the closest guess from a set of options"""
    closest = None
    for option in options:
        t_closest, t_min = get_closest_match(option, guesses, min_ratio)
        if t_min and t_min > min_ratio:
            closest = t_closest
            min_ratio = t_min

    return (closest, min_ratio) if closest else (None, None)
