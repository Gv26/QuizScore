"""Print quiz team final scores as percentages sorted by team name."""
import csv


def quiz_scores(filename):
    """Return dictionary of quiz team name and percentage final scores
    using data from TSV file of individual round scores for each team.

    Score for a team calculated by summing their score for each round as
    a fraction of the maximum score for that round.
    """
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter="\t", quoting=csv.QUOTE_NONNUMERIC)
        # Get number of rounds from data.
        rounds = len(next(reader)) - 1

        # Create list of maximum scores from each round.
        round_max = []
        for column in range(1, rounds + 1):
            round_max.append(max(row[column] for row in reader))
            file.seek(0)

        # Create list of minimum scores from each round.
        round_min = []
        for column in range(1, rounds + 1):
            round_min.append(min(row[column] for row in reader))
            file.seek(0)

        round_range = [round_max[i] - round_min[i] for i in range(rounds)]
        # Rounds where every team scored the same don't count.
        rounds -= round_range.count(0)

        # Create dictionary for team names and respective final scores.
        results = {}
        for row in reader:
            score = 0
            for j in range(rounds):
                # Rounds where every team scored the same don't count.
                if round_range[j] != 0:
                    # For rounds where negative scores exist, shift all
                    # scores up evenly so the minimum becomes zero.
                    if round_min[j] >= 0:
                        score += row[j+1] / round_max[j]
                    else:
                        score += (row[j+1] - round_min[j]) / round_range[j]
            # Convert to percentage and add to dictionary.
            results[row[0]] = score * 100/rounds

        return results


if __name__ == "__main__":
    for team, result in sorted(quiz_scores('animesoc_quiz_data.txt').items()):
        print(team + ':', str(round(result, 1)) + '%')
