"""analisator module."""


def get_gorisontal_line(cage, list_cages, number_to_win):
    return [elem for elem in list_cages if elem['y'] == cage['y']]


def get_vertical_line(cage, list_cages, number_to_win):
    return [elem for elem in list_cages if elem['x'] == cage['x']]


def check_list(list_number, number_to_win):
    """
    Check if list_number contains numbersthat follow one after the other.

    Args:
        list_number: list
        number_to_win: str

    Returns:
        bool
    """
    groups = []
    for index in range(len(list_number)):
        groups.append(list_number[index:index + number_to_win])
    for group in groups:
        valid_group = range(group[0], group[0] + number_to_win, 1)
        if group == list(valid_group):
            return True
    return False


def find_series_numbers(list_cages, number_to_win):
    """
    Find 'number_to_win' consecutive numbers in a 'list_cages'.

    Args:
        list_cages: dict
        number_to_win: str

    Returns:
        bool
    """
    for cage in list_cages:
        list_gorisontal_cages = get_gorisontal_line(
            cage,
            list_cages,
            number_to_win,
        )
        list_coordinates_x = [elem['x'] for elem in list_gorisontal_cages]
        if check_list(list_coordinates_x, number_to_win):
            return True
        list_vertical_cages = get_vertical_line(
            cage,
            list_cages,
            number_to_win,
        )
        list_coordinates_y = [elem['y'] for elem in list_vertical_cages]
        if check_list(list_coordinates_y, number_to_win):
            return True
    return False


def is_victory(situation, name_winner):
    """
    Check if the situation is winning for name_winner.

    Args:
        situation: dict
        name_winner: str

    Returns:
        dict
    """
    list_cages = situation['cages']
    number_to_win = situation['number of cage to win']
    list_cages = [
        cage for cage in list_cages if cage['condition'] == name_winner
    ]
    return find_series_numbers(list_cages, number_to_win)
