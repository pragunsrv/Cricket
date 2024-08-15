import random
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

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
        self.matches_won = 0
        self.form = 100
        self.fatigue = 0
        self.injury_status = False

    def bat(self):
        if not self.is_out and not self.injury_status:
            shot_type = random.choices(["Defensive", "Aggressive", "Neutral"], [0.3, 0.5, 0.2])[0]
            if shot_type == "Defensive":
                runs = random.randint(0, 2)
            elif shot_type == "Aggressive":
                runs = random.randint(0, 6)
            else:
                runs = random.randint(0, 4)
            self.runs += runs
            self.balls_faced += 1
            if runs == 0 and random.choice([True, False]):
                self.is_out = True
            self.form -= runs * 0.5
            self.fatigue += runs * 0.2
            if self.fatigue > 100:
                self.is_out = True
            if runs > 0:
                self.form += runs * 0.2
            if random.random() < 0.05:
                self.injury_status = True
            return runs, shot_type
        return 0, "N/A"

    def update_statistics(self):
        self.matches_played += 1
        self.total_runs += self.runs
        self.total_balls_faced += self.balls_faced
        if self.runs > self.high_score:
            self.high_score = self.runs
        self.runs = 0
        self.balls_faced = 0
        self.is_out = False
        self.injury_status = False
        self.fatigue = max(0, self.fatigue - 10)
        self.form = min(100, self.form)

    def display_statistics(self):
        print(f"{self.name}: Matches: {self.matches_played}, Total Runs: {self.total_runs}, Total Balls Faced: {self.total_balls_faced}, High Score: {self.high_score}, Matches Won: {self.matches_won}, Form: {self.form:.2f}, Fatigue: {self.fatigue:.2f}, Injury Status: {'Injured' if self.injury_status else 'Healthy'}")

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
        self.shot_types = []

    def get_current_batsman(self):
        return self.players[self.current_batsman_index]

    def bat(self):
        if self.wickets < 10:
            current_batsman = self.get_current_batsman()
            runs, shot_type = current_batsman.bat()
            self.score += runs
            self.balls_faced += 1
            self.runs_per_ball.append(runs)
            self.shot_types.append(shot_type)
            if current_batsman.is_out:
                current_batsman.update_statistics()
                self.wickets += 1
                self.current_batsman_index += 1
            return runs, shot_type
        return 0, "N/A"

    def update_team_statistics(self, won):
        if won:
            self.matches_won += 1
        for player in self.players:
            if won:
                player.matches_won += 1
            player.update_statistics()

    def display_scorecard(self):
        print(f"Team: {self.name}")
        print(f"Score: {self.score}/{self.wickets} in {self.balls_faced} balls")
        print(f"Runs per ball: {self.runs_per_ball}")
        print(f"Shot types: {self.shot_types}")
        for player in self.players:
            status = "Out" if player.is_out else "Not Out"
            print(f"{player.name}: {player.runs} runs off {player.balls_faced} balls ({status})")

    def display_team_statistics(self):
        print(f"Team: {self.name}")
        print(f"Matches Won: {self.matches_won}")
        for player in self.players:
            player.display_statistics()

class Tournament:
    def __init__(self, teams, format_type):
        self.teams = teams
        self.format_type = format_type
        self.group_stage_results = []
        self.knockout_stage_results = []

    def simulate_group_stage(self):
        print("Simulating Group Stage...")
        results = {}
        for team in self.teams:
            results[team.name] = random.randint(0, 10)
        self.group_stage_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        print("Group Stage Results:")
        for team, points in self.group_stage_results:
            print(f"{team}: {points} points")

    def simulate_knockout_stage(self):
        print("Simulating Knockout Stage...")
        if self.format_type == "Single-Elimination":
            self.simulate_single_elimination()
        elif self.format_type == "Double-Elimination":
            self.simulate_double_elimination()

    def simulate_single_elimination(self):
        print("Single Elimination Tournament")
        while len(self.teams) > 1:
            match_results = []
            for i in range(0, len(self.teams), 2):
                team1, team2 = self.teams[i], self.teams[i+1]
                winner = random.choice([team1, team2])
                print(f"{team1.name} vs {team2.name}: {winner.name} wins")
                match_results.append(winner)
            self.teams = match_results
        print(f"Tournament Winner: {self.teams[0].name}")

    def simulate_double_elimination(self):
        print("Double Elimination Tournament")
        eliminated = set()
        while len(self.teams) > 1:
            match_results = []
            for i in range(0, len(self.teams), 2):
                team1, team2 = self.teams[i], self.teams[i+1]
                winner = random.choice([team1, team2])
                loser = team1 if winner == team2 else team2
                print(f"{team1.name} vs {team2.name}: {winner.name} wins")
                if loser not in eliminated:
                    eliminated.add(loser)
                match_results.append(winner)
            self.teams = match_results
        print(f"Tournament Winner: {self.teams[0].name}")

    def display_tournament_summary(self):
        print(f"Tournament Format: {self.format_type}")
        print("Group Stage Results:")
        for team, points in self.group_stage_results:
            print(f"{team}: {points} points")
        print("Knockout Stage Results:")
        for result in self.knockout_stage_results:
            print(result)

