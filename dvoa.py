import csv
import os

# ['Player', 'Team', 'DYAR Rank', 'DYAR', 'YAR Rank', 'YAR', 'DVOA Rank', 'DVOA', 'VOA Rank', 'VOA', 'QBR Rank', 'QBR', 'Pass', 'Yards', 'EYds Rank', 'EYds', 'TD', 'FK', 'FL', 'INT', 'C%', 'DPI', 'ALEX Rank', 'ALEX']
# 2020-Quarterbacks.csv'

def stat_ranking(stat_per_player):
    return sorted(stat_per_player.items(), key=lambda item: item[1], reverse=True)

def stat_ranking_n(stat_per_player, n):
    return sorted(stat_per_player.items(), key=lambda item: item[1], reverse=True)[0:n]

def get_stat(player, stat_per_player):
    return player, stat_per_player[player]

def find_ranking(player, stat_per_player):
    rank = 1
    for p, stat in stat_ranking(stat_per_player):
        if (player == p):
            print('{0}. {1}: {2}'.format(rank, player, stat))
        else:
            rank += 1

def print_stat_ranking(stat_per_player, pass_per_player, n):
    top_stat = stat_ranking_n(stat_per_player, n)
    rank = 1
    for player, stat in top_stat:
        print('{0};{1};{2};{3}'.format(rank, player, pass_per_player[player], stat))
        rank += 1

def print_dvoa_ranking(dvoa_per_player, pass_per_player, n):
    top_dvoa = stat_ranking_n(dvoa_per_player, n)
    rank = 1
    for player, dvoa in top_dvoa:
        print('{0};{1};{2};{3:.1%}'.format(rank, player, pass_per_player[player], dvoa))
        rank += 1

def print_stat(player, stat_per_player):
    print('{0}: {1}'.format(player, stat_per_player[player]))

def print_dvoa(player, stat_per_player):
    print('{0}: {1:.1%}'.format(player, stat_per_player[player]))

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.csv')]

dyar_per_player = {}
for f in files:
    with open(f) as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        player_index = header.index('Player')
        dyar_index = header.index('DYAR')
        for line in reader:
            player = line[player_index]
            dyar = int(line[dyar_index])
            if player in dyar_per_player:
                dyar_per_player[player] += dyar
            else:
                dyar_per_player[player] = dyar


def str_to_float(p):
    return float(p.strip('%')) / 100

dvoa_per_player = {}
pass_per_player = {}
for f in files:
    with open(f) as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        player_index = header.index('Player')
        dvoa_index = header.index('DVOA')
        plays_index = header.index('Pass')
        for line in reader:
            player = line[player_index]
            dvoa = str_to_float(line[dvoa_index])
            plays = float(line[plays_index])
            if player in dvoa_per_player:
                dvoa_per_player[player] += dvoa * plays
                pass_per_player[player] += plays
            else:
                dvoa_per_player[player] = dvoa * plays
                pass_per_player[player] = plays

for player in dvoa_per_player:
    if (pass_per_player[player] < 4000):
        dvoa_per_player[player] = 0
    dvoa = dvoa_per_player[player] / pass_per_player[player]
    dvoa_per_player[player] = dvoa


print('Top DVOA')
print_dvoa_ranking(dvoa_per_player, pass_per_player, 25)

print()

print('Top DYAR')
print_stat_ranking(dyar_per_player, pass_per_player, 25)

print()
print_dvoa('B. Favre', dvoa_per_player)
print_dvoa('J. Elway', dvoa_per_player)
print_dvoa('J. Kelly', dvoa_per_player)
print_dvoa('E. Manning', dvoa_per_player)

# print('{0},{1},{2}'.format('P. Manning', stat_per_player['P. Manning']['Pass'], stat_per_player['P. Manning']['DYAR']))
# print('{0},{1},{2}'.format('P. Mahomes', stat_per_player['P. Mahomes']['Pass'], stat_per_player['P. Mahomes']['DYAR']))
