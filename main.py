import random

class Team:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.wickets = 0
        self.balls_faced = 0
        self.runs_per_ball = []

    def bat(self):
        if self.wickets < 10:
            runs = random.randint(0, 6)
            self.score += runs
            self.balls_faced += 1
            self.runs_per_ball.append(runs)
            if runs == 0:
                if random.choice([True, False]):
                    self.wickets += 1
            return runs
        return 0

    def display_scorecard(self):
        print(f"Team: {self.name}")
        print(f"Score: {self.score}/{self.wickets} in {self.balls_faced} balls")
        print(f"Runs per ball: {self.runs_per_ball}")

class CricketGame:
    def __init__(self, team1_name, team2_name, overs):
        self.team1 = Team(team1_name)
        self.team2 = Team(team2_name)
        self.overs = overs
        self.total_balls = self.overs * 6

    def play_innings(self, batting_team):
        for _ in range(self.total_balls):
            if batting_team.wickets == 10:
                break
            run = batting_team.bat()
            print(f"Ball {_ + 1}: {run} run(s)")

    def display_match_summary(self):
        self.team1.display_scorecard()
        self.team2.display_scorecard()
        if self.team1.score > self.team2.score:
            print(f"{self.team1.name} wins by {self.team1.score - self.team2.score} runs")
        elif self.team2.score > self.team1.score:
            print(f"{self.team2.name} wins by {self.team2.score - self.team1.score} runs")
        else:
            print("The match is a tie")

    def start_game(self):
        print(f"Starting the match between {self.team1.name} and {self.team2.name}")
        print(f"{self.team1.name} is batting first")
        self.play_innings(self.team1)
        print(f"{self.team1.name} finished their innings with {self.team1.score} runs")
        print(f"{self.team2.name} is batting now")
        self.play_innings(self.team2)
        print(f"{self.team2.name} finished their innings with {self.team2.score} runs")
        self.display_match_summary()

game = CricketGame("Team A", "Team B", 2)
game.start_game()
