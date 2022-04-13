from cup import Cup
import pytest

@pytest.fixture
def cup():
    return Cup()


def test_calculate_scorecard(cup):

    games_goals = [
        [['QAT', 'ECU'], [2, 0]],
        [['QAT', 'SEN'], [2, 0]],
        [['QAT', 'NED'], [2, 0]],
        [['ECU', 'SEN'], [1, 0]], 
        [['ECU', 'NED'], [2, 2]],  
        [['SEN', 'NED'], [3, 3]]
    ]

    scoreboard_expected = {
        # Points, goal diff, goals
        'QAT': [9,  6, 6], # 1
        'ECU': [4, -1, 3], # 2
        'SEN': [1, -3, 3],  
        'NED': [2, -2, 5]
    }

    assert cup.calculate_scoreboard(games_goals) == scoreboard_expected


def test_calculate_scorecard2(cup):

    games_goals = [
        [['QAT', 'ECU'], [0, 0]],
        [['QAT', 'SEN'], [1, 0]],
        [['QAT', 'NED'], [1, 0]],
        [['ECU', 'SEN'], [2, 0]], 
        [['ECU', 'NED'], [2, 0]], 
        [['SEN', 'NED'], [0, 0]]
    ]

    scoreboard_expected = {
        # Points, goal diff, goals
        'QAT': [7,  2, 2], # 2
        'ECU': [7,  4, 4], # 1
        'SEN': [1, -3, 0],  
        'NED': [1, -3, 0]
    }

    assert cup.calculate_scoreboard(games_goals) == scoreboard_expected
    

def test_get_group_top2_by_points(cup):

    scoreboard = {
        # Points, goal diff, goals
        'QAT': [9,  6, 6], # 1
        'ECU': [4, -1, 3], # 2
        'SEN': [1, -3, 3],  
        'NED': [2, -2, 5]
    }

    top2_expected = {
        '1A': 'QAT', 
        '2A': 'ECU'
    }

    assert cup.get_group_top2(scoreboard, groups=["A"]) == top2_expected


def test_get_group_top2_by_goal_diff(cup):

    scoreboard = {
        # Points, goal diff, goals
        'QAT': [7,  2, 2], # 2
        'ECU': [7,  4, 4], # 1
        'SEN': [1, -3, 0],  
        'NED': [1, -3, 0]
    }

    top2_expected = {
        '1A': 'ECU', 
        '2A': 'QAT'
    }

    assert cup.get_group_top2(scoreboard, groups=["A"]) == top2_expected


def test_get_group_top2_by_goals(cup):

    scoreboard = {
        # Points, goal diff, goals
        'QAT': [4,  1, 3], # 2
        'ECU': [9,  3, 3], # 1
        'SEN': [4,  0, 2],  
        'NED': [0, -4, 0]
    }

    top2_expected = {
        '1A': 'ECU', 
        '2A': 'QAT'
    }

    assert cup.get_group_top2(scoreboard, groups=["A"]) == top2_expected


def test_get_group_top2_by_goaldiff_and_goals(cup):

    scoreboard = {
        # Points, goal diff, goals
        'QAT': [9,  6, 6], #1
        'ECU': [2, -2, 3], 
        'SEN': [2, -2, 4],  
        'NED': [2, -2, 5]  #2
    }

    top2_expected = {
        '1A': 'QAT', 
        '2A': 'NED'
    }

    assert cup.get_group_top2(scoreboard, groups=["A"]) == top2_expected


def test_get_group_top2_by_direct_comparison(cup):

    scoreboard = {
        # Points, goal diff, goals
        'QAT': [5, 3, 2], #1
        'ECU': [5, 3, 2], #2
        'SEN': [4, 3, 2],  
        'NED': [0, 0, 0]
    }

    cup.game_results = [
        [["QAT","ECU"], [1,0]] # QAT wins agains ECU in direct comparison
    ]

    top2_expected = {
        '1A': 'QAT', 
        '2A': 'ECU'
    }

    assert cup.get_group_top2(scoreboard, groups=["A"]) == top2_expected