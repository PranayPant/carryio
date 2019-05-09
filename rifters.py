import cassiopeia as cass
from cassiopeia.data import Queue, Position
from cassiopeia.core import Summoner

import json, requests, os

cass.set_riot_api_key('RGAPI-845b32bd-aee5-41c7-9d6f-5acad2aa8048')



def leagues(summoner_name: str, region: str):
    summoner = Summoner(name=summoner_name, region=region)
    print("Name:", summoner.name)
    print("ID:", summoner.id)

    # positions = cass.get_league_positions(summoner, region=region)
    positions = summoner.league_positions
    if positions.fives.promos is not None:
        # If the summoner is in their promos, print some info
        print("Promos progress:", positions.fives.promos.progress)
        print("Promos wins", positions.fives.promos.wins)
        print("Promos losses:", positions.fives.promos.losses)
        print("Games not yet played in promos:", positions.fives.promos.not_played)
        print("Number of wins required to win promos:", positions.fives.promos.wins_required)
    else:
        print("The summoner is not in their promos.")

    print("Name of leagues this summoner is in:")
    for league in positions:
        print(league.name)
    print()

    leagues = summoner.leagues

    my_league = leagues.fives
    entries = my_league.entries
    summoner_names = [ e.summoner.sanitized_name for e in entries ]
    print( f'{len(summoner_names)} summoners in {my_league.name}' )
    return summoner_names

    '''
    BASE_LEAGUE_URL = "https://na1.api.riotgames.com/lol/league/v4/leagues"
    
    league_id = str( leagues.fives.id )
    url = os.path.join( BASE_LEAGUE_URL, league_id, "?api_key=RGAPI-b5b2c3f6-d63d-4f38-8e46-32f2d1dc26d6" )
    print( f'Sending request to {url}' )
    res = requests.get( url )
    
    fh = open( 'silvers.txt', 'w+')
    json_str = res.text()
    fh.write( json.dumps( json_str, indent=3 ) )
    fh.close()
    '''
def ranks( summoner_name, region ):

    summoner = Summoner(name=summoner_name, region=region)
    ranks = summoner.ranks

    my_ranks = [ str(ro.tier) + " " + str(ro.division) for q, ro in ranks.items() ]

    print( my_ranks )

ranks( "jiangpro", "NA" )

