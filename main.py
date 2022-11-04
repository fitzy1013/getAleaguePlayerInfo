from bs4 import BeautifulSoup
import requests
import csv
import random


class Player:
    def __init__(self, id, name, position, club):
        self.name = name
        self.position = position
        self.club = club
        self.id = id

    def get_playerID(self):
        return self.id

    def print_info(self):
        print(self.name + " " + self.club + " " + self.position)

try:
    source = requests.get('https://www.ultimatealeague.com/players/')
    source.raise_for_status()

    playerList = []

    soup = BeautifulSoup(source.text, 'html.parser')


except Exception as e:
    print(e)


def playerInfoToCSV():
    players = soup.find('table', { 'id' : 'players-data-table' }).find('tbody').find_all('tr')

    for player in players:
        name = player.find('div', {'class' : 'player-link'}).a.text
        pos = player.find('td', {'class' : 'data-table-desktop-hide data-table-cell'}).text
        club = player.find('div', {'class' : 'club-link club-link-left'}).a.text
        playerEntry = {'name': name, 'pos': pos, 'club': club}
        playerList.append(playerEntry)

    header = {'name', 'pos', 'club'}
    with open('a-league_players.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(playerList)


def checkIfPlayerInSquad(squad: [Player], playerID) :
    for i in squad:
        if i.get_playerID() == playerID:
            return True

    return False

def getRandomXI():
    gk_list = []
    def_list = []
    mid_list = []
    fwd_list = []
    with open('a-league_players.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                p = Player(line_count, row[0], row[2], row[1])
                if row[2] == "GK":
                    gk_list.append(p)
                elif row[2] == "DEF":
                    def_list.append(p)
                elif row[2] == "MID":
                    mid_list.append(p)
                elif row[2] == "FWD":
                    fwd_list.append(p)
            line_count += 1

    squad = []
    squad.append(gk_list[random.randint(0, len(gk_list) - 1)])
    for i in range(0, 4):
        index = random.randint(0, len(def_list) - 1)
        if not checkIfPlayerInSquad(squad, def_list[index].get_playerID()):
            squad.append(def_list[index])

    for i in range(0, 4):
        index = random.randint(0, len(mid_list) - 1)
        if not checkIfPlayerInSquad(squad, mid_list[index].get_playerID()):
            squad.append(mid_list[index])

    for i in range(0, 2):
        index = random.randint(0, len(fwd_list) - 1)
        if not checkIfPlayerInSquad(squad, fwd_list[index].get_playerID()):
            squad.append(fwd_list[index])

    for i in squad:
        i.print_info()

getRandomXI()

