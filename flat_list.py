
def flat_list(some_list):
    string_list = str(some_list)
    new_string_for_list = ''
    for char in string_list:
        if char not in ['[',']']:
            new_string_for_list += char
    new_list = [int(el) for el in new_string_for_list.split(', ')]
    return new_list