
import requests, json, sys, math

API_KEY = "RGAPI-d2d0424d-44ef-4da5-ba30-468ba95214a5"
HEADERS = {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": f"{API_KEY}",
    "Accept-Language": "en-US,en-AS;q=0.7,en;q=0.3",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
     (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"
}

def get_account_id( name ):

    URL = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}"
    data = requests.get( URL, headers=HEADERS ).json()

    return data['accountId']

def get_match_metas( account_id, limit=50 ):
     URL = f"https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?endIndex={limit}"
     data = requests.get( URL, headers=HEADERS ).json()

     return data['matches']

def get_match_performance( match_id ):

    URL = f"https://na1.api.riotgames.com/lol/match/v4/matches/{match_id}"
    data = requests.get( URL, headers=HEADERS ).json()

    try:
        players = list( filter( lambda p: p['timeline'].get('xpPerMinDeltas') != None, data['participants'] ) )
        
    except Exception as err:
        print(json.dumps(data))
        sys.exit(1)

    return players

def extract_infos( players ):
    ret_obj = {}
    try:
        dmg_dealts = [ int(p['stats']['totalDamageDealtToChampions']) for p in players ]
        dmg_takens = [ int(p['stats']['totalDamageTaken']) for p in players ]
        kills      = [ int(p['stats']['kills']) for p in players ]
        deaths     = [ int(p['stats']['deaths']) for p in players ]
        assists    = [ int(p['stats']['assists']) for p in players ]
        kdrs       = [ (k + a)/(k + d + a) if k + d + a > 0 else 1 for (k, d, a) in zip( kills, deaths, assists ) ]
        objec_dmgs = [ int(p['stats']['damageDealtToObjectives']) for p in players ]
        gold_spent = [ int(p['stats']['goldSpent']) for p in players ]
        exp_gained = [ sum( [ int(delt) * 10 for delt in p['timeline']['xpPerMinDeltas'].values() ] ) for p in players ]

        ret_obj = { 'dd': dmg_dealts, 'dt': dmg_takens, 'kdr': kdrs, 'od': objec_dmgs, 'gs': gold_spent, 'eg': exp_gained }

    except Exception as err:
        print(f'Caught {err}')
        with open( './data/matches.txt', 'w+' ) as fh:
            print(f'{len(players)} players in this match')
            fh.write( json.dumps(players, indent=3) )
            sys.exit(1)

    return ret_obj

def scores( infos ):

    score    = lambda impact, pressure: 0.5 * impact + 0.5 * pressure
    impact   = lambda dd, dt, kdr, od: (od + dd + dt) * kdr
    pressure = lambda gs, eg: gs * eg

    impact_args   = zip( infos['dd'], infos['dt'], infos['kdr'], infos['od'] )
    pressure_args = zip( infos['gs'], infos['eg'] )

    impacts   = [ impact( *arg ) for arg in impact_args ]
    pressures = [ pressure( *arg ) for arg in pressure_args ]

    score_args = zip( impacts, pressures )
    scores     = [ score( *arg ) for arg in score_args ]

    scores_norm = [ round( s*100/math.fsum( scores ), 2 ) for s in scores ]

    return scores_norm