class CricketGame:
    def __init__(self, team1_name, team2_name, overs, players_per_team, match_format, weather_conditions, stadium):
        self.team1 = Team(team1_name, players_per_team)
        self.team2 = Team(team2_name, players_per_team)
        self.overs = overs
        self.total_balls = self.overs * 6
        self.match_format = match_format
        self.weather_conditions = weather_conditions
        self.stadium = stadium
        self.match_history = []

    def apply_weather_conditions(self, team):
        if self.weather_conditions == "Rainy":
            team.balls_faced = max(0, team.balls_faced - random.randint(1, 3))
        elif self.weather_conditions == "Windy":
            team.balls_faced = max(0, team.balls_faced - random.randint(1, 2))

    def play_innings(self, batting_team):
        self.apply_weather_conditions(batting_team)
        for _ in range(self.total_balls):
            if batting_team.wickets == 10:
                break
            run, shot_type = batting_team.bat()
            print(f"Ball {_ + 1}: {run} run(s), Shot: {shot_type}")
            time.sleep(0.1)

    def display_match_summary(self):
        self.team1.display_scorecard()
        self.team2.display_scorecard()
        if self.team1.score > self.team2.score:
            print(f"{self.team1.name} wins by {self.team1.score - self.team2.score} runs")
            self.team1.update_team_statistics(True)
            self.team2.update_team_statistics(False)
            self.match_history.append(f"{self.team1.name} won by {self.team1.score - self.team2.score} runs")
        elif self.team2.score > self.team1.score:
            print(f"{self.team2.name} wins by {self.team2.score - self.team1.score} runs")
            self.team2.update_team_statistics(True)
            self.team1.update_team_statistics(False)
            self.match_history.append(f"{self.team2.name} won by {self.team2.score - self.team1.score} runs")
        else:
            print("The match is a tie")
            self.match_history.append("The match was a tie")

    def display_overall_statistics(self):
        self.team1.display_team_statistics()
        self.team2.display_team_statistics()

    def plot_scorecard(self):
        balls = np.arange(1, len(self.team1.runs_per_ball) + 1)
        plt.figure(figsize=(10, 6))
        plt.plot(balls, self.team1.runs_per_ball, label=self.team1.name, marker='o')
        plt.plot(balls, self.team2.runs_per_ball, label=self.team2.name, marker='o')
        plt.xlabel('Ball Number')
        plt.ylabel('Runs Scored')
        plt.title(f'Scorecard for {self.stadium}')
        plt.legend()
        plt.grid(True)
        plt.show()

    def start_game(self):
        print(f"Starting the {self.match_format} match between {self.team1.name} and {self.team2.name} at {self.stadium} with {self.weather_conditions} conditions")
        print(f"{self.team1.name} is batting first")
        self.play_innings(self.team1)
        print(f"{self.team1.name} finished their innings with {self.team1.score} runs")
        print(f"{self.team2.name} is batting now")
        self.play_innings(self.team2)
        print(f"{self.team2.name} finished their innings with {self.team2.score} runs")
        self.display_match_summary()
        self.display_overall_statistics()
        self.plot_scorecard()

def select_team(team_name):
    print(f"Select players for {team_name}:")
    players = []
    for i in range(1, 12):
        player_name = input(f"Enter name for Player {i}: ")
        players.append(player_name)
    return players

def main():
    print("Welcome to the Cricket Game!")
    team1_name = input("Enter name for Team 1: ")
    team2_name = input("Enter name for Team 2: ")
    team1_players = select_team(team1_name)
    team2_players = select_team(team2_name)
    overs = int(input("Enter number of overs for the match: "))
    match_format = input("Enter match format (T20/ODI/Test): ").upper()
    weather_conditions = input("Enter weather conditions (Clear/Rainy/Windy): ").capitalize()
    stadium = input("Enter the stadium name: ")
    game = CricketGame(team1_name, team2_name, overs, team1_players, match_format, weather_conditions, stadium)
    game.start_game()
    while True:
        replay = input("Do you want to play another match? (yes/no): ").lower()
        if replay == "yes":
            team1_name = input("Enter name for Team 1: ")
            team2_name = input("Enter name for Team 2: ")
            team1_players = select_team(team1_name)
            team2_players = select_team(team2_name)
            overs = int(input("Enter number of overs for the match: "))
            match_format = input("Enter match format (T20/ODI/Test): ").upper()
            weather_conditions = input("Enter weather conditions (Clear/Rainy/Windy): ").capitalize()
            stadium = input("Enter the stadium name: ")
            game = CricketGame(team1_name, team2_name, overs, team1_players, match_format, weather_conditions, stadium)
            game.start_game()
        else:
            break

if __name__ == "__main__":
    main()
