import spade
import time
import argparse
from owlready2 import *
import pandas as pd

XMPP_HOST = 'host.docker.internal'

class AgenteOnto(spade.agent.Agent):

    async def setup(self):
        self.add_behaviour(self.BuscarBehaviour())

        self.onto = get_ontology("data/movielens.owl")
        self.onto.load()

        df = pd.read_csv('ml-latest-small/movies.csv')

        def get_genres(genres):
            return [self.onto.Genre(genre) for genre in genres]
                
        for _, row in df.iterrows():
            movie = self.onto.Movie(row['title'])
            movie.tieneGenero = get_genres(row['genres'].split('|'))

    def set_query_args(self, args):
        self.query_args = args

    class BuscarBehaviour(spade.behaviour.OneShotBehaviour):

        async def run(self):
            print(self.agent.onto.search(tieneGenero = self.agent.onto.Genre(self.agent.query_args.genre)))

def main(query_args):
    agent = AgenteOnto(f"agente_onto@{XMPP_HOST}", "env_password")
    agent.set_query_args(query_args)
    agent.start()
    time.sleep(10)

if __name__ == '__main__':
    print("Iniciar")
    parser = argparse.ArgumentParser()
    parser.add_argument('genre', type=str)
    args = parser.parse_args()

    main(args)