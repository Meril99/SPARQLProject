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
    df.cast =df.cast.str.replace(" ", "")
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
    Actors = schema['Actors']
    Country = schema['Country']
    Genre = schema['Genre']
    AgeLimit = schema['Age_category']
    Directeur = schema['Director']

    # Create classes
    #Media
    g.add((Media, RDF.type, RDFS.Class))

    #TV_Show
    g.add((TV_show, RDF.type, RDFS.Class))
    g.add((TV_show, RDFS.subClassOf, Media))

    #Movie
    g.add((Movie, RDF.type, RDFS.Class))
    g.add((Movie, RDFS.subClassOf, Media))

    #Person
    g.add((Person, RDF.type, RDFS.Class))

    #Actors
    g.add((Actors, RDF.type, RDFS.Class))
    g.add((Actors, RDFS.subClassOf, Person))

    #Directeur
    g.add((Directeur, RDF.type, RDFS.Class))
    g.add((Directeur, RDFS.subClassOf, Person))

    #Country
    g.add((Country, RDF.type, RDFS.Class))

    #Genre
    g.add((Genre, RDF.type, RDFS.Class))

    #Age_Limit
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
    durationInMin = schema['hasDuration_InMin']
    hasGenre = schema['hasGenre']
    description = schema['hasDescription']
    ageLimitedTo = schema['hasAge_categorization']
    name = schema['title']
    releaseYear = schema['releasedIn']
    #inverse of age_limit
    isAgeLimitationOf = schema['isAgeLimitationFor']
    #inverse of produced
    location_of = schema['isLocationOf']
    #inverseOfduration
    durationOf=schema['isDurationOf']
    #inverseOfGenre
    isGenreOf=schema['isGenreOf']
    #inverseOf directedBY
    isDirectorOf=schema['isDirectorOf']


    # create the properties and spoecify domain + range (id)
    #An id is unique, that's why it is a functional Property
    g.add(((hasId, RDF.type, RDF.Property)))
    g.add((hasId, RDFS.domain, Media))
    g.add((hasId, RDFS.range, XSD.string))
    g.add((hasId, RDF.type, OWL.FunctionalProperty))

    # name
    g.add((name, RDF.type, RDF.Property))
    g.add((name, RDFS.domain, Media))
    g.add((name, RDFS.range, XSD.string))

    # directedBy
    g.add((directedBy, RDF.type, RDF.Property))
    g.add((directedBy, RDFS.domain, Media))
    g.add((directedBy, RDFS.range, Directeur))

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
    g.add((figuresIn, RDFS.domain, Actors))
    g.add((figuresIn, RDFS.range, Media))

    # casting ( inverse of figuresIn)
    g.add((containsActorNamed, RDF.type, RDF.Property))
    g.add((containsActorNamed, OWL.inverseOf, figuresIn))
    g.add((containsActorNamed, RDFS.domain, Media))
    g.add((containsActorNamed, RDFS.range, Actors))

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

    #locationOf
    g.add((location_of, RDF.type, RDF.Property))
    g.add((location_of, OWL.inverseOf, producedIn))
    g.add((location_of, RDFS.domain, Country))
    g.add((isAgeLimitationOf, RDFS.range, Media))


    #durartionOf
    g.add((durationOf, RDF.type, RDF.Property))
    g.add((durationOf, OWL.inverseOf, duration))
    g.add((durationOf, RDFS.domain, XSD.string))
    g.add((durationOf, RDFS.range, Media))

    #isGenreOf
    g.add((isGenreOf, RDF.type, RDF.Property))
    g.add((isGenreOf, OWL.inverseOf, hasGenre))
    g.add((isGenreOf, RDFS.domain, Genre))
    g.add((isGenreOf, RDFS.range, Media))

    # isDirectorOf
    g.add((isDirectorOf, RDF.type, RDF.Property))
    g.add((isDirectorOf, OWL.inverseOf, directedBy))
    g.add((isDirectorOf, RDFS.domain, Directeur))
    g.add((isDirectorOf, RDFS.range, Media))

    """----------------------Triplets--------------------------------"""
    # Create triples for each row in dataframe
    for _, row in df.iterrows():

        titre=row['title']

        # media_uri
        media_uri = rdflib.URIRef(f"{schema}{titre}/{row['type']}")
        g.add((media_uri, RDF.type, Media))
	    #title
        g.add((media_uri, name, Literal(titre)))

        # If the media is a movie :
        if row['type'] == "Movie":

            mediatype = row['type']
            # create a movie uri
            movie_uri = rdflib.URIRef(f"{schema}{titre}/{mediatype}")
            g.add((movie_uri, name, Literal(titre)))

            # Add triplets
            g.add((movie_uri, RDF.type, Movie))

            # Date where the movie got added on Netflix
            g.add((movie_uri, addedOnNetflixIn, Literal(row['date_added'])))


            # age limit triplets
            age_restriction = row['rating']
            age_restriction_uri = rdflib.URIRef(f"{schema}{age_restriction}")
            g.add((age_restriction_uri, RDF.type, AgeLimit))
            g.add((movie_uri, ageLimitedTo, age_restriction_uri))
            g.add((movie_uri, ageLimitedTo, Literal(row['rating'])))
            #inverse
            g.add((age_restriction_uri, isAgeLimitationOf, movie_uri))
            g.add((age_restriction_uri, isAgeLimitationOf, Literal(row['title'])))

            # title triplets
            g.add((movie_uri, name, Literal(row['title'].replace('_', ''))))

            # id triplets
            g.add((movie_uri, hasId, Literal(row['show_id'])))

            # decription triplets
            g.add((movie_uri, description, Literal(row['description'].split(' '))))

            # release_year triplets
            g.add((movie_uri, releaseYear, Literal(row['release_year'])))

            # duration in minutes
            duree = row['duration'].replace(" ", "_")
            if "min" in row['duration']:
                literal_duration = Literal(int(duree.replace("min", "")))
                g.add((movie_uri, durationInMin, literal_duration))
                # inverse
                g.add((literal_duration, durationOf, movie_uri))
            #duration with no minutes
            else:
                literal_duration = Literal(duree.replace(" ", "_"))
                g.add((movie_uri, duration, literal_duration))
                # inverse
                g.add((literal_duration, durationOf, movie_uri))

            # Add triplet for casting, director, and Genres
            for cast_member in row['cast'].split(','):
                # Person_uri creation
                person_uri = rdflib.URIRef(f"{schema}{cast_member}")
                g.add((person_uri, RDF.type, Person))
                # Create URI for actors
                actors_uri = rdflib.URIRef(f"{schema}{cast_member}")
                # add tyhe triplets
                g.add((actors_uri, RDF.type, Actors))
                g.add((movie_uri, containsActorNamed, actors_uri))
                g.add((movie_uri, containsActorNamed, Literal(cast_member)))
                g.add((actors_uri, figuresIn, movie_uri))
                g.add((Literal(cast_member), figuresIn, media_uri))


            for director in row['director'].split(','):
                # Person_uri creation
                person_uri = rdflib.URIRef(f"{schema}{director}")
                g.add((person_uri, RDF.type, Person))
                # Create URI for directors
                dir_uri = rdflib.URIRef(f"{schema}{director}")
                g.add((dir_uri, RDF.type, Directeur))
                g.add((movie_uri, directedBy, dir_uri))
                g.add((movie_uri, directedBy, Literal(director)))
                #inverse
                g.add((dir_uri, isDirectorOf, movie_uri ))
                g.add((Literal(director), isDirectorOf, movie_uri ))





            for genre in row['listed_in'].split(','):
                # Create URI for genre
                genre_uri = rdflib.URIRef(f"{schema}{genre}")
                g.add((genre_uri, RDF.type, Genre))
                g.add((movie_uri, hasGenre, genre_uri))
                g.add((movie_uri, hasGenre, Literal(genre)))
                #inverse
                g.add((genre_uri, isGenreOf, movie_uri))
                g.add((Literal(genre), isGenreOf, movie_uri))


            for country in row['country'].split(','):
                country_uri = rdflib.URIRef(f"{schema}{country}")
                g.add((country_uri, RDF.type, Country))
                g.add((movie_uri, producedIn, country_uri))
                g.add((movie_uri, producedIn, Literal(country)))
                #inverse
                g.add((country_uri, location_of, movie_uri))
                g.add((Literal(country), location_of, movie_uri))


        # if the media is a tv-show
        else:

            tv_show_uri = rdflib.URIRef(f"{schema}{titre}/{row['type']}")
            g.add((tv_show_uri, name, Literal(titre)))

            # Add triplets
            g.add((tv_show_uri, RDF.type, TV_show))

            # Date where the tv-show got added on Netflix
            g.add((tv_show_uri, addedOnNetflixIn, Literal(row['date_added'])))

            # release year
            g.add((tv_show_uri, releaseYear, Literal(row['release_year'])))

            # age limit triplets
            age_restriction = row['rating']
            age_restriction_uri = rdflib.URIRef(f"{schema}{age_restriction}")
            g.add((age_restriction_uri, RDF.type, AgeLimit))
            g.add((tv_show_uri, ageLimitedTo, age_restriction_uri))
            g.add((tv_show_uri, ageLimitedTo, Literal(row['rating'])))

            # which other movies have this age limitation ?
            g.add((age_restriction_uri, isAgeLimitationOf, tv_show_uri))
            g.add((age_restriction_uri, isAgeLimitationOf, Literal(row['title'])))

            # title triplets
            g.add((tv_show_uri, name, Literal(row['title'].replace('_', ''))))

            # id triplets
            g.add((tv_show_uri, hasId, Literal(row['show_id'])))

            # descfription triplets
            g.add((tv_show_uri, description, Literal(row['description'].split(' '))))

            # duration
            duree = row['duration'].replace(" ", "_")
            if "min" in row['duration']:
                literal_duration = Literal(int(duree.replace("min", "")))
                g.add((tv_show_uri, durationInMin, literal_duration))
                # inverse
                g.add((literal_duration, durationOf, tv_show_uri))

            else:
                literal_duration = Literal(duree.replace(" ", "_"))
                g.add((tv_show_uri, duration, literal_duration))
                # inverse
                g.add((literal_duration, durationOf, tv_show_uri))

            # Add labels for casting, director, and Genres
            for cast_member in row['cast'].split(','):
                # Person_uri creation
                person_uri = rdflib.URIRef(f"{schema}{cast_member}")
                g.add((person_uri, RDF.type, Person))
                # Create URI for actors
                actors_uri = rdflib.URIRef(f"{schema}{cast_member}")
                g.add((actors_uri, RDF.type, Actors))
                g.add((tv_show_uri, containsActorNamed, actors_uri))
                g.add((tv_show_uri, containsActorNamed, Literal(cast_member)))
                #inverse
                g.add((actors_uri, figuresIn, tv_show_uri))
                g.add((Literal(cast_member), figuresIn, media_uri))


            for director in row['director'].split(','):
                # Person_uri creation
                person_uri = rdflib.URIRef(f"{schema}{director}")
                g.add((person_uri, RDF.type, Person))
                # Create URI for directors
                dir_uri = rdflib.URIRef(f"{schema}{director}")
                g.add((dir_uri, RDF.type, Directeur))
                g.add((tv_show_uri, directedBy, dir_uri))
                g.add((tv_show_uri, directedBy, Literal(director)))
                # inverse
                g.add((dir_uri, isDirectorOf, tv_show_uri))
                g.add((Literal(director), isDirectorOf, tv_show_uri))

            for genre in row['listed_in'].split(','):
                # Create URI for genre
                genre_uri = rdflib.URIRef(f"{schema}{genre}")
                g.add((genre_uri, RDF.type, Genre))
                g.add((tv_show_uri, hasGenre, genre_uri))
                g.add((tv_show_uri, hasGenre, Literal(genre)))
                # inverse
                g.add((genre_uri, isGenreOf, tv_show_uri))
                g.add((Literal(genre), isGenreOf, tv_show_uri))


            for country in row['country'].split(','):
                country_uri = rdflib.URIRef(f"{schema}{country}")
                g.add((country_uri, RDF.type, Country))
                g.add((tv_show_uri, producedIn, country_uri))
                g.add((tv_show_uri, producedIn, Literal(country)))
                #inverse
                g.add((country_uri, location_of, tv_show_uri))
                g.add((Literal(country), location_of, tv_show_uri))


    # Serialize RDF graph to file
    g.serialize(destination=rdf_file_name, format='xml')

    return g

chunk_size = 100  # Define the size of each chunk
df = pd.read_csv("netflix_titles.csv")
df_chunks = split_dataframe(df, chunk_size)


for i, chunk in enumerate(df_chunks):
    rdf_file_name = f"netflix_titles_transformer_update_part_{i + 1}.owl"
    csv_to_rdf(chunk, rdf_file_name)
