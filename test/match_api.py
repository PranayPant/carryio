
import sys, os, logging, json, time
from threading import Thread
sys.path.append( os.path.abspath('.') )

from summ_api import *

def master_func( match_id, all_scores ):
    (player_infos, player_idens) = get_match_performance( match_id )
    parsed_infos, ordered_idens = extract_infos( player_infos, player_idens )
    all_scores.append( scores( parsed_infos, ordered_idens ) )

if len( sys.argv ) != 2:
    print("Usage: python match_api <summoner_name>")
    sys.exit()

name = sys.argv[1]
match_metas = get_match_metas( get_account_id( name ) )

print( f'Processing {len(match_metas)} matches' )

start = time.process_time()

all_scores = []
threads = [ Thread( target=master_func, args=[ meta['gameId'], all_scores ] ) for meta in match_metas ]
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

end = time.process_time()

print(f'Analyzed {len(match_metas)} matches in {end-start}s')
with open('./data/matches.txt', 'w+') as f:
    f.write( json.dumps(all_scores, indent=3) )
