import os
import pandas as pd
import rdflib
import re
from rdflib import RDF, RDFS, OWL, XSD, Literal
from tqdm import tqdm




# seperate a camalCased word
def split_camel_case(text):
    if text == "TV":
        return text
    else:
        return re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', text)




def preprocess_data(csv_path):
    df = pd.read_csv(csv_path)

    # Split rows that contain multiple values
    df["cast"].str.split(",")
    df['listed_in'].str.split(",")
    df['country'].str.split(",")
    df['director'].str.split(",")

    # Fill blank rows
    df = df.fillna("Unknown")

    # Put everything in CamelCase and remove some punctuation characters
    df.country = df.country.str.replace(" ", "")
    df.director = df.director.str.replace(" ", "")
    df.cast = df.cast.str.replace(" ", "")
    df.duration = df.duration.str.replace(" ", "")
    df['cast'] = df['cast'].apply(lambda actor: re.sub('\"[^\"]*\"', '', actor))
    df.listed_in = df.listed_in.str.replace(" ", "")
    df['title'] = df['title'].str.replace(' ', '').str.replace('\"', '')

    return df




def create_rdf_graph():
    # Create RDF graph
    g = rdflib.Graph()

    # Bind namespaces
    schema = rdflib.Namespace("http://example.org/")
    g.bind("ex", schema)
    g.bind('rdf', RDF)
    g.bind('rdfs', RDFS)

    return g, schema
def add_classes_to_graph(g, schema):
    # Define Namespaces
    Media = schema['Media']
    TV_show = schema['TV_show']
    Movie = schema['Movie']
    Person = schema['Person']
    Actor = schema['Actor']
    Country = schema['Country']
    Genre = schema['Genre']
    AgeLimit = schema['Age_category']
    Director = schema['Director']

    # Media
    g.add((Media, RDF.type, RDFS.Class))

    # TV_Show
    g.add((TV_show, RDF.type, RDFS.Class))
    g.add((TV_show, RDFS.subClassOf, Media))

    # Movie
    g.add((Movie, RDF.type, RDFS.Class))
    g.add((Movie, RDFS.subClassOf, Media))

    # Person
    g.add((Person, RDF.type, RDFS.Class))

    # Actors
    g.add((Actor, RDF.type, RDFS.Class))
    g.add((Actor, RDFS.subClassOf, Person))

    # Directeur
    g.add((Director, RDF.type, RDFS.Class))
    g.add((Director, RDFS.subClassOf, Person))

    # Country
    g.add((Country, RDF.type, RDFS.Class))

    # Genre
    g.add((Genre, RDF.type, RDFS.Class))

    # Age_Limit
    g.add((AgeLimit, RDF.type, RDFS.Class))


