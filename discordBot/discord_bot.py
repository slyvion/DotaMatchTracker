import discord
import requests
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

hero_mapping = {
    1: "Anti-Mage",
    2: "Axe",
    3: "Bane",
    4: "Bloodseeker",
    5: "Crystal Maiden",
    6: "Drow Ranger",
    7: "Earthshaker",
    8: "Juggernaut",
    9: "Mirana",
    10: "Morphling",
    11: "Shadow Fiend",
    12: "Phantom Lancer",
    13: "Puck",
    14: "Pudge",
    15: "Razor",
    16: "Sand King",
    17: "Storm Spirit",
    18: "Sven",
    19: "Tiny",
    20: "Vengeful Spirit",
    21: "Windranger",
    22: "Zeus",
    23: "Kunkka",
    25: "Lina",
    26: "Lion",
    27: "Shadow Shaman",
    28: "Slardar",
    29: "Tidehunter",
    30: "Witch Doctor",
    31: "Lich",
    32: "Riki",
    33: "Enigma",
    34: "Tinker",
    35: "Sniper",
    36: "Necrophos",
    37: "Warlock",
    38: "Beastmaster",
    39: "Queen of Pain",
    40: "Venomancer",
    41: "Faceless Void",
    42: "Wraith King",
    43: "Death Prophet",
    44: "Phantom Assassin",
    45: "Pugna",
    46: "Templar Assassin",
    47: "Viper",
    48: "Luna",
    49: "Dragon Knight",
    50: "Dazzle",
    51: "Clockwerk",
    52: "Leshrac",
    53: "Nature's Prophet",
    54: "Lifestealer",
    55: "Dark Seer",
    56: "Clinkz",
    57: "Omniknight",
    58: "Enchantress",
    59: "Huskar",
    60: "Night Stalker",
    61: "Broodmother",
    62: "Bounty Hunter",
    63: "Weaver",
    64: "Jakiro",
    65: "Batrider",
    66: "Chen",
    67: "Spectre",
    68: "Ancient Apparition",
    69: "Doom",
    70: "Ursa",
    71: "Spirit Breaker",
    72: "Gyrocopter",
    73: "Alchemist",
    74: "Invoker",
    75: "Silencer",
    76: "Outworld Destroyer",
    77: "Lycan",
    78: "Brewmaster",
    79: "Shadow Demon",
    80: "Lone Druid",
    81: "Chaos Knight",
    82: "Meepo",
    83: "Treant Protector",
    84: "Ogre Magi",
    85: "Undying",
    86: "Rubick",
    87: "Disruptor",
    88: "Nyx Assassin",
    89: "Naga Siren",
    90: "Keeper of the Light",
    91: "Io",
    92: "Visage",
    93: "Slark",
    94: "Medusa",
    95: "Troll Warlord",
    96: "Centaur Warrunner",
    97: "Magnus",
    98: "Timbersaw",
    99: "Bristleback",
    100: "Tusk",
    101: "Skywrath Mage",
    102: "Abaddon",
    103: "Elder Titan",
    104: "Legion Commander",
    105: "Techies",
    106: "Ember Spirit",
    107: "Earth Spirit",
    108: "Underlord",
    109: "Terrorblade",
    110: "Phoenix",
    111: "Oracle",
    112: "Winter Wyvern",
    113: "Arc Warden",
    114: "Monkey King",
    119: "Dark Willow",
    120: "Pangolier",
    121: "Grimstroke",
    126: "Void Spirit",
    128: "Snapfire",
    129: "Mars",
    135: "Dawnbreaker",
    136: "Marci",
    137: "Primal Beast",
    138: "Muerta",
}


