import random

class Player:
    def __init__(self, name):
        self.name = name
        self.runs = 0
        self.balls_faced = 0
        self.is_out = False
        self.matches_played = 0
        self.total_runs = 0
        self.total_balls_faced = 0
        self.high_score = 0

    def bat(self):
        if not self.is_out:
            runs = random.randint(0, 6)
            self.runs += runs
            self.balls_faced += 1
            if runs == 0 and random.choice([True, False]):
                self.is_out = True
            return runs
        return 0

    def update_statistics(self):
        self.matches_played += 1
        self.total_runs += self.runs
        self.total_balls_faced += self.balls_faced
        if self.runs > self.high_score:
            self.high_score = self.runs
        self.runs = 0
        self.balls_faced = 0
        self.is_out = False

    def display_statistics(self):
        print(f"{self.name}: Matches: {self.matches_played}, Total Runs: {self.total_runs}, Total Balls Faced: {self.total_balls_faced}, High Score: {self.high_score}")

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = [Player(player) for player in players]
        self.current_batsman_index = 0
        self.score = 0
        self.wickets = 0
        self.balls_faced = 0
        self.runs_per_ball = []
        self.matches_won = 0

    def get_current_batsman(self):
        return self.players[self.current_batsman_index]

    def bat(self):
        if self.wickets < 10:
            current_batsman = self.get_current_batsman()
            runs = current_batsman.bat()
            self.score += runs
            self.balls_faced += 1
            self.runs_per_ball.append(runs)
            if current_batsman.is_out:
                current_batsman.update_statistics()
                self.wickets += 1
                self.current_batsman_index += 1
            return runs
        return 0

    def update_team_statistics(self, won):
        if won:
            self.matches_won += 1
        for player in self.players:
            player.update_statistics()

    def display_scorecard(self):
        print(f"Team: {self.name}")
        print(f"Score: {self.score}/{self.wickets} in {self.balls_faced} balls")
        print(f"Runs per ball: {self.runs_per_ball}")
        for player in self.players:
            status = "Out" if player.is_out else "Not Out"
            print(f"{player.name}: {player.runs} runs off {player.balls_faced} balls ({status})")

    def display_team_statistics(self):
        print(f"Team: {self.name}")
        print(f"Matches Won: {self.matches_won}")
        for player in self.players:
            player.display_statistics()

class CricketGame:
    def __init__(self, team1_name, team2_name, overs, players_per_team):
        self.team1 = Team(team1_name, players_per_team)
        self.team2 = Team(team2_name, players_per_team)
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
            self.team1.update_team_statistics(True)
            self.team2.update_team_statistics(False)
        elif self.team2.score > self.team1.score:
            print(f"{self.team2.name} wins by {self.team2.score - self.team1.score} runs")
            self.team2.update_team_statistics(True)
            self.team1.update_team_statistics(False)
        else:
            print("The match is a tie")

    def display_overall_statistics(self):
        self.team1.display_team_statistics()
        self.team2.display_team_statistics()

    def start_game(self):
        print(f"Starting the match between {self.team1.name} and {self.team2.name}")
        print(f"{self.team1.name} is batting first")
        self.play_innings(self.team1)
        print(f"{self.team1.name} finished their innings with {self.team1.score} runs")
        print(f"{self.team2.name} is batting now")
        self.play_innings(self.team2)
        print(f"{self.team2.name} finished their innings with {self.team2.score} runs")
        self.display_match_summary()
        self.display_overall_statistics()

players = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5", "Player 6", "Player 7", "Player 8", "Player 9", "Player 10", "Player 11"]
game = CricketGame("Team A", "Team B", 2, players)
game.start_game()
