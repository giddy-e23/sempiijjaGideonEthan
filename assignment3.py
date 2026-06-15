
import random


def future_feature_placeholder():
	pass


def ask_choice(prompt, valid_choices):
	while True:
		choice = input(prompt).strip().lower()
		if choice in valid_choices:
			return choice
		print("Invalid choice. Try again.")


def simulate_match(team_strength, morale, injuries, opponent_rating, tactic_bonus=0):
	team_score = team_strength + morale - (injuries * 8) + tactic_bonus + random.randint(-10, 10)
	opponent_score = opponent_rating + random.randint(-8, 8)

	if team_score > opponent_score + 5:
		return "win"
	if abs(team_score - opponent_score) <= 5:
		return "draw"
	return "loss"


def pre_tournament_prep(morale, injuries, strength):
	print("\nPre-tournament preparation begins.")
	print("You have 3 preparation days before the World Cup starts.\n")

	day = 1
	while day <= 3:
		print(f"Day {day}: morale={morale}, injuries={injuries}, strength={strength}")
		print("1. Hard training")
		print("2. Friendly match")
		print("3. Recovery")
		print("4. Rest")
		choice = ask_choice("Choose an action: ", {"1", "2", "3", "4"})

		if choice == "1":
			strength += 6
			morale += 2
			injuries += 1
			print("The squad trained hard and improved, but picked up minor fatigue.")
		elif choice == "2":
			outcome = random.choice(["win", "draw", "loss"])
			if outcome == "win":
				morale += 5
				strength += 2
				print("The friendly was a strong win. Morale rises.")
			elif outcome == "draw":
				morale += 2
				print("The friendly ended level. The squad stays steady.")
			else:
				morale -= 3
				injuries += 1
				print("The friendly went badly and one player is carrying a knock.")
		elif choice == "3":
			if injuries == 0:
				print("Everyone is already fit. Recovery would waste a day, so you move on.")
				day += 1
				continue
			injuries = max(0, injuries - 2)
			morale += 1
			print("Recovery reduced injuries and steadied the squad.")
		else:
			morale += 1
			print("The team rested and kept energy in reserve.")

		day += 1

	return morale, injuries, strength


def group_stage(morale, injuries, strength):
	print("\nGroup stage begins.")
	points = 0
	wins = 0
	losses = 0
	match = 1

	while match <= 3:
		print(f"\nGroup Match {match}")
		print(f"Current form: points={points}, morale={morale}, injuries={injuries}, strength={strength}")
		print("1. Attack")
		print("2. Balanced")
		print("3. Defend")
		print("4. Call recovery session instead")
		choice = ask_choice("Choose a tactic: ", {"1", "2", "3", "4"})

		if choice == "4":
			if injuries == 0:
				print("No players need recovery right now. Skipping to the next match.")
				match += 1
				continue
			injuries = max(0, injuries - 1)
			morale += 1
			print("A short recovery session helps the squad.")
			match += 1
			continue

		tactic_bonus = 0
		if choice == "1":
			tactic_bonus = 8
			morale -= 1
		elif choice == "2":
			tactic_bonus = 4
		else:
			tactic_bonus = 1
			morale += 1

		result = simulate_match(
			team_strength=strength,
			morale=morale,
			injuries=injuries,
			opponent_rating=60 + (match * 4),
			tactic_bonus=tactic_bonus,
		)

		if result == "win":
			print("You won the match.")
			points += 3
			wins += 1
			morale += 3
			strength += 1
		elif result == "draw":
			print("The match ended in a draw.")
			points += 1
			morale += 1
		else:
			print("The team lost the match.")
			losses += 1
			morale -= 3
			injuries += 1

		if losses >= 2:
			print("Too many group-stage losses. The tournament ends here.")
			break

		match += 1

	qualified = points >= 4
	if qualified:
		print(f"\nGroup stage complete. You qualified with {points} points.")
	else:
		print(f"\nGroup stage complete. You failed to qualify with {points} points.")

	return qualified, morale, injuries, strength


def knockout_stage(morale, injuries, strength):
	print("\nKnockout stage begins.")
	rounds = ["Round of 16", "Quarter-final", "Semi-final", "Final"]

	for round_name in rounds:
		print(f"\n{round_name}")
		print(f"Current form: morale={morale}, injuries={injuries}, strength={strength}")
		print("1. Attack")
		print("2. Balanced")
		print("3. Defend")
		print("4. Recovery day")
		choice = ask_choice("Choose a tactic: ", {"1", "2", "3", "4"})

		if choice == "4":
			if injuries == 0:
				print("The squad is already fit, so the recovery day is skipped.")
				continue
			injuries = max(0, injuries - 1)
			morale += 1
			print("Recovery helps the squad, and you move to the next round.")
			continue

		if choice == "1":
			tactic_bonus = 9
			morale -= 1
		elif choice == "2":
			tactic_bonus = 5
		else:
			tactic_bonus = 2
			morale += 1

		result = simulate_match(
			team_strength=strength,
			morale=morale,
			injuries=injuries,
			opponent_rating=72 + (rounds.index(round_name) * 5),
			tactic_bonus=tactic_bonus,
		)

		if result == "win":
			print(f"You advance from the {round_name}.")
			morale += 3
			strength += 2
			if round_name == "Final":
				print("You have won the 2026 FIFA World Cup.")
				break
			continue

		if result == "draw":
			print("The match goes to penalties.")
			penalty_chance = morale + strength - (injuries * 4) + random.randint(-5, 5)
			if penalty_chance >= 80:
				print(f"You win the penalties and advance from the {round_name}.")
				morale += 2
				strength += 1
				if round_name == "Final":
					print("You have won the 2026 FIFA World Cup.")
					break
				continue

			print(f"You lose on penalties in the {round_name}.")
			break

		print(f"You lose the {round_name}. The tournament is over.")
		break


def main():
	print("2026 FIFA World Cup Team Manager Simulation")
	print("Your choices shape morale, injuries, and strength.\n")

	morale = 50
	injuries = 0
	strength = 55

	future_feature_placeholder()

	morale, injuries, strength = pre_tournament_prep(morale, injuries, strength)

	qualified, morale, injuries, strength = group_stage(morale, injuries, strength)
	if not qualified:
		print("\nSimulation over: the team did not reach the knockout rounds.")
		return

	knockout_stage(morale, injuries, strength)


if __name__ == "__main__":
	main()