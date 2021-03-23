import spade
import time
import argparse
from owlready2 import *
import pandas as pd
import json

class AgenteJson(spade.agent.Agent):

    async def setup(self):
        self.add_behaviour(self.BuscarBehaviour())

        self.onto = get_ontology("data/movielens.owl")
        self.onto.load()

        df = pd.read_csv('ml-latest-small/movies.csv')

        #def get_genres(genres):
        #    return [self.onto.Genre(genre) for genre in genres]
                
        #for _, row in df.iterrows():
        #    movie = self.onto.Movie(row['title'])
        #    movie.tieneGenero = get_genres(row['genres'].split('|'))
        
        
def set_query_args(self, args):
        self.query_args = args

    class BuscarBehaviour(spade.behaviour.OneShotBehaviour):

        async def run(self):
            #print(self.agent.onto.search(tieneGenero = self.agent.onto.Genre(self.agent.query_args.genre)))
            mensaje = Mensaje(args.data1, args.data2, args.data3)
            serialize = json.dumps(mensaje, cls=Encoder, indent=4)
            #un print rápidito
            print serialize
            

def main(query_args):
    agent = AgenteJson("usuario", "json")
    agent.set_query_args(query_args)
    agent.start()
    time.sleep(10)

if __name__ == '__main__':
    print("Inicio agente presentador json")
    parser = argparse.ArgumentParser()
    parser.add_argument('dato1', type=str)
    parser.add_argument('dato2', type=str)
    parser.add_argument('dato3', type=str)
    args = parser.parse_args()

    main(args)
    
class Mensaje(object):
    
    def __init__(self, a1, a2, a3):
        self.data1 = a1
        self.data2 = a2
        self.data3 = a3

class Encoder(json.JSONEncoder):
 
    def default(self, obj):
        return obj.__dict__