def add_properties_to_graph(g, schema):
    # Namespaces
    hasId = schema['hasId']
    directedBy = schema['directedBy']
    containsActorNamed = schema['containsActorNamed']
    figuresIn = schema['appearsIn']
    producedIn = schema['producedIn']
    addedOnNetflixIn = schema['addedOnNetflixIn']
    duration = schema['hasDuration']
    durationInMin = schema['hasDurationInMin']
    hasGenre = schema['hasGenre']
    description = schema['hasDescription']
    ageLimitedTo = schema['ageLimitedTo']
    releaseYear = schema['releasedIn']
    # inverse of age_limit
    isAgeLimitationOf = schema['isAgeLimitationFor']
    # inverse of produced
    location_of = schema['isLocationOf']
    # inverseOfduration
    durationOf = schema['isDurationOf']
    # inverseOfGenre
    isGenreOf = schema['isGenreOf']
    # inverseOf directedBY
    isDirectorOf = schema['isDirectorOf']

    # create the properties and spoecify domain + range (id)
    # An id is unique, that's why it is a functional Property
    g.add(((hasId, RDF.type, RDF.Property)))
    g.add((hasId, RDFS.domain, schema['Media']))
    g.add((hasId, RDFS.range, XSD.string))
    g.add((hasId, RDF.type, OWL.FunctionalProperty))

    # directedBy
    g.add((directedBy, RDF.type, RDF.Property))
    g.add((directedBy, RDFS.domain, schema['Media']))
    g.add((directedBy, RDFS.range, schema['Person']))

    # duration
    g.add((duration, RDF.type, RDF.Property))
    g.add((duration, RDFS.domain, schema['Media']))
    g.add((duration, RDFS.range, XSD.string))

    # duration in Minutes
    g.add((durationInMin, RDF.type, RDF.Property))
    g.add((durationInMin, RDFS.domain, schema['Media']))
    g.add((durationInMin, RDFS.range, XSD.string))

    # listed_in (genre)
    g.add((hasGenre, RDF.type, RDF.Property))
    g.add((hasGenre, RDFS.domain, schema['Media']))
    g.add((hasGenre, RDFS.range, schema['Genre']))

    # producedIn (where was the media porduced)
    g.add((producedIn, RDF.type, RDF.Property))
    g.add((producedIn, RDFS.domain, schema['Media']))
    g.add((producedIn, RDFS.range, schema['Country']))

    # figuresIn (which actor figures in the media)
    g.add((figuresIn, RDF.type, RDF.Property))
    g.add((figuresIn, RDFS.domain, schema['Person']))
    g.add((figuresIn, RDFS.range, schema['Media']))

    # casting ( inverse of figuresIn)
    g.add((containsActorNamed, RDF.type, RDF.Property))
    g.add((containsActorNamed, OWL.inverseOf, figuresIn))
    g.add((containsActorNamed, RDFS.domain, schema['Media']))
    g.add((containsActorNamed, RDFS.range, schema['Person']))

    # age_limit
    g.add((ageLimitedTo, RDF.type, RDF.Property))
    g.add((ageLimitedTo, RDFS.domain, schema['Media']))
    g.add((ageLimitedTo, RDFS.range, schema['AgeLimit']))

    # description
    g.add((description, RDF.type, RDF.Property))
    g.add((description, RDFS.domain, schema['Media']))
    g.add((description, RDFS.range, XSD.string))

    # added_in
    g.add((addedOnNetflixIn, RDF.type, RDF.Property))
    g.add((addedOnNetflixIn, RDFS.domain, schema['Media']))
    g.add((addedOnNetflixIn, RDFS.range, XSD.date))

    # releaseYear
    g.add((releaseYear, RDF.type, RDF.Property))
    g.add((releaseYear, RDFS.domain, schema['Media']))
    g.add((releaseYear, RDFS.range, XSD.integer))

    # isAgeLimitationOf
    g.add((isAgeLimitationOf, RDF.type, RDF.Property))
    g.add((isAgeLimitationOf, OWL.inverseOf, ageLimitedTo))
    g.add((isAgeLimitationOf, RDFS.domain, schema['AgeLimit']))
    g.add((isAgeLimitationOf, RDFS.range, schema['Media']))

    # locationOf
    g.add((location_of, RDF.type, RDF.Property))
    g.add((location_of, OWL.inverseOf, producedIn))
    g.add((location_of, RDFS.domain, schema['Country']))
    g.add((location_of, RDFS.range, schema['Media']))

    # durartionOf
    g.add((durationOf, RDF.type, RDF.Property))
    g.add((durationOf, OWL.inverseOf, duration))
    g.add((durationOf, RDFS.domain, XSD.string))
    g.add((durationOf, RDFS.range, schema['Media']))

    # isGenreOf
    g.add((isGenreOf, RDF.type, RDF.Property))
    g.add((isGenreOf, OWL.inverseOf, hasGenre))
    g.add((isGenreOf, RDFS.domain, schema['Genre']))
    g.add((isGenreOf, RDFS.range, schema['Media']))

    # isDirectorOf
    g.add((isDirectorOf, RDF.type, RDF.Property))
    g.add((isDirectorOf, OWL.inverseOf, directedBy))
    g.add((isDirectorOf, RDFS.domain, schema['Person']))
    g.add((isDirectorOf, RDFS.range, schema['Media']))



def create_triples(df, g, schema):
    for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Creating triples"):
        titre = row['title']
        # media_uri
        media_uri = rdflib.URIRef(f"{schema}{row['type']}/{titre}")
        g.add((media_uri, RDF.type, schema['Media']))
        # title
        g.add((media_uri, RDFS.label, Literal(f"{split_camel_case(titre)}")))

        if row['type'] == "Movie":
            create_movie_triples(row, g, schema,titre)
        else:
            create_tv_show_triples(row, g, schema,titre)




