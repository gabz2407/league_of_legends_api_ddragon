import requests
from pprint import pprint
from flask import Flask, jsonify
app = Flask(__name__)


@app.get("/champions")
def lol_champion():
    url = 'https://ddragon.leagueoflegends.com/cdn/14.18.1/data/en_US/champion.json'
    response = requests.get(url)
    data = response.json()['data']

    champion_data = []
    for champ in data:
        champion_url = f'https://ddragon.leagueoflegends.com/cdn/14.18.1/data/en_US/champion/{champ}.json'
        champion_response = requests.get(champion_url)
        champion = champion_response.json()['data'][champ]

        # get title, ally tips, enemy tips and lore
        title = champion['title']
        allytips = champion['allytips']
        enemytips = champion['enemytips']
        lore = champion['lore']
        tags = champion['tags']

        # get skins and skin image
        skins = champion['skins']
        print(champion)
        champ_skins = []
        for skin in skins:
            skin_name = champ
            if skin['name'] != 'default':
                skin_name = skin['name']

            champ_skins.append({
                'name': skin_name,
                'image': f'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ}_{skin["num"]}.jpg'
            })

        # get abilities
        abilities = champion['spells']
        champ_abilities = []
        for ability in abilities:
            ability_id = ability['id']
            ability_name = ability['name']
            ability_description = ability['description']
            ability_image = f'https://ddragon.leagueoflegends.com/cdn/14.13.1/img/spell/{ability_id}.png'

            champ_abilities.append({
                'id': ability_id,
                'ability': ability_name,
                'description': ability_description,
                'image': ability_image
            })

        # get passive
        passive = champion['passive']
        champ_passive = []
        passive_name = passive['name']
        passive_description = passive['description']
        passive_img_id = passive['image']['full']
        passive_image = f'https://ddragon.leagueoflegends.com/cdn/14.13.1/img/passive/{passive_img_id}'

        champ_passive.append({
            'name': passive_name,
            'description': passive_description,
            'image': passive_image
        })

        champion_data.append({
                 champ: {
                    'title': title,
                    'story': lore,
                    'role': tags,
                    'skins': champ_skins,
                    'abilities': champ_abilities,
                    'passive': champ_passive,
                    'ally tips': allytips,
                    'enemy tips': enemytips
                    }
                })

    return jsonify(champion_data)

# if __name__ == "__main__":
#     app.run(debug=True)


