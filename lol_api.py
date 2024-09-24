import requests
from pprint import pprint

def champion():
    url = 'https://ddragon.leagueoflegends.com/cdn/14.18.1/data/en_US/champion.json'
    response = requests.get(url)
    champions = response.json()['data']
    pprint(champions)

    

champion()