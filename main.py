import random
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime

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
        self.injury_history = []
        self.skills = {"Batting": 50, "Bowling": 50, "Fielding": 50, "Fitness": 50, "Strategy": 50}
        self.training_sessions = 0
        self.practice_effectiveness = {"Batting": 0.1, "Bowling": 0.1, "Fielding": 0.1, "Fitness": 0.1, "Strategy": 0.1}
        self.performance_history = {"Batting": [], "Bowling": []}
        self.match_winning_impact = random.uniform(0.1, 0.5)
        self.age = random.randint(20, 35)
        self.experience = random.uniform(0.1, 1.0)
        self.mental_strength = random.uniform(0.5, 1.0)
        self.training_intensity = 0.1
        self.recovery_time = 0
        self.training_load = 0
        self.injury_history = []
        self.mood = "Neutral"
        self.fitness_level = 100
        self.tactical_acumen = 50
        self.agility = random.uniform(0.5, 1.0)
        self.expertise = {"Batting": random.uniform(0.5, 1.0), "Bowling": random.uniform(0.5, 1.0)}
        self.tactical_improvement = {"Batting": 0.1, "Bowling": 0.1}
        self.stats = pd.DataFrame(columns=["Match", "Runs", "Balls Faced", "Wickets", "Overs", "Team"])

    def train(self, skill):
        if skill in self.skills:
            increase = random.uniform(0.1, 0.5)
            self.skills[skill] += increase
            self.training_sessions += 1
            self.practice_effectiveness[skill] += 0.05
            self.training_load += increase
            if self.training_load > 100:
                self.injury_status = True
                self.injury_history.append("Training Injury")
                self.recovery_time = random.randint(1, 3)
            self.adjust_training_effectiveness()

    def adjust_training_effectiveness(self):
        for skill in self.tactical_improvement:
            self.tactical_improvement[skill] = min(0.5, self.tactical_improvement[skill] * (1 + self.skills["Fitness"] / 100))

    def recover(self):
        if self.recovery_time > 0:
            self.recovery_time -= 1
            if self.recovery_time == 0:
                self.injury_status = False
                self.fitness_level = min(100, self.fitness_level + 20)
                self.mood = "Happy"

    def bat(self):
        if not self.is_out and not self.injury_status:
            skill_multiplier = self.skills["Batting"] / 100
            shot_type = random.choices(["Defensive", "Aggressive", "Neutral"], [0.3, 0.5, 0.2])[0]
            if shot_type == "Defensive":
                runs = int(random.uniform(0, 2) * skill_multiplier)
            elif shot_type == "Aggressive":
                runs = int(random.uniform(0, 6) * skill_multiplier)
            else:
                runs = int(random.uniform(0, 4) * skill_multiplier)
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
                self.injury_history.append("Injury")
            self.recover()
            return runs, shot_type
        return 0, "N/A"

    def bowl(self):
        if not self.injury_status:
            skill_multiplier = self.skills["Bowling"] / 100
            ball_type = random.choices(["Fast", "Spin", "Swing"], [0.4, 0.3, 0.3])[0]
            if ball_type == "Fast":
                runs = int(random.uniform(0, 6) * skill_multiplier)
            elif ball_type == "Spin":
                runs = int(random.uniform(0, 4) * skill_multiplier)
            else:
                runs = int(random.uniform(0, 2) * skill_multiplier)
            self.performance_history["Bowling"].append(runs)
            if random.random() < 0.1:
                wickets = 1
            else:
                wickets = 0
            return runs, ball_type, wickets
        return 0, "N/A", 0

    def update_statistics(self, match, runs, balls_faced, wickets, overs, team):
        self.matches_played += 1
        self.total_runs += runs
        self.total_balls_faced += balls_faced
        if runs > self.high_score:
            self.high_score = runs
        self.stats = self.stats.append({"Match": match, "Runs": runs, "Balls Faced": balls_faced, "Wickets": wickets, "Overs": overs, "Team": team}, ignore_index=True)
        if self.injury_status:
            self.injury_history.append(f"Injury in match {match}")

    def display_statistics(self):
        print(f"{self.name}: Matches: {self.matches_played}, Total Runs: {self.total_runs}, Total Balls Faced: {self.total_balls_faced}, High Score: {self.high_score}, Matches Won: {self.matches_won}, Form: {self.form:.2f}, Fatigue: {self.fatigue:.2f}, Injury Status: {'Injured' if self.injury_status else 'Healthy'}")
        if self.injury_history:
            print(f"Injury History: {', '.join(self.injury_history)}")
        print(f"Skills: {self.skills}")
        print(f"Training Sessions: {self.training_sessions}")
        print(f"Performance History: {self.performance_history}")

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = [Player(player) for player in players]
        self.current_batsman_index = 0
        self.current_bowler_index = 0
        self.score = 0
        self.wickets = 0
        self.balls_faced = 0
        self.runs_per_ball = []
        self.shot_types = []
        self.matches_won = 0
        self.shot_counts = {"Defensive": 0, "Aggressive": 0, "Neutral": 0}
        self.training_sessions = 0
        self.strategy = {"Aggression": 50, "Defense": 50}
        self.form_index = 0.0
        self.batting_order = []
        self.bowling_order = []

    def get_current_batsman(self):
        return self.players[self.current_batsman_index]

    def get_current_bowler(self):
        return self.players[self.current_bowler_index]

    def train_all_players(self, skill):
        for player in self.players:
            player.train(skill)
        self.training_sessions += 1

    def bat(self):
        if self.wickets < 10:
            current_batsman = self.get_current_batsman()
            runs, shot_type = current_batsman.bat()
            self.score += runs
            self.balls_faced += 1
            self.runs_per_ball.append(runs)
            self.shot_types.append(shot_type)
            self.shot_counts[shot_type] += 1
            if current_batsman.is_out:
                current_batsman.update_statistics("Match", current_batsman.runs, current_batsman.balls_faced, 0, self.balls_faced, self.name)
                self.wickets += 1
                self.current_batsman_index += 1
            return runs, shot_type
        return 0, "N/A"

    def bowl(self):
        if self.balls_faced < self.total_balls:
            current_bowler = self.get_current_bowler()
            runs, ball_type, wickets = current_bowler.bowl()
            self.runs_per_ball.append(runs)
            if wickets > 0:
                self.wickets += wickets
            return runs, ball_type, wickets
        return 0, "N/A", 0

    def update_team_statistics(self, won):
        if won:
            self.matches_won += 1

    def display_team_statistics(self):
        print(f"Team: {self.name}")
        for player in self.players:
            player.display_statistics()

    def set_batting_order(self, order):
        self.batting_order = order

    def set_bowling_order(self, order):
        self.bowling_order = order

    def get_currentt_batsman(self):
        return self.players[self.current_batsman_index]

    def get_currentt_bowler(self):
        return self.players[self.current_bowler_index]

    def train_all_playerrs(self, skill):
        for player in self.players:
            player.train(skill)
        self.training_sessions += 1

    def bat_(self):
        if self.wickets < 10:
            current_batsman = self.get_current_batsman()
            runs, shot_type = current_batsman.bat()
            self.score += runs
            self.balls_faced += 1
            self.runs_per_ball.append(runs)
            self.shot_types.append(shot_type)
            self.shot_counts[shot_type] += 1
            if current_batsman.is_out:
                current_batsman.update_statistics()
                self.wickets += 1
                self.current_batsman_index += 1
            return runs, shot_type
        return 0, "N/A"

    def bowl_(self):
        if self.balls_faced < self.total_balls:
            current_bowler = self.get_current_bowler()
            runs, ball_type, wickets = current_bowler.bowl()
            self.runs_per_ball.append(runs)
            if wickets > 0:
                self.wickets += wickets
                self.current_batsman_index += 1
            return runs, ball_type, wickets
        return 0, "N/A", 0
    def adjust_strategy(self):
        total_runs = sum(self.runs_per_ball)
        if total_runs / self.balls_faced > 6:
            self.strategy["Aggression"] += 10
        else:
            self.strategy["Defense"] += 10
    def apply_strategy(self, phase):
        if phase == "Early":
            self.strategy["Aggression"] += 10
        elif phase == "Middle":
            self.strategy["Defense"] += 10
        else:
            self.strategy["Aggression"] += 5
            self.strategy["Defense"] += 5

    def assess_performance(self):
        self.form_index = (self.score / self.balls_faced) * 100

