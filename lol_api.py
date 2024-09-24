import requests
from pprint import pprint


skin_img_url = 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/'
def lol_champion():
    url = 'https://ddragon.leagueoflegends.com/cdn/14.18.1/data/en_US/champion.json'
    response = requests.get(url)
    data = response.json()['data']

    champion_data = []
    for champ in data:
        champion_url = f'https://ddragon.leagueoflegends.com/cdn/14.18.1/data/en_US/champion/{champ}.json'
        champion_response = requests.get(champion_url)
        champion = champion_response.json()['data'][champ]

        title = champion['title']
        allytips = champion['allytips']
        enemytips = champion['enemytips']
        print(enemytips)
        story = champion['lore']

        skins = champion['skins']
        champ_skins = []
        for skin in skins:
            skin_name = champ
            if skin['name'] != 'default':
                skin_name = skin['name']

            champ_skins.append({
                'name': skin_name,
                'image': f'{skin_img_url}{champ}_{skin['num']}.jpg'
            })

        abilities = champion['spells']
        champ_abilities = []
        for ability in abilities:
            ability_id = ability['id']
            ability_name = ability['name']
            ability_description = ability['description']
            champ_abilities.append({
                'id': ability_id,
                'ability': ability_name,
                'description': ability_description
            })

        champion_data = [ {
            '2024': {
                'champion': champion,
                'title': title,
                'story': story,
                'skins': champ_skins,
                'abilities': champ_abilities

            }}]

        break

lol_champion()