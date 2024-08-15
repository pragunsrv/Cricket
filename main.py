import random

class Team:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def bat(self):
        runs = random.randint(0, 6)
        self.score += runs
        return runs

class CricketGame:
    def __init__(self, team1_name, team2_name, overs):
        self.team1 = Team(team1_name)
        self.team2 = Team(team2_name)
        self.overs = overs

    def play_innings(self, batting_team):
        balls = self.overs * 6
        for _ in range(balls):
            run = batting_team.bat()
            if random.choice([True, False]):
                break

    def start_game(self):
        self.play_innings(self.team1)
        team1_score = self.team1.score
        self.play_innings(self.team2)
        team2_score = self.team2.score

        if team1_score > team2_score:
            return f"{self.team1.name} wins by {team1_score - team2_score} runs"
        elif team2_score > team1_score:
            return f"{self.team2.name} wins by {team2_score - team1_score} runs"
        else:
            return "The match is a tie"

game = CricketGame("Team A", "Team B", 2)
result = game.start_game()
print(result)
