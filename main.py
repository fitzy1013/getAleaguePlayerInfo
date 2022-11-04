from bs4 import BeautifulSoup
import requests
import csv

""""
class Player:
    def __init__(self, name, position, club):
        self.name = name
        self.position = position
        self.club = club

"""

try:
    source = requests.get('https://www.ultimatealeague.com/players/')
    source.raise_for_status()

    playerList = []

    soup = BeautifulSoup(source.text, 'html.parser')

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


except Exception as e:
    print(e)

