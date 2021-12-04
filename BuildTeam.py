import sqlite3

connection = sqlite3.connect('/Users/halleypark/PycharmProjects/pokemon type chart.db')

cursor = connection.cursor()


class TeamMember:
    def __init__(self, name, move_1, move_2, move_3, move_4):
        self.name = name
        self.move_1 = move_1
        self.move_2 = move_2
        self.move_3 = move_3
        self.move_4 = move_4

    def __str__(self):
        return f"{self.name}, {self.move_1}, {self.move_2}, {self.move_3}, {self.move_4}"


def get_move(effectiveness_list, multiplier, pokemon_move):
    rows = cursor.execute("SELECT Defending_Type, Multiplier "
                          "FROM Moves, Effectiveness_Chart "
                          "WHERE Multiplier = ? "
                          "AND (CATEGORY = 'Physical' OR CATEGORY = 'Special') "
                          "AND Moves.TYPE = Effectiveness_Chart.Attacking_Type "
                          "AND NAME = ?", (multiplier, pokemon_move,)).fetchall()
    for effectiveness in rows:
        if effectiveness not in effectiveness_list:
            effectiveness_list.append(effectiveness)


def get_moves(multiplier, pokemon):
    effectiveness_list = []

    get_move(effectiveness_list, multiplier, pokemon.move_1)

    get_move(effectiveness_list, multiplier, pokemon.move_2)

    get_move(effectiveness_list, multiplier, pokemon.move_3)

    get_move(effectiveness_list, multiplier, pokemon.move_4)

    return effectiveness_list


def filter_type(original_list, filtered_list):
    for original in original_list:
        for filtered in filtered_list:
            if original[0] == filtered[0]:
                filtered_list.remove(filtered)


team = []
team_number = 6

while len(team) < team_number:
    choose_pokemon = input('Choose a Pokemon. ').strip()
    rows = cursor.execute("SELECT * FROM Pokemon WHERE Name = ?", (choose_pokemon,)).fetchall()
    if len(rows) != 1:
        print("Couldn't Find Pokemon.")
        print(choose_pokemon)
        continue

    move_1 = input('Choose a move. ').strip()
    rows = cursor.execute("SELECT * FROM Moves WHERE Name = ?", (move_1,)).fetchall()
    if len(rows) != 1:
        print("Couldn't Find Move.")
        print(move_1)
        continue
    move_2 = input('Choose a move. ').strip()
    rows = cursor.execute("SELECT * FROM Moves WHERE Name = ?", (move_2,)).fetchall()
    if len(rows) != 1:
        print("Couldn't Find Move.")
        print(move_2)
        continue
    move_3 = input('Choose a move. ').strip()
    rows = cursor.execute("SELECT * FROM Moves WHERE Name = ?", (move_3,)).fetchall()
    if len(rows) != 1:
        print("Couldn't Find Move.")
        print(move_3)
        continue
    move_4 = input('Choose a move. ').strip()
    rows = cursor.execute("SELECT * FROM Moves WHERE Name = ?", (move_4,)).fetchall()
    if len(rows) != 1:
        print("Couldn't Find Move.")
        print(move_4)
        continue

    member = TeamMember(choose_pokemon, move_1, move_2, move_3, move_4)
    print(member)
    team.append(member)
print()
print('Defensive Analysis')
for pokemon in team:
    rows = cursor.execute("SELECT Name, EC1.Attacking_Type, EC1.Multiplier * IFNULL(EC2.Multiplier, 1) "
                          "FROM Pokemon P , Effectiveness_Chart EC1 "
                          "LEFT JOIN Effectiveness_Chart EC2 "
                          "ON P.Type_2 = EC2.Defending_Type "
                          "AND EC1.Attacking_Type = EC2.Attacking_Type "
                          "WHERE P.Type_1 = EC1.Defending_Type "
                          "AND EC1.Multiplier * IFNULL(EC2.Multiplier, EC1.Multiplier) >= 2 "
                          "AND Name = ?", (pokemon.name,)).fetchall()
    print(pokemon)
    print(rows)
    print()

print('Offensive Analysis')
for pokemon in team:

    super_effective = get_moves(2, pokemon)

    effective = get_moves(1, pokemon)

    ineffective = get_moves(.5, pokemon)

    immune = get_moves(0, pokemon)

    filter_type(super_effective, effective)
    filter_type(super_effective, ineffective)
    filter_type(super_effective, immune)
    filter_type(effective, ineffective)
    filter_type(effective, immune)
    filter_type(ineffective, immune)

    print(pokemon)
    print('Super Effective Types')
    print(super_effective)
    print('Effective Types')
    print(effective)
    if len(ineffective) > 0:
        print('Ineffective Types')
        print(ineffective)
    if len(immune) > 0:
        print('Immune Types')
        print(immune)
    print()
