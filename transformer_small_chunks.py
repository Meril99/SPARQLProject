import pandas as pd
import rdflib
import re

from rdflib import RDF, RDFS, OWL, XSD, Literal




def split_dataframe(df, chunk_size):
    chunks = []
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i * chunk_size:(i + 1) * chunk_size])
    return chunks



def csv_to_rdf(df, rdf_file_name):

    """ """"""""""""""""""""""""""""""""""Prepreocessing"""""""""""""""""""""""""""""""""""""

    # split rows that contain multiple values
    df["cast"].str.split(",")
    df['listed_in'].str.split(",")
    df['country'].str.split(",")
    df['director'].str.split(",")

    # Fill blank rows
    df = df.fillna("Unknown")

    # Put everything in CamelCase and remove " "
    df.country = df.country.str.replace(" ", "")
    df.director = df.director.str.replace(" ", "")
    df.cast = df.cast.str.replace(" ", "")
    df.duration = df.duration.str.replace(" ", "")
    df['cast'] = df['cast'].apply(lambda actor: re.sub('\"[^\"]*\"', '', actor))
    df.listed_in = df.listed_in.str.replace(" ", "")
    df['title'] = df['title'].str.replace(' ', '').str.replace('\"', '')

    """ """"""""""""""""""""""""""""""""""RDF graph creation"""""""""""""""""""""""""""""""""""""

    # Create RDF graph
    g = rdflib.Graph()

    # Bind namespaces
    schema = rdflib.Namespace("http://example.org/")
    g.bind("ex", schema)
    g.bind('rdf', RDF)
    g.bind('rdfs', RDFS)

    """""""""""""""""""""""""""""""""Classes"""""""""""""""""""""""""""""""""""""""""""""""
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
    Job = schema['Job']

    # Create classes
    # Job
    g.add((Job, RDF.type, RDFS.Class))

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
    g.add((Actor, RDFS.subClassOf, Job))

    # Directeur
    g.add((Director, RDF.type, RDFS.Class))
    g.add((Director, RDFS.subClassOf, Job))

    # Country
    g.add((Country, RDF.type, RDFS.Class))

    # Genre
    g.add((Genre, RDF.type, RDFS.Class))

    # Age_Limit
    g.add((AgeLimit, RDF.type, RDFS.Class))

    """""""""""""""""""""""""""""""Properties"""""""""""""""""""""""""""""""""""""""""""

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
    title = schema['title']
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
    jobTitle = schema['jobTitle']
    isJobTitleOf = schema['isJobTitleOf']

    # create the properties and spoecify domain + range (id)
    # An id is unique, that's why it is a functional Property
    g.add(((hasId, RDF.type, RDF.Property)))
    g.add((hasId, RDFS.domain, Media))
    g.add((hasId, RDFS.range, XSD.string))
    g.add((hasId, RDF.type, OWL.FunctionalProperty))

    # name
    g.add((title, RDF.type, RDF.Property))
    g.add((title, RDFS.domain, Media))
    g.add((title, RDFS.range, XSD.string))

    # directedBy
    g.add((directedBy, RDF.type, RDF.Property))
    g.add((directedBy, RDFS.domain, Media))
    g.add((directedBy, RDFS.range, Person))

    # duration
    g.add((duration, RDF.type, RDF.Property))
    g.add((duration, RDFS.domain, Media))
    g.add((duration, RDFS.range, XSD.string))

    # duration in Minutes
    g.add((durationInMin, RDF.type, RDF.Property))
    g.add((durationInMin, RDFS.domain, Media))
    g.add((durationInMin, RDFS.range, XSD.string))

    # listed_in (genre)
    g.add((hasGenre, RDF.type, RDF.Property))
    g.add((hasGenre, RDFS.domain, Media))
    g.add((hasGenre, RDFS.range, Genre))

    # producedIn (where was the media porduced)
    g.add((producedIn, RDF.type, RDF.Property))
    g.add((producedIn, RDFS.domain, Media))
    g.add((producedIn, RDFS.range, Country))

    # figuresIn (which actor figures in the media)
    g.add((figuresIn, RDF.type, RDF.Property))
    g.add((figuresIn, RDFS.domain, Person))
    g.add((figuresIn, RDFS.range, Media))

    # casting ( inverse of figuresIn)
    g.add((containsActorNamed, RDF.type, RDF.Property))
    g.add((containsActorNamed, OWL.inverseOf, figuresIn))
    g.add((containsActorNamed, RDFS.domain, Media))
    g.add((containsActorNamed, RDFS.range, Person))

    # age_limit
    g.add((ageLimitedTo, RDF.type, RDF.Property))
    g.add((ageLimitedTo, RDFS.domain, Media))
    g.add((ageLimitedTo, RDFS.range, AgeLimit))

    # description
    g.add((description, RDF.type, RDF.Property))
    g.add((description, RDFS.domain, Media))
    g.add((description, RDFS.range, XSD.string))

    # added_in
    g.add((addedOnNetflixIn, RDF.type, RDF.Property))
    g.add((addedOnNetflixIn, RDFS.domain, Media))
    g.add((addedOnNetflixIn, RDFS.range, XSD.date))

    # releaseYear
    g.add((releaseYear, RDF.type, RDF.Property))
    g.add((releaseYear, RDFS.domain, Media))
    g.add((releaseYear, RDFS.range, XSD.integer))

    # isAgeLimitationOf
    g.add((isAgeLimitationOf, RDF.type, RDF.Property))
    g.add((isAgeLimitationOf, OWL.inverseOf, ageLimitedTo))
    g.add((isAgeLimitationOf, RDFS.domain, AgeLimit))
    g.add((isAgeLimitationOf, RDFS.range, Media))

    # locationOf
    g.add((location_of, RDF.type, RDF.Property))
    g.add((location_of, OWL.inverseOf, producedIn))
    g.add((location_of, RDFS.domain, Country))
    g.add((location_of, RDFS.range, Media))

    # durartionOf
    g.add((durationOf, RDF.type, RDF.Property))
    g.add((durationOf, OWL.inverseOf, duration))
    g.add((durationOf, RDFS.domain, XSD.string))
    g.add((durationOf, RDFS.range, Media))

    # isGenreOf
    g.add((isGenreOf, RDF.type, RDF.Property))
    g.add((isGenreOf, OWL.inverseOf, hasGenre))
    g.add((isGenreOf, RDFS.domain, Genre))
    g.add((isGenreOf, RDFS.range, Media))

    # isDirectorOf
    g.add((isDirectorOf, RDF.type, RDF.Property))
    g.add((isDirectorOf, OWL.inverseOf, directedBy))
    g.add((isDirectorOf, RDFS.domain, Person))
    g.add((isDirectorOf, RDFS.range, Media))

    # jobTitle
    g.add((jobTitle, RDF.type, RDF.Property))
    g.add((jobTitle, RDFS.domain, Person))
    g.add((jobTitle, RDFS.range, Job))
    g.add((jobTitle, RDFS.range, Director))
    g.add((jobTitle, RDFS.range, Actor))

    # isJobTitleOf
    g.add((isJobTitleOf, RDF.type, RDF.Property))
    g.add((isJobTitleOf, OWL.inverseOf, jobTitle))
    g.add((isJobTitleOf, RDFS.domain, Director))
    g.add((isJobTitleOf, RDFS.domain, Actor))
    g.add((jobTitle, RDFS.domain, Job))
    g.add((isJobTitleOf, RDFS.range, Person))

    """----------------------Triplets--------------------------------"""
    # Create triples for each row in dataframe
    for _, row in df.iterrows():

        titre = row['title']

        # media_uri
        media_uri = rdflib.URIRef(f"{schema}{titre}/{row['type']}")
        g.add((media_uri, RDF.type, Media))
        # title
        g.add((media_uri, title, Literal(titre)))

        # If the media is a movie :
        if row['type'] == "Movie":

            mediatype = row['type']
            # create a movie uri
            movie_uri = rdflib.URIRef(f"{schema}{titre}/{mediatype}")
            # Add the uri to the graph
            g.add((movie_uri, RDF.type, Movie))
            # We still add the media type as an rdfs:label with language tag "en" to use the full power of RDF GRapohs
            g.add((movie_uri, RDFS.label, Literal(titre, lang='en')))

            """----------------------Data properties---------------------------------"""

            # Date where the movie got added on Netflix
            g.add((movie_uri, addedOnNetflixIn, Literal(row['date_added'])))

            # this will allow us to display clean answers to our requests but is not necessary since we got a labeled movie_uri
            g.add((movie_uri, title, Literal(titre)))

            # id triplets
            g.add((movie_uri, hasId, Literal(row['show_id'])))

            # decription triplets
            g.add((movie_uri, description, Literal(row['description'].split(' '))))

            # release_year triplets
            g.add((movie_uri, releaseYear, Literal(row['release_year'])))

            # duration in minutes
            duree = row['duration']
            if "min" in row['duration']:
                literal_duration = Literal(int(duree.replace("min", "")))
                g.add((movie_uri, durationInMin, literal_duration))
                # inverse
                g.add((literal_duration, durationOf, movie_uri))
            # duration with no minutes
            else:
                g.add((movie_uri, duration, duree))
                # inverse
                g.add((duree, durationOf, movie_uri))

                """----------------------Entities relationships---------------------------------"""

                # Add triplet for casting, director, and Genres, age limit
                # age limit triplets
                age_restriction = row['rating']
                # creating the uri and add it to the graph
                age_restriction_uri = rdflib.URIRef(f"{schema}{age_restriction}")
                g.add((age_restriction_uri, RDF.type, AgeLimit))
                # create a triplet
                g.add((movie_uri, ageLimitedTo, age_restriction_uri))
                g.add((age_restriction_uri, RDFS.label, Literal(row['rating'], lang='en')))
                # inverse
                g.add((age_restriction_uri, isAgeLimitationOf, movie_uri))

            # Actors
            for cast_member in row['cast'].split(','):
                # Person_uri creation
                person_uri = rdflib.URIRef(f"{schema}{cast_member}")
                # add uri to the graph
                g.add((person_uri, RDF.type, Person))
                # a Person has a Name
                g.add((person_uri, RDFS.label, Literal(cast_member, lang='en')))
                # Create URI for actors
                actors_uri = rdflib.URIRef(f"{schema}{cast_member}")
                # add the actors uri to the graph
                g.add((actors_uri, RDF.type, Actor))
                g.add((actors_uri, RDFS.label, Literal("Actor", lang='en')))
                # construct the relationships : a media contains named people that work as actors
                g.add((movie_uri, containsActorNamed, person_uri))
                # inverse
                g.add((person_uri, figuresIn, movie_uri))
                # second relationship: a person works as an actor
                g.add((person_uri, jobTitle, actors_uri))
                # inverse
                g.add((actors_uri, isJobTitleOf, person_uri))

            for director in row['director'].split(','):
                # Person_uri creation
                person_uri = rdflib.URIRef(f"{schema}{director}")
                # add uri to the graph
                g.add((person_uri, RDF.type, Person))
                # a Person has a Name
                g.add((person_uri, RDFS.label, Literal(director, lang='en')))
                # Create URI for directors
                director_uri = rdflib.URIRef(f"{schema}{director}")
                # add the directors uri to the graph
                g.add((director_uri, RDF.type, Director))
                g.add((director_uri, RDFS.label, Literal("Director", lang='en')))
                # construct the relationships : a media contains named people that work as directors
                g.add((movie_uri, directedBy, person_uri))
                # inverse
                g.add((person_uri, isDirectorOf, movie_uri))
                # second relationship: a person works as an actor
                g.add((person_uri, jobTitle, director_uri))
                # inverse
                g.add((director_uri, isJobTitleOf, person_uri))

            for genre in row['listed_in'].split(','):
                # Create URI for genre
                genre_uri = rdflib.URIRef(f"{schema}{genre}")
                g.add((genre_uri, RDF.type, Genre))
                g.add((movie_uri, hasGenre, genre_uri))
                g.add((genre_uri, RDFS.label, Literal(genre, lang='en')))
                # inverse
                g.add((genre_uri, isGenreOf, movie_uri))

            for country in row['country'].split(','):
                country_uri = rdflib.URIRef(f"{schema}{country}")
                g.add((country_uri, RDF.type, Country))
                g.add((movie_uri, producedIn, country_uri))
                g.add((country_uri, RDFS.label, Literal(country, lang='en')))
                # inverse
                g.add((country_uri, location_of, movie_uri))


        # if the media is a tv-show
        else:

            # create a movie uri
            tv_show_uri = rdflib.URIRef(f"{schema}{titre}/{row['type']}")
            # Add the uri to the graph
            g.add((tv_show_uri, RDF.type, TV_show))
            # We still add the media type as an rdfs:label with language tag "en" to use the full power of RDF GRapohs
            g.add((tv_show_uri, RDFS.label, Literal(titre, lang='en')))

            """----------------------------Data properties----------------------------"""

            # Date where the tv-show got added on Netflix
            g.add((tv_show_uri, addedOnNetflixIn, Literal(row['date_added'])))

            # release year
            g.add((tv_show_uri, releaseYear, Literal(row['release_year'])))

            # title triplets
            g.add((tv_show_uri, title, Literal(row['title'])))

            # id triplets
            g.add((tv_show_uri, hasId, Literal(row['show_id'])))

            # descfription triplets
            g.add((tv_show_uri, description, Literal(row['description'].split(' '))))

            # duration
            duree = row['duration']
            if "min" in row['duration']:
                literal_duration = Literal(int(duree.replace("min", "")))
                g.add((tv_show_uri, durationInMin, literal_duration))
                # inverse
                g.add((literal_duration, durationOf, tv_show_uri))

            else:
                g.add((tv_show_uri, duration, Literal(duree)))
                # inverse
                g.add((Literal(duree), durationOf, tv_show_uri))

                # Add labels for casting, director, and Genres, age limit

                # age limit triplets
                age_restriction = row['rating']
                age_restriction_uri = rdflib.URIRef(f"{schema}{age_restriction}")
                g.add((age_restriction_uri, RDF.type, AgeLimit))
                g.add((tv_show_uri, ageLimitedTo, age_restriction_uri))
                g.add((age_restriction_uri, RDFS.label, Literal(row['rating'], lang='en')))
                # inverse
                g.add((age_restriction_uri, isAgeLimitationOf, tv_show_uri))

                # Actors
                for cast_member in row['cast'].split(','):
                    # Person_uri creation
                    person_uri = rdflib.URIRef(f"{schema}{cast_member}")
                    # add uri to the graph
                    g.add((person_uri, RDF.type, Person))
                    # a Person has a Name
                    g.add((person_uri, RDFS.label, Literal(cast_member, lang='en')))
                    # Create URI for actors
                    actors_uri = rdflib.URIRef(f"{schema}{cast_member}")
                    # add the actors uri to the graph
                    g.add((actors_uri, RDF.type, Actor))
                    g.add((actors_uri, RDFS.label, Literal("Actor", lang='en')))
                    # construct the relationships : a media contains named people that work as actors
                    g.add((tv_show_uri, containsActorNamed, person_uri))
                    # inverse
                    g.add((person_uri, figuresIn, tv_show_uri))
                    # second relationship: a person works as an actor
                    g.add((person_uri, jobTitle, actors_uri))
                    # inverse
                    g.add((actors_uri, isJobTitleOf, person_uri))

                for director in row['director'].split(','):
                    # Person_uri creation
                    person_uri = rdflib.URIRef(f"{schema}{director}")
                    # add uri to the graph
                    g.add((person_uri, RDF.type, Person))
                    # a Person has a Name
                    g.add((person_uri, RDFS.label, Literal(director, lang='en')))
                    # Create URI for directors
                    director_uri = rdflib.URIRef(f"{schema}{director}")
                    # add the directors uri to the graph
                    g.add((director_uri, RDF.type, Director))
                    g.add((director_uri, RDFS.label, Literal("Director", lang='en')))
                    # construct the relationships : a media contains named people that work as directors
                    g.add((tv_show_uri, directedBy, person_uri))
                    # inverse
                    g.add((person_uri, isDirectorOf, tv_show_uri))
                    # second relationship: a person works as an actor
                    g.add((person_uri, jobTitle, director_uri))
                    # inverse
                    g.add((director_uri, isJobTitleOf, person_uri))

                for genre in row['listed_in'].split(','):
                    # Create URI for genre
                    genre_uri = rdflib.URIRef(f"{schema}{genre}")
                    g.add((genre_uri, RDF.type, Genre))
                    g.add((tv_show_uri, hasGenre, genre_uri))
                    g.add((genre_uri, RDFS.label, Literal(genre, lang='en')))
                    # inverse
                    g.add((genre_uri, isGenreOf, tv_show_uri))

                for country in row['country'].split(','):
                    country_uri = rdflib.URIRef(f"{schema}{country}")
                    g.add((country_uri, RDF.type, Country))
                    g.add((tv_show_uri, producedIn, country_uri))
                    g.add((country_uri, RDFS.label, Literal(country, lang='en')))
                    # inverse
                    g.add((country_uri, location_of, tv_show_uri))
    # Serialize RDF graph to file
    g.serialize(destination=rdf_file_name, format='xml')

    return g

chunk_size = 100  # Define the size of each chunk
df = pd.read_csv("netflix_titles.csv")
df_chunks = split_dataframe(df, chunk_size)


for i, chunk in enumerate(df_chunks):
    rdf_file_name = f"netflix_titles_transformer_update_part_{i + 1}.owl"
    csv_to_rdf(chunk, rdf_file_name)