def create_movie_triples(row, g, schema,titre):
    mediatype = row['type']
    # create a movie uri
    movie_uri = rdflib.URIRef(f"{schema}{mediatype}/{titre}")
    # Add the uri to the graph
    g.add((movie_uri, RDF.type, schema['Movie']))
    # We still add the media type as an rdfs:label with language tag "en" to use the full power of RDF GRapohs
    g.add((movie_uri, RDFS.label, Literal(f"{split_camel_case(titre)}", lang='en')))

    """----------------------Data properties---------------------------------"""

    # Date where the movie got added on Netflix
    g.add((movie_uri, schema['addedOnNetflixIn'], Literal(row['date_added'])))

    # id triplets
    g.add((movie_uri, schema['hasId'], Literal(row['show_id'])))

    # decription triplets
    g.add((movie_uri, schema['hasDescription'], Literal(row['description'].split(' '))))

    # release_year triplets
    g.add((movie_uri, schema['releasedIn'], Literal(int(row['release_year']))))

    # duration in minutes
    duree = row['duration']
    if "min" in row['duration']:
        literal_duration = Literal(int(duree.replace("min", "")))
        g.add((movie_uri, schema['hasDurationInMin'], literal_duration))
        # inverse
        g.add((literal_duration, schema['durationOf'], movie_uri))
    # duration with no minutes
    else:
        g.add((movie_uri, schema['hasDuration'], Literal(duree)))
        # inverse
        g.add((Literal(duree), schema['durationOf'], movie_uri))

        """----------------------Entities relationships---------------------------------"""

        # Add triplet for casting, director, and Genres, age limit
        # age limit triplets
        age_restriction = row['rating']
        # creating the uri and add it to the graph
        age_restriction_uri = rdflib.URIRef(f"{schema}{age_restriction}")
        g.add((age_restriction_uri, RDF.type, schema['Age_category']))
        # create a triplet
        g.add((movie_uri, schema['ageLimitedTo'], age_restriction_uri))
        g.add((age_restriction_uri, RDFS.label, Literal(row['rating'], lang='en')))
        # inverse
        g.add((age_restriction_uri, schema['isAgeLimitationFor'], movie_uri))

    # Actors
    for cast_member in row['cast'].split(','):
        # Person_uri creation
        person_uri = rdflib.URIRef(f"{schema}{cast_member}")
        # add uri to the graph
        g.add((person_uri, RDF.type, schema['Person']))
        # a Person has a Name
        g.add((person_uri, RDFS.label, Literal(f"{split_camel_case(cast_member)}", lang='en')))
        # Create URI for actors
        actors_uri = rdflib.URIRef(f"{schema}{cast_member}")
        # add the actors uri to the graph
        g.add((actors_uri, RDF.type, schema['Actor']))
        g.add((actors_uri, RDFS.label, Literal(f"{split_camel_case(cast_member)}", lang='en')))
        # construct the relationships : a media contains named people that work as actors
        g.add((movie_uri, schema['containsActorNamed'], person_uri))
        # inverse
        g.add((person_uri, schema['appearsIn'], movie_uri))

    for director in row['director'].split(','):
        # Person_uri creation
        person_uri = rdflib.URIRef(f"{schema}{director}")
        # add uri to the graph
        g.add((person_uri, RDF.type, schema['Person']))
        # a Person has a Name
        g.add((person_uri, RDFS.label, Literal(f"{split_camel_case(director)}", lang='en')))
        # Create URI for directors
        director_uri = rdflib.URIRef(f"{schema}{director}")
        # add the directors uri to the graph
        g.add((director_uri, RDF.type, schema['Director']))
        g.add((director_uri, RDFS.label, Literal(f"{split_camel_case(director)}", lang='en')))
        # construct the relationships : a media contains named people that work as directors
        g.add((movie_uri, schema['directedBy'], person_uri))
        # inverse
        g.add((person_uri, schema['isDirectorOf'], movie_uri))

    for genre in row['listed_in'].split(','):
        # Create URI for genre
        genre_uri = rdflib.URIRef(f"{schema}{genre}")
        g.add((genre_uri, RDF.type, schema['Genre']))
        g.add((movie_uri, schema['hasGenre'], genre_uri))
        g.add((genre_uri, RDFS.label, Literal(split_camel_case(genre), lang='en')))
        # inverse
        g.add((genre_uri, schema['isGenreOf'], movie_uri))

    for country in row['country'].split(','):
        country_uri = rdflib.URIRef(f"{schema}{country}")
        g.add((country_uri, RDF.type, schema['Country']))
        g.add((movie_uri, schema['producedIn'], country_uri))
        g.add((country_uri, RDFS.label, Literal(split_camel_case(country), lang='en')))
        # inverse
        g.add((country_uri, schema['isLocationOf'], movie_uri))


