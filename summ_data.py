
import json
from pyquery import PyQuery as pq

from summoner import Summoner

def scrape( name, region='na' ):

    url = f"https://lol.mobalytics.gg/summoner/{region}/{name}?game-types=2&season=13"

    d = pq(url=url)

    divs = d('div')
    champs_infos = [ pq(div).find('p').text() for div in divs if pq(div).attr('class') and "champions-statisticstyles__ChampionInfoRow" in pq(div).attr('class') ]
    lp = [ pq(div).text() for div in divs if pq(div).attr('class') and "profilestyles__LP" in pq(div).attr('class') ]
    win_rate = [ pq(div).text() for div in divs if pq(div).attr('class') and "profilestyles__WinRate" in pq(div).attr('class') ]
    game_types = [ pq(div).text() for div in divs if pq(div).attr('class') and "profilestyles__TierInfoGameType" in pq(div).attr('class') ]

    spans = d('span')
    wins = [ pq(span).text() for span in spans if pq(span).attr('class') and "profilestyles__Wins" in pq(span).attr('class') ]
    losses = [ pq(span).text() for span in spans if pq(span).attr('class') and "profilestyles__Losses" in pq(span).attr('class') ]

    ps = d('p')
    ranks = [ pq(p).text() for p in ps if pq(p).attr('class') and "profilestyles__TierInfoLabel" in pq(p).attr('class') ]

    summoner = Summoner( name )
    stats = zip( game_types, ranks, wins, losses, win_rate )
    summoner.set_from_tup( stats )

    return summoner
