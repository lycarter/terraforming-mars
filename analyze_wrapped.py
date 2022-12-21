import csv
import json
import datetime

def monthNumToMonthName(m):
    datetime_object = datetime.datetime.strptime(str(m), "%m")
    return datetime_object.strftime("%b")

def find_best_months(wins):
    months = []
    max_wins = 0
    for i in range(len(wins)):
        if wins[i] > max_wins:
            months = [monthNumToMonthName(i+1)]
            max_wins = wins[i]
        elif wins[i] == max_wins:
            months.append(monthNumToMonthName(i+1))
            
    return (months, max_wins)

def format_played(played):
    formatted = []
    for play in played:
        formatted.append("{0}: {1}/{2}".format(play[0], play[1], play[2] if len(play) == 3 else "x"))
    return formatted

def most_played_corps(corps):
    sortedCorps = []
    for corp in corps:
        sortedCorps.append((corp, sum([corps[corp][name] for name in corps[corp]])))
    sortedCorps.sort(key=lambda x: x[1], reverse=True)
    return sortedCorps

def playedToDict(played):
    return {x[0]: x[1] for x in played}

def find_least_played(sortedCorps, played):
    toReturn = []
    playedDict = playedToDict(played)
    for corp in sortedCorps:
        if len(toReturn) == 10:
            break
        if corp[0] not in playedDict:
            toReturn.append([corp[0], 0, corp[1]])
    for corp in sortedCorps:
        if len(toReturn) < 10:
            if playedDict[corp[0]] == 1:
                toReturn.append([corp[0], 1, corp[1]])
        else:
            break
    return toReturn

def reverse(l):
    l.reverse()
    return l



names = ["Landon", "Amy", "Victor", "Lindsey"]

corps = {} # {corp: {name: playCount}}
corps_played_by_name = {name: {} for name in names} # {name: {corp: playCount}}
total_plays_by_name = {name: 0 for name in names}
wins_by_month_by_name = {name: [0]*12 for name in names}

final_info = {name: {"total games": 0, "best month(s)": [], "wins in best month": 0, "most played": [], "least played": []} for name in names}


with open("games.tsv", "r") as games:
    tsv_reader = csv.DictReader(games, delimiter="\t")
    next(tsv_reader)
    for game in tsv_reader:
        # print(game)
        score = {n: 0 for n in names}
        for name in names:
            corp = game[name + "Corp"]
            if corp == None or corp == "":
                continue
            if corp not in corps:
                corps[corp] = {n: 0 for n in names}
            corps[corp][name] += 1
            if corp not in corps_played_by_name[name]:
                corps_played_by_name[name][corp] = 0
            corps_played_by_name[name][corp] += 1
            total_plays_by_name[name] += 1
            score[name] = int(game[name + "Score"])
        scores = list(score.items())
        scores.sort(key=lambda x: x[1])
        winner = scores[-1][0]
        month = datetime.datetime.strptime(game["date"], "%m/%d/%y").month
        wins_by_month_by_name[winner][month-1] += 1

# print(corps)

# print(total_plays_by_name)

# print(wins_by_month_by_name)

mostPopularCorps = most_played_corps(corps)

for name in corps_played_by_name:
    played = list(corps_played_by_name[name].items())
    played.sort(key=lambda x: x[1])

    final_info[name]["total games"] = total_plays_by_name[name]
    wins = find_best_months(wins_by_month_by_name[name])
    final_info[name]["best month(s)"] = wins[0]
    final_info[name]["wins in best month"] = wins[1]

    final_info[name]["most played"] = format_played(reverse(played[-6:-1]))
    final_info[name]["least played"] = format_played(find_least_played(mostPopularCorps, played))


    # print(played)
    # print(name + ": " + played)

print(json.dumps(final_info, indent=2))


