import numpy as np
import random

class Cup:
    
    def __init__(self):
        
        # https://digitalhub.fifa.com/m/6a616c6cf19bc57a/original/FWC-2022-Match-Schedule.pdf
    
        self.groups = {
            "A": ["QAT", "ECU", "SEN", "NED"],
            "B": ["ENG", "IRN", "USA", "EUR"], # <- Updates (Wales vs Scotland/Ukraine)
            "C": ["ARG", "KSA", "MEX", "POL"],
            "D": ["FRA", "ICP-1", "DEN", "TUN"], # <- Update (UAE/Australia vs Peru)
            "E": ["ESP", "ICP-2", "GER", "JPN"], # <- Update (Costa Rica vs New Zealand)
            "F": ["BEL", "CAN", "MAR", "CRO"],
            "G": ["BRA", "SRB", "SUI", "CMR"],
            "H": ["POR", "GHA", "URU", "KOR"],  
        }
        
        self.gameplan_group = [
            ["QAT","ECU"],   #1
            ["SEN","NED"],   #2
            ["ENG","IRN"],   #3
            ["USA","EUR"],   #4
            ["FRA","ICP-1"], #5
            ["DEN","TUN"],   #6
            ["MEX","POL"],   #7
            ["ARG","KSA"],   #8
            ["BEL","CAN"],   #9
            ["ESP","ICP-2"],#10
            ["GER","JPN"],  #11
            ["MAR","CRO"],  #12
            ["SUI","CMR"],  #13
            ["URU","KOR"],  #14
            ["POR","GHA"],  #15
            ["BRA","SRB"],  #16
            ["EUR","IRN"],  #17 
            ["QAT","SEN"],  #18
            ["NED","ECU"],  #19
            ["ENG","USA"],  #20
            ["TUN","ICP-1"],#21 
            ["POL","KSA"],  #22
            ["FRA","DEN"],  #23
            ["ARG","MEX"],  #24
            ["JPN","ICP-2"],#25 
            ["BEL","MAR"],  #26
            ["CRO","CAN"],  #27
            ["ESP","GER"],  #28
            ["CMR","SRB"],  #29
            ["KOR","GHA"],  #30
            ["BRA","SUI"],  #31
            ["POR","URU"],  #32
            ["EUR","ENG"],  #33
            ["IRN","USA"],  #34
            ["ECU","SEN"],  #35
            ["NED","QAT"],  #36
            ["ICP-1","DEN"],#37 
            ["TUN","FRA"],  #38
            ["POL","ARG"],  #39
            ["KSA","MEX"],  #40
            ["CRO","BEL"],  #41
            ["CAN","MAR"],  #42
            ["JPN","ESP"],  #43
            ["ICP-2","GER"],#44
            ["GHA","URU"],  #45
            ["KOR","POR"],  #46
            ["SRB","SUI"],  #47
            ["CMR","BRA"],  #48        
        ]
        
        
        self.knock_out = {
            "round_of_16": [
                ["1A","2B"], #49
                ["1C","2D"], #50
                ["1B","2A"], #51
                ["1D","2C"], #52
                ["1E","2F"], #53
                ["1G","2H"], #54
                ["1F","2E"], #55
                ["1H","2G"], #56   
            ],
            "quarter_finals": [
                ["W49","W50"], #57
                ["W53","W54"], #58
                ["W51","W52"], #59
                ["W55","W56"], #60  
            ],
            "semi_finals": [
                ["W57","W58"], #61
                ["W59","W60"], #62
            ],
            "final":
                [["W61","W62"]], #64
        }
        
        self.game_results = []


    def group_round(self):
        
        games_goals = self.predict_goals_groupround()
        scoreboard = self.calculate_scoreboard(games_goals)
        group_results = self.get_group_top2(scoreboard)

        return group_results
    

    def predict_goals_groupround(self):
    
        games_goals = []
        for game in self.gameplan_group:

            # Add prediction logic here
            goals = self.predict_goals(game, no_draw=False)

            games_goals.append([game, goals])
            
        self.game_results = games_goals

        return games_goals    
        
    
    def predict_goals(self, game, no_draw):
        
        # Add prediction logic here
        goals = [random.randrange(0, 6), random.randrange(0, 6)]
        
        if no_draw and (goals[0] == goals[1]):

            while goals[0] == goals[1]:
                goals = [random.randrange(0, 6), random.randrange(0, 6)]
                
        return goals
    

    def calculate_scoreboard(self, games_goals):

        scoreboard = {}
        for game_goals in games_goals:

            #print(game_goals)

            game, goals = game_goals[0], game_goals[1]

            winner, points, goal_diffs = self.get_game_stats(game, goals)

            for i, team in enumerate(game):

                #print(game, goals, i, team, points[i], goal_diffs[i], goals[i])

                if team not in scoreboard:

                    scoreboard[team] = [points[i], goal_diffs[i], goals[i]]

                else:
                    # Update points
                    scoreboard[team][0] += points[i]

                    # Update goal diff
                    scoreboard[team][1] += goal_diffs[i]

                    # Update goals
                    scoreboard[team][2] += goals[i]

        return scoreboard
    
    
    def get_game_stats(self, game, goals):
    
        winner = "draw"

        if goals[0]>goals[1]:
            winner = game[0]
            points = [3, 0]

        elif goals[0]==goals[1]:
            points = [1, 1]

        else:
            winner = game[1]
            points = [0, 3]
            
        goal_diffs = [goals[0]-goals[1], goals[1]-goals[0]]

        return winner, points, goal_diffs 
                     
        
    def get_group_top2(self, scoreboard, groups=None):
        
        g = groups if groups is not None else self.groups
        group_results = {}
        for group in g:

            group_teams = self.groups[group]
            group_points = [scoreboard[team][0] for team in group_teams]
            group_goal_diffs = [scoreboard[team][1] for team in group_teams]
            group_goals = [scoreboard[team][2] for team in group_teams]

            winner, idx = self.get_next_winner(group_teams, group_points, group_goal_diffs, group_goals)

            group_teams2 = [group_teams[i] for i in range(4) if i not in [idx]]
            group_points2  = [group_points[i] for i in range(4) if i not in [idx]]
            group_goal_diffs2 = [group_goal_diffs[i] for i in range(4) if i not in [idx]]
            group_goals2 = [group_goals[i] for i in range(4) if i not in [idx]]

            second, _ = self.get_next_winner(group_teams2, group_points2, group_goal_diffs2, group_goals2)

            group_results[f"1{group}"] = winner
            group_results[f"2{group}"] = second

        return group_results
    

    def get_next_winner(self, teams, points, goal_diffs, goals):

        #print(teams, points, goal_diffs, goals)

        # get indices of maximum points
        max_points_indices = [1 if v == max(points) else 0 for v in points]

        # check POINTS
        if sum(max_points_indices) == 1:
            return teams[np.argmax(points)], np.argmax(points)

        # two or more teams have same goal diff
        else:
            # check GOAL DIFF
            max_goal_diffs_indices = [1 if v == max(goal_diffs) else 0 for v in goal_diffs]
            max_goal_diffs_indices = [i*j for i, j in zip(max_points_indices, max_goal_diffs_indices)]

            if sum(max_goal_diffs_indices) == 1:
                return teams[np.argmax(max_goal_diffs_indices)], np.argmax(max_goal_diffs_indices)

            else:
                # check GOALS
                max_goals_indices = [1 if v == max(goals) else 0 for v in goals]
                max_goals_indices = [i*j for i, j in zip(max_goal_diffs_indices, max_goals_indices)]

                if sum(max_goals_indices) == 1:
                    return teams[np.argmax(max_goals_indices)], np.argmax(max_goals_indices)

                else:
                    compare_teams = [team for team,i in zip(teams, max_goals_indices) if i==1]
                    
                    if len(compare_teams) == 2:
                        direct_comparison = [result for result in self.game_results 
                                             if (compare_teams[0] in result[0]) 
                                             and (compare_teams[1] in result[0])][0]
                        winner = direct_comparison[0][np.argmax(direct_comparison[1])]
                                        
                    else:
                        print("Random choice")
                        winner = random.choice(teams)
                    
                    return winner, teams.index(winner)
    

    def knock_out_round(self, round="round_of_16", matches={}):
    
        match_no = {
            "round_of_16": 49,
            "quarter_finals": 57,
            "semi_finals": 61,
            "final": 64,
        }

        next_matches = {}

        for i, game in enumerate(self.knock_out[round]):

            match = [matches[game[0]], matches[game[1]]]
            
            goals = self.predict_goals(match, no_draw=True)
            winner, _, _ = self.get_game_stats(match, goals)

            next_matches[f"W{match_no[round]+i}"] = winner

        return next_matches

    
    def simulate(self):
        
        group_results = self.group_round()
        round_of_16_results = self.knock_out_round(round="round_of_16", matches=group_results)
        quarter_final_results = self.knock_out_round(round="quarter_finals", matches=round_of_16_results)
        semi_final_results = self.knock_out_round(round="semi_finals", matches=quarter_final_results)
        final = self.knock_out_round(round="final", matches=semi_final_results)
        
        winner = final["W64"]
        #print(winner)
        
        return winner     