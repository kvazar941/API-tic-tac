"""Fixture"""
#  Представление клетки игрового поля:
#  {
#      'x': 0,
#      'y': 0,
#      'condition': 'cross',
#  },
#  'condition' может принимать значения 'cross' или 'round'.

GAME_SITUATION_WIN_CROSS = {
    'number of cage to win': 3,
    'cages': [
        {
            'x': 0,
            'y': 0,
            'condition': 'cross',
        },
        {
            'x': 0,
            'y': 1,
            'condition': 'round',
        },
        {
            'x': 0,
            'y': 2,
            'condition': 'round',
        },
        {
            'x': 2,
            'y': 0,
            'condition': 'cross',
        },
        {
            'x': 5,
            'y': 0,
            'condition': 'cross',
        },
        {
            'x': 6,
            'y': 0,
            'condition': 'cross',
        },
        {
            'x': 7,
            'y': 0,
            'condition': 'cross',
        },
    ],
}

GAME_START_SITUATION = {
    'number of cage to win': 3,
    'cages': [
        {
            'x': 0,
            'y': 0,
            'condition': 'cross',
        },
    ],
}
