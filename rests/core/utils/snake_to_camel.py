

def snake_to_camel_case(snake_value: str):
    first, *others = snake_value.split('_')
    return ''.join([first.lower(), *map(str.title, others)])