class Tournament:
    def __init__(self, teams, format_type):
        self.teams = teams
        self.format_type = format_type
        self.matches = []
        self.group_stage_results = []
        self.knockout_stage_results = []
        self.tournament_phase = 0
        self.phases = {}

    def simulate_group_stage(self):
        self.phases[1] = "Group Stage"
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                team1 = self.teams[i]
                team2 = self.teams[j]
                self.play_match(team1.name, team2.name)
                self.group_stage_results.append((team1.name, team1.score))
                self.group_stage_results.append((team2.name, team2.score))

    def simulate_knockout_stage(self):
        self.tournament_phase += 1
        self.phases[self.tournament_phase] = "Knockout Stage"
        if self.format_type == "Single-Elimination":
            self.simulate_single_elimination()
        elif self.format_type == "Double-Elimination":
            self.simulate_double_elimination()
        elif self.format_type == "Round-Robin":
            self.simulate_round_robin()
        else:
            print("Invalid tournament format.")

    def simulate_single_elimination(self):
        self.matches = []
        teams = self.group_stage_results[:4]
        while len(teams) > 1:
            next_round_teams = []
            for i in range(0, len(teams), 2):
                team1, team2 = teams[i][0], teams[i + 1][0]
                match_result = self.play_match(team1, team2)
                self.matches.append(match_result)
                winner = match_result['winner']
                next_round_teams.append(winner)
            teams = next_round_teams
        self.knockout_stage_results = teams
        print("Single Elimination Results:")
        for match in self.matches:
            print(f"{match['team1']} vs {match['team2']} - Winner: {match['winner']}")

    def simulate_double_elimination(self):
        print("Double Elimination is not yet implemented.")

    def simulate_round_robin(self):
        print("Round-Robin is not yet implemented.")

    def play_match(self, team1_name, team2_name):
        team1 = next(team for team in self.teams if team.name == team1_name)
        team2 = next(team for team in self.teams if team.name == team2_name)
        overs = 20
        match_format = "T20"
        weather_conditions = "Clear"
        stadium = "Neutral"
        game = CricketGame(team1_name, team2_name, overs, team1.players, match_format, weather_conditions, stadium)
        game.start_game()
        return {
            'team1': team1_name,
            'team2': team2_name,
            'winner': team1_name if team1.score > team2.score else team2_name
        }

    def schedule_matches(self):
        print("Scheduling Matches...")
        self.simulate_group_stage()

    def display_tournament_summary(self):
        print("Tournament Summary:")
        for phase in range(1, self.tournament_phase + 1):
            print(f"Phase {phase}: {self.phases[phase]}")
        print("Knockout Stage Results:")
        for result in self.knockout_stage_results:
            print(f"Winner: {result}")