def create_tv_show_triples(row, g, schema,titre):
    mediatype = row['type']
    # create a movie uri
    tv_show_uri = rdflib.URIRef(f"{schema}{mediatype}/{titre}")
    # Add the uri to the graph
    g.add((tv_show_uri, RDF.type, schema['TV_show']))
    # We still add the media type as an rdfs:label with language tag "en" to use the full power of RDF GRapohs
    g.add((tv_show_uri, RDFS.label, Literal(f"{split_camel_case(titre)}", lang='en')))

    """----------------------Data properties---------------------------------"""

    # Date where the movie got added on Netflix
    g.add((tv_show_uri, schema['addedOnNetflixIn'], Literal(row['date_added'])))

    # id triplets
    g.add((tv_show_uri, schema['hasId'], Literal(row['show_id'])))

    # decription triplets
    g.add((tv_show_uri, schema['hasDescription'], Literal(row['description'].split(' '))))

    # release_year triplets
    g.add((tv_show_uri, schema['releasedIn'], Literal(int(row['release_year']))))

    # duration in minutes
    duree = row['duration']
    if "min" in row['duration']:
        literal_duration = Literal(int(duree.replace("min", "")))
        g.add((tv_show_uri, schema['hasdurationInMin'], literal_duration))
        # inverse
        g.add((literal_duration, schema['durationOf'], tv_show_uri))
    # duration with no minutes
    else:
        g.add((tv_show_uri, schema['hasduration'], Literal(duree)))
        # inverse
        g.add((Literal(duree), schema['durationOf'], tv_show_uri))

        """----------------------Entities relationships---------------------------------"""

        # Add triplet for casting, director, and Genres, age limit
        # age limit triplets
        age_restriction = row['rating']
        # creating the uri and add it to the graph
        age_restriction_uri = rdflib.URIRef(f"{schema}{age_restriction}")
        g.add((age_restriction_uri, RDF.type, schema['Age_category']))
        # create a triplet
        g.add((tv_show_uri, schema['ageLimitedTo'], age_restriction_uri))
        g.add((age_restriction_uri, RDFS.label, Literal(row['rating'], lang='en')))
        # inverse
        g.add((age_restriction_uri, schema['isAgeLimitationFor'], tv_show_uri))

    # Actors
    for cast_member in row['cast'].split(','):
        # Person_uri creation
        person_uri = rdflib.URIRef(f"{schema}{cast_member}")
        # add uri to the graph
        g.add((person_uri, RDF.type, schema['Person']))
        # a Person has a Name
        g.add((person_uri, RDFS.label, Literal(f"{split_camel_case(cast_member)}", lang='en')))
        # Create URI for actors
        actors_uri = rdflib.URIRef(f"{schema}{cast_member}")
        # add the actors uri to the graph
        g.add((actors_uri, RDF.type, schema['Actor']))
        g.add((actors_uri, RDFS.label, Literal(f"{split_camel_case(cast_member)}", lang='en')))
        # construct the relationships : a media contains named people that work as actors
        g.add((tv_show_uri, schema['containsActorNamed'], person_uri))
        # inverse
        g.add((person_uri, schema['appearsIn'], tv_show_uri))

    for director in row['director'].split(','):
        # Person_uri creation
        person_uri = rdflib.URIRef(f"{schema}{director}")
        # add uri to the graph
        g.add((person_uri, RDF.type, schema['Person']))
        # a Person has a Name
        g.add((person_uri, RDFS.label, Literal(f"{split_camel_case(director)}", lang='en')))
        # Create URI for directors
        director_uri = rdflib.URIRef(f"{schema}{director}")
        # add the directors uri to the graph
        g.add((director_uri, RDF.type, schema['Director']))
        g.add((director_uri, RDFS.label, Literal(f"{split_camel_case(director)}", lang='en')))
        # construct the relationships : a media contains named people that work as directors
        g.add((tv_show_uri, schema['directedBy'], person_uri))
        # inverse
        g.add((person_uri, schema['isDirectorOf'], tv_show_uri))

    for genre in row['listed_in'].split(','):
        # Create URI for genre
        genre_uri = rdflib.URIRef(f"{schema}{genre}")
        g.add((genre_uri, RDF.type, schema['Genre']))
        g.add((tv_show_uri, schema['hasGenre'], genre_uri))
        g.add((genre_uri, RDFS.label, Literal(split_camel_case(genre), lang='en')))
        # inverse
        g.add((genre_uri, schema['isGenreOf'], tv_show_uri))

    for country in row['country'].split(','):
        country_uri = rdflib.URIRef(f"{schema}{country}")
        g.add((country_uri, RDF.type, schema['Country']))
        g.add((tv_show_uri, schema['producedIn'], country_uri))
        g.add((country_uri, RDFS.label, Literal(split_camel_case(country), lang='en')))
        # inverse
        g.add((country_uri, schema['isLocationOf'], tv_show_uri))



def main():
    # Load and preprocess data
    csv_path = "netflix.csv"

    try:
        print("Serialization in progress")
        df = preprocess_data(csv_path)

        # Create RDF graph and bind namespaces
        g, schema = create_rdf_graph()

        # Add classes to the graph
        add_classes_to_graph(g, schema)

        # Add properties to the graph
        add_properties_to_graph(g, schema)

        # Create triples for movies and TV shows
        create_triples(df, g, schema)

        # Save RDF graph to a file
        rdf_path = "netflix.owl"
        g.serialize(destination=rdf_path, format="xml")
        print(f"RDF graph saved to {rdf_path}")
    except FileNotFoundError:
        print("Please try again with a valid path.")


if __name__ == "__main__":
    main()
