
import sys, os, logging
sys.path.append( os.path.abspath('.') )

import time, json
from summ_api import *

if len( sys.argv ) != 2:
    print("Usage: python match_api <summoner_name>")
    sys.exit()

name = sys.argv[1]
match_metas = get_match_metas( get_account_id( name ) )

num = 1
print( f'Processing {len(match_metas)} matches' )
for meta in match_metas:

    match_id = meta['gameId']
    player_infos = get_match_performance( match_id )
    parsed_infos = extract_infos( player_infos )
    player_scores = scores( parsed_infos )

    print(f'Match({num}) {match_id}: {player_scores}')
    num += 1