class ODI:
    def __init__(self, teams, format_type):
        self.teams = teams
        self.format_type = format_type
        self.matches = []
        self.group_stage_results = []
        self.knockout_stage_results = []
        self.tournament_phase = 0
        self.phases = {}

    def simulate_group_stage(self):
        self.phases[1] = "Group Stage"
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                team1 = self.teams[i]
                team2 = self.teams[j]
                self.play_match(team1.name, team2.name)
                self.group_stage_results.append((team1.name, team1.score))
                self.group_stage_results.append((team2.name, team2.score))

    def simulate_knockout_stage(self):
        self.tournament_phase += 1
        self.phases[self.tournament_phase] = "Knockout Stage"
        if self.format_type == "Single-Elimination":
            self.simulate_single_elimination()
        elif self.format_type == "Double-Elimination":
            self.simulate_double_elimination()
        elif self.format_type == "Round-Robin":
            self.simulate_round_robin()
        else:
            print("Invalid tournament format.")

    def simulate_single_elimination(self):
        self.matches = []
        teams = self.group_stage_results[:4]
        while len(teams) > 1:
            next_round_teams = []
            for i in range(0, len(teams), 2):
                team1, team2 = teams[i][0], teams[i + 1][0]
                match_result = self.play_match(team1, team2)
                self.matches.append(match_result)
                winner = match_result['winner']
                next_round_teams.append(winner)
            teams = next_round_teams
        self.knockout_stage_results = teams
        print("Single Elimination Results:")
        for match in self.matches:
            print(f"{match['team1']} vs {match['team2']} - Winner: {match['winner']}")

    def simulate_double_elimination(self):
        print("Double Elimination is not yet implemented.")

    def simulate_round_robin(self):
        print("Round-Robin is not yet implemented.")

    def play_match(self, team1_name, team2_name):
        team1 = next(team for team in self.teams if team.name == team1_name)
        team2 = next(team for team in self.teams if team.name == team2_name)
        overs = 20
        match_format = "T20"
        weather_conditions = "Clear"
        stadium = "Neutral"
        game = CricketGame(team1_name, team2_name, overs, team1.players, match_format, weather_conditions, stadium)
        game.start_game()
        return {
            'team1': team1_name,
            'team2': team2_name,
            'winner': team1_name if team1.score > team2.score else team2_name
        }

    def schedule_matches(self):
        print("Scheduling Matches...")
        self.simulate_group_stage()

    def display_tournament_summary(self):
        print("Tournament Summary:")
        for phase in range(1, self.tournament_phase + 1):
            print(f"Phase {phase}: {self.phases[phase]}")
        print("Knockout Stage Results:")
        for result in self.knockout_stage_results:
            print(f"Winner: {result}")

class CricketGame:
    def __init__(self, team1_name, team2_name, overs, team1_players, match_format, weather_conditions, stadium):
        self.team1 = Team(team1_name, team1_players)
        self.team2 = Team(team2_name, team1_players)
        self.overs = overs
        self.match_format = match_format
        self.weather_conditions = weather_conditions
        self.stadium = stadium
        self.total_balls = overs * 6
        self.match_history = []

    def apply_weather_conditions(self, team):
        effect = {"Clear": 1.0, "Rainy": 0.8, "Windy": 0.9}.get(self.weather_conditions, 1.0)
        for player in team.players:
            if not player.injury_status:
                player.form *= effect
                player.fatigue *= effect

    def play_innings(self, team):
        self.apply_weather_conditions(team)
        for _ in range(self.total_balls):
            runs, shot_type = team.bat()
            if team.get_current_batsman().is_out:
                break
            runs_conceded, ball_type, wickets = team.bowl()
            if wickets > 0:
                team.wickets += wickets

    def display_match_summary(self):
        print(f"Match Summary at {self.stadium}:")
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
        plt.figure(figsize=(12, 8))
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

def create_tournament(teams, format_type):
    return Tournament(teams, format_type)

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
        elif replay == "no":
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()
