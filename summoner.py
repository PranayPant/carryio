
import json
from enum import Enum

class GameMode( Enum ):

    SOLO = 0
    FLEX = 1

class Summoner:
    '''
    Summoner stats for each ranked game mode
    '''
    def __init__( self, name ):

        self.summonerName = name

        self.game_types = []
        self.ranks = []
        self.wins = []
        self.losses = []
        self.win_rates = []
        self.games_played = []

    def __getitem__( self, key ):
        return self.__dict__[ key ]

    def __setitem__( self, key, value ):
        self.__dict__[ key ] = value

    def __str__( self ):

        json_str =  json.dumps( self.__dict__, indent=3 )
        return json_str

    def to_json( self ):
        return self.__dict__

    def filter( self, mode=GameMode.SOLO ):
        '''
        Only include stats from mode that are from this game mode
        Note: stats are not a list, but singular value
        '''
        try:
            fs = { label: stats[ mode.value ] for label, stats in self.__dict__.items() if label != 'summonerName' }
            obj = { 'summonerName': self.summonerName }
            obj.update( filtered_stats )
            
            return Summoner.from_json( obj )

        except KeyError as err:
            raise Exception("Stats not collected for this game mode")

    def set( self, key, value ):

        self.__setitem__( key, value )

    def update( self, fields ):

        self.__dict__.update( fields )

    def set_from_tup( self, stats ):
        '''
        Example stat tuple:
            ('Ranked Solo', 'SILVER I', '105W', '83L', '(55.9%)')
        '''

        for tup in stats:

            win_num = int(tup[2][:-1])
            loss_num = int(tup[3][:-1])
            win_rate_num = float(tup[4][1:-2])

            self.game_types.append( tup[0] )
            self.ranks.append( tup[1] )
            self.wins.append( win_num )
            self.losses.append( loss_num )
            self.win_rates.append( win_rate_num )
            self.games_played.append( win_num + loss_num )

    @classmethod
    def list_filter( cls, summoners, tfield, tvalue ):
        filtered_summs = [ summ for summ in summoners if summ[ tfield ] >= tvalue ]
        return filtered_summs

    @classmethod
    def list_json( cls, summoners ):
        jsons = [ s.to_json() for s in summoners ]
        return jsons

    @classmethod
    def from_json( cls, obj ):

        summ = Summoner( obj.get('summonerName') )
        for k,v in obj.items():
            summ.set( k, v )

        return summ

    @classmethod
    def sort( cls, summoners, key, inc=False ):
        '''
        Implement quicksort on a list of Summoners
        Sort by key
        '''
        
        def quicksort( items, low, high ):
    
            def partition(items, low, high):

                i = high + 1
                pivot = items[low][key]

                for j in range(high, low, -1):
                    if inc:
                        if items[j][key] >= pivot:
                            i -= 1
                            items[i], items[j] = items[j], items[i]
                    else:
                        if items[j][key] <= pivot:
                            i -= 1
                            items[i], items[j] = items[j], items[i]

                items[i - 1], items[low] = items[low], items[i - 1]

                return i - 1

            if low < high and high < len(items) and low > -1:

                pi = partition( items, low, high )

                quicksort( items, low, pi - 1 )
                quicksort( items, pi + 1, high )


        quicksort( summoners, 0, len(summoners) - 1 )









