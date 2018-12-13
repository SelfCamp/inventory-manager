def print_title(title):
    """Print `title`, and a row of dashes of equal length on the next line"""
    print('')
    print(title)
    print('-' * len(title.strip()))


def print_titled_list(list_of_dicts, omit_empty=True, gap=2):
    longest_title = max(len(line['title']) for line in list_of_dicts)
    if omit_empty:
        list_of_dicts = [line for line in list_of_dicts if line['data']]
    else:
        for line in list_of_dicts:
            if not line['data']:
                line['data'] = '-'
    for line in list_of_dicts:
        padding = longest_title - len(line['title']) + gap
        line['title'] += ':'
        line['title'] += ' ' * padding
    print('\n'.join(f"{line['title']}{line['data']}" for line in list_of_dicts))