player_mapping = {
    "nigma": "460729799",
    "ango": "312965538",
    "slyvion": "113798198",
    "bajra": "106176512",
    "palanka": "38254237",
    "eldorado": "185456064",
    "frikz": "99678432",
    "jovco": "133374408",
    "kabal": "236938533",
    "gorgi": "123218297",
    "fakeango": "913843739",
}

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name} ({client.user.id})")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!recent_matches'):
        try:
            player_name = message.content.split()[1].lower()
            player_id = player_mapping.get(player_name)
            if player_id:
                url = f"https://api.opendota.com/api/players/{player_id}/matches?limit=5"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()

                    if data:
                        match_details = []
                        for match in data:
                            match_id = match['match_id']
                            hero_id = match['hero_id']
                            win = match['radiant_win'] if match['player_slot'] < 128 else not match['radiant_win']
                            kda = f"{match['kills']}/{match['deaths']}/{match['assists']}"
                            start_time = match['start_time']

                            hero_name = hero_mapping.get(hero_id, f"Hero ID {hero_id}")
                            date_played = datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')

                            match_details.append(f"Match ID: {match_id} | Hero: {hero_name} | Win: {'Win' if win else 'Loss'} | KDA: {kda} | Date: {date_played}")

                        response_message = f"Latest 5 matches for player {player_name} (ID: {player_id}):\n"
                        response_message += '\n'.join(match_details)
                    else:
                        response_message = f"No recent matches found for player {player_name} (ID: {player_id})."

                    await message.channel.send(response_message)
                else:
                    await message.channel.send("Failed to fetch recent matches.")
            else:
                await message.channel.send(f"Player '{player_name}' not found in player mapping.")
        except Exception as e:
            await message.channel.send(f"An error occurred: {str(e)}")

    elif message.content.startswith('!rank'):
        try:
            player_name = message.content.split()[1].lower()
            player_id = player_mapping.get(player_name)
            if player_id:
                url = f"https://api.opendota.com/api/players/{player_id}"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()

                    rank_tier = data.get("rank_tier")
                    if rank_tier:
                        tier = rank_tier // 10
                        tier_name = "Unknown"
                        if tier == 1:
                            tier_name = "Herald"
                        elif tier == 2:
                            tier_name = "Guardian"
                        elif tier == 3:
                            tier_name = "Crusader"
                        elif tier == 4:
                            tier_name = "Archon"
                        elif tier == 5:
                            tier_name = "Legend"
                        elif tier == 6:
                            tier_name = "Ancient"
                        elif tier == 7:
                            tier_name = "Divine"
                        elif tier == 8:
                            tier_name = "Immortal"

                        response_message = f"{player_name}'s rank is {tier_name}"
                    else:
                        response_message = f"No rank information found for player {player_name} (ID: {player_id})."

                    await message.channel.send(response_message)
                else:
                    await message.channel.send("Failed to fetch rank information.")
            else:
                await message.channel.send(f"Player '{player_name}' not found in player mapping.")
        except Exception as e:
            await message.channel.send(f"An error occurred: {str(e)}")

    elif message.content.startswith('!mostplayed'):
        await message.channel.send("not fixed jbg...")

    elif message.content.startswith('!winrate'):
        try:
            player_name = message.content.split()[1].lower()
            player_id = player_mapping.get(player_name)
            if player_id:
                url = f"https://api.opendota.com/api/players/{player_id}/wl"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()

                    win = data.get('win')
                    lose = data.get('lose')

                    if win is not None and lose is not None:
                        total_matches = win + lose
                        win_rate = (win / total_matches) * 100

                        response_message = f"{player_name} has a Win Rate of {win_rate:.2f}% with {total_matches} games played."
                    else:
                        response_message = f"No win/loss data found for player {player_name} (ID: {player_id})."

                    await message.channel.send(response_message)
                else:
                    await message.channel.send("Failed to fetch win/loss data.")
            else:
                await message.channel.send(f"Player '{player_name}' not found in player mapping.")
        except Exception as e:
            await message.channel.send(f"An error occurred: {str(e)}")

    elif message.content.startswith('!id'):
        try:
            player_name = message.content.split()[1].lower()
            player_id = player_mapping.get(player_name)
            if player_id:
                response_message = f"{player_name}'s SteamID is {player_id}."
            else:
                response_message = f"Player '{player_name}' not found in player mapping."
            await message.channel.send(response_message)
        except Exception as e:
            await message.channel.send(f"An error occurred: {str(e)}")

    elif message.content.startswith('!dotabuff'):
        try:
            player_name = message.content.split()[1].lower()
            player_id = player_mapping.get(player_name)
            if player_id:
                response_message = f"{player_name}'s dotabuff profile is : https://www.dotabuff.com/players/{player_id}"
            else:
                response_message = f"Player '{player_name}' not found in player mapping."
            await message.channel.send(response_message)
        except Exception as e:
            await message.channel.send(f"An error occurred: {str(e)}")

    elif message.content.startswith('!opendota'):
        try:
            player_name = message.content.split()[1].lower()
            player_id = player_mapping.get(player_name)
            if player_id:
                response_message = f"{player_name}'s dotabuff profile is : https://www.opendota.com/players/{player_id}"
            else:
                response_message = f"Player '{player_name}' not found in player mapping."
            await message.channel.send(response_message)
        except Exception as e:
            await message.channel.send(f"An error occurred: {str(e)}")

    elif message.content.startswith('!komandi'):
        await message.channel.send("!recent_matches ime //za posledni 5 igri")
        await message.channel.send("!rank ime // za rank")
        await message.channel.send("!winrate ime // za winrate")
        await message.channel.send("!id ime // za id")
        await message.channel.send("!dotabuff/opendota ime // za dotabuff/opendota link")

client.run("bot_token")
