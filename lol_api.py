import requests
import os
from pprint import pprint
from flask import Flask, jsonify
from markupsafe import escape

application = Flask(__name__)


def fetch_data():
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

        champion_data.append(
               {'champion': champ,
                'title': title,
                'story': lore,
                'role': tags,
                'skins': champ_skins,
                'abilities': champ_abilities,
                'passive': champ_passive,
                'ally tips': allytips,
                'enemy tips': enemytips
            }
        )

    return champion_data

@application.route("/champions")
def lol_champions():
    return jsonify(champ_data)


champ_data = fetch_data()

@application.route("/champions/<name>")
def lol_champion(name):
    champ_name = escape(name)
    for c in champ_data:
        if c['champion'] == champ_name:
            return jsonify(c)
    not_found = {'Error': f'Champion {champ_name} not found.'}
    return jsonify(not_found)


if __name__ == "__main__":
    application.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



