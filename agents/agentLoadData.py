import spade
import argparse
from owlready2 import *
import pandas as pd


class LoadDataAgent(spade.agent.Agent):

    async def setup(self):
        self.onto = get_ontology("data/movielens.owl")
        self.onto.load()
        
        self.load = self.LoadDataBehaviour()
        self.add_behaviour(self.load)

    class LoadDataBehaviour(spade.behaviour.OneShotBehaviour):
        movies_df = pd.read_csv('data/ml-latest-small/movies.csv')
        ratings_df = pd.read_csv('data/ml-latest-small/ratings.csv')
        tags_df = pd.read_csv('data/ml-latest-small/tags.csv')

        async def run(self):
            self.ratings_df.drop(columns='timestamp', inplace=True)
            self.tags_df.drop(columns='timestamp', inplace=True)
            self.load_movies()
            self.load_tags()
            self.load_ratings()
            
        def load_movies(self):
            def get_genres(genres):
                return [self.agent.onto.Genre(genre) for genre in genres]
                
            for _, row in self.movies_df.iterrows():
                title_str = str(row['title']).strip()
                movie_id = 'movie_{}'.format(int(row['movieId']))
                movie = self.agent.onto.Movie(movie_id)
                year_str = re.search(r"(\d{4})", title_str)
                year = None
                if year_str:
                    year = int(year_str.group(1))
                    movie.year = [year]
                title = title_str.replace('({})'.format(year), '').strip()
                movie.title = [title]
                movie.tieneGenero = get_genres(row['genres'].split('|'))

        def load_ratings(self):    
            for _, row in self.ratings_df.iterrows():
                user_id = 'user_{}'.format(int(row['userId']))
                movie_id = 'movie_{}'.format(int(row['movieId']))
                rating_value = float(row['rating'])
                rating_instance = self.agent.onto.Rating('rating__{}-{}'.format(user_id, movie_id))
                rating_instance.ratingValue = [rating_value]
                rating_instance.esCalificadaPor = [self.agent.onto.User(user_id)]
                rating_instance.calificaA = [self.agent.onto.Movie(movie_id)]

        def load_tags(self):
            for _, row in self.tags_df.iterrows():
                user_id = 'user_{}'.format(int(row['userId']))
                movie_id = 'movie_{}'.format(int(row['movieId']))
                tag_value = row['tag']
                tag_instance = self.agent.onto.Tag('tag__{}-{}'.format(user_id, movie_id))
                tag_instance.tagValue.append(tag_value)
                tag_instance.creadaPor = [self.agent.onto.User(user_id)]
                tag_instance.asociadaConPelicula = [self.agent.onto.Movie(movie_id)]

        async def on_end(self):
            print("{} finished with exit code: {}.".format(self.__class__.__name__, self.exit_code))
            await self.agent.stop()

    
def print_instances(entity_type):
    for instance in entity_type.instances():
        print(instance.name)
        for prop in instance.get_properties():
            for value in prop[instance]:
                print("> %s == %s" % (prop.python_name, value))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--XMPP_HOST', type=str, default='localhost')
    args = parser.parse_args()

    agent = LoadDataAgent(f"load_data_agent@{args.XMPP_HOST}", "env_password")
    future = agent.start()
    future.result()
    agent.load.join()

    agent.onto.save('onto_with_instances.rdfxml')