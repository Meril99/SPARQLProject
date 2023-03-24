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
    # Your existing code here, but without the line that reads the CSV file
    # some preprocessing if needed
    df["cast"].str.split(",")
    df['listed_in'].str.split(",")
    df['country'].str.split(",")
    df['director'].str.split(",")

    df = df.fillna("Unknown")
    df.country = [label.replace(" ", "_") for label in df['country']]
    df.director = [label.replace(" ", "_") for label in df['director']]
    df.cast = [label.replace(" ", "_") for label in df['cast']]
    df.cast = [re.sub('\"[^\"]*\"', '_', label) for label in df['cast']]

    df.listed_in = [label.replace(" ", "_") for label in df['listed_in']]

    # Create RDF graph
    g = rdflib.Graph()

    # Bind namespaces
    schema = rdflib.Namespace("http://example.org/")

    g.bind("ex", schema)
    g.bind('rdf', RDF)
    g.bind('rdfs', RDFS)

    # Define classes  namespaces
    Media = schema['Media']
    TV_show = schema['TV_show']
    Movie = schema['Movie']
    Person = schema['Person']
    Actors = schema['Actors']
    Country = schema['Country']
    Genre = schema['Genre']
    Pegi = schema['Age_category']
    Directeur = schema['Director']
    Date = schema['Date']

    # Create classes
    g.add((Media, RDF.type, RDFS.Class))

    g.add((TV_show, RDF.type, RDFS.Class))
    g.add((TV_show, RDFS.subClassOf, Media))

    g.add((Movie, RDF.type, RDFS.Class))
    g.add((Movie, RDFS.subClassOf, Media))

    g.add((Person, RDF.type, RDFS.Class))

    g.add((Actors, RDF.type, RDFS.Class))
    g.add((Actors, RDFS.subClassOf, Person))

    g.add((Directeur, RDF.type, RDFS.Class))
    g.add((Directeur, RDFS.subClassOf, Person))

    g.add((Country, RDF.type, RDFS.Class))

    g.add((Genre, RDF.type, RDFS.Class))

    g.add((Pegi, RDF.type, RDFS.Class))

    g.add((Date, RDF.type, RDFS.Class))

    # properties namespaces
    id = schema['hasId']
    directedBy = schema['directedBy']
    casting = schema['casting']
    figuresIn = schema['figuresIn']
    produced = schema['producedIn']
    added_in = schema['added_in']
    duration = schema['hasDuration']
    durationInMin = schema['hasDurationInMin']
    listed_in = schema['listed_in']
    desc = schema['hasDescription']
    age_limit = schema['hasAge_categorization']
    name = schema['title']
    releaseYear = schema['releasedIn']
    occursin = schema['occursIn']

    # create the properties and spoecify domain + range (id)
    g.add(((id, RDF.type, RDF.Property)))
    g.add((id, RDFS.domain, Media))
    g.add((id, RDFS.range, XSD.string))

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

    # listed_in
    g.add((listed_in, RDF.type, RDF.Property))
    g.add((listed_in, RDFS.domain, Media))
    g.add((listed_in, RDFS.range, Genre))

    # produced
    g.add((produced, RDF.type, RDF.Property))
    g.add((produced, RDFS.domain, Media))
    g.add((produced, RDFS.range, Country))

    # figuresIn
    g.add((figuresIn, RDF.type, RDF.Property))
    g.add((figuresIn, RDFS.domain, Actors))
    g.add((figuresIn, RDFS.range, Media))

    # casting
    g.add((casting, RDF.type, RDF.Property))
    g.add((casting, OWL.inverseOf, figuresIn))
    g.add((casting, RDFS.domain, Media))
    g.add((casting, RDFS.range, Actors))

    # age_limit
    g.add((age_limit, RDF.type, RDF.Property))
    g.add((age_limit, RDFS.domain, Media))
    g.add((age_limit, RDFS.range, Pegi))

    # description
    g.add((desc, RDF.type, RDF.Property))
    g.add((desc, RDFS.domain, Media))
    g.add((desc, RDFS.range, XSD.string))

    # added_in
    g.add((added_in, RDF.type, RDF.Property))
    g.add((added_in, RDFS.domain, Media))
    g.add((added_in, RDFS.range, Date))

    # releaseYear
    g.add((releaseYear, RDF.type, RDF.Property))
    g.add((releaseYear, RDFS.domain, Media))
    g.add((releaseYear, RDFS.range, XSD.integer))

    # occursIn
    g.add((occursin, RDF.type, RDF.Property))
    g.add((occursin, RDFS.domain, Pegi))
    g.add((occursin, RDFS.range, Media))

    # Create triples for each row in dataframe
    for _, row in df.iterrows():
        titre = row['title'].replace(' ', '')
        titre2 = titre.replace('\"', '')

        # media_uri
        media_uri = rdflib.URIRef(f"{schema}{titre2}/{row['type']}")
        g.add((media_uri, RDF.type, Media))

        # Date_uri
        date_uri = rdflib.URIRef(f"{schema}{titre2}/{row['date_added'].replace(' ', '_')}")
        g.add((date_uri, RDF.type, Date))

        # If the media is a movie :
        if row['type'] == "Movie":
            mediatype = row['type']

            # create a movie uri
            movie_uri = rdflib.URIRef(f"{schema}{titre2}/{mediatype}")

            # Add triplets
            g.add((movie_uri, RDF.type, Movie))

            # Date where the movie got added on Netflix
            g.add((movie_uri, added_in, date_uri))
            g.add((movie_uri, added_in, Literal(row['date_added'].replace(' ','_'))))



            # age limit triplets
            age_restriction = row['rating']
            age_restriction_uri = rdflib.URIRef(f"{schema}{age_restriction}")
            g.add((age_restriction_uri, RDF.type, Pegi))
            g.add((movie_uri, age_limit, age_restriction_uri))
            g.add((movie_uri, age_limit, Literal(row['rating'])))

            #which other movies have this age limitation ?
            g.add((age_restriction_uri, occursin, movie_uri))
            g.add((age_restriction_uri, occursin, Literal(row['title'])))



            # title triplets
            g.add((movie_uri, name, Literal(row['title'].replace('_', ''))))

            # id triplets
            g.add((movie_uri, id, Literal(row['show_id'])))

            # decription triplets
            g.add((movie_uri, desc, Literal(row['description'].split(' '))))

            # release_year triplets
            g.add((movie_uri, releaseYear, Literal(row['release_year'])))

            # duration
            duree = row['duration'].replace(" ", "_")
            if "min" in row['duration']:
                g.add((movie_uri, durationInMin, Literal(int(duree.replace("min", "")))))
            else:
                g.add((movie_uri, duration, Literal(duree.replace(" ", "_"))))

            # Add triplet for casting, director, and Genres

            for cast_member in row['cast'].split(','):
                # Create URI for actors
                cast_member1 = cast_member.replace("_", "")
                cast_member2 = cast_member1.replace(" ", "")
                actors_uri = rdflib.URIRef(f"{schema}{cast_member}")
                # add tyhe triplets
                g.add((actors_uri, RDF.type, Actors))
                g.add((movie_uri, casting, actors_uri))
                g.add((movie_uri, casting, Literal(cast_member2)))
                g.add((actors_uri, figuresIn, movie_uri))
                g.add((Literal(cast_member2), figuresIn, media_uri))

            for director in row['director'].split(','):
                # Create URI for directors
                dir1 = director.replace("_", "")
                dir2 = dir1.replace(" ", "")
                dir_uri = rdflib.URIRef(f"{schema}{director}")
                g.add((dir_uri, RDF.type, Directeur))
                g.add((movie_uri, directedBy, dir_uri))
                g.add((movie_uri, directedBy, Literal(dir2)))

            for genre in row['listed_in'].split(','):
                # Create URI for genre
                genre1 = genre.replace("_", "")
                genre2 = genre1.replace(" ", "")
                genre_uri = rdflib.URIRef(f"{schema}{genre}")
                g.add((genre_uri, RDF.type, Genre))
                g.add((movie_uri, listed_in, genre_uri))
                g.add((movie_uri, listed_in, Literal(genre2)))

            for country in row['country'].split(','):
                c1 = country.replace("_", "")
                c2 = c1.replace(" ", "")
                country_uri = rdflib.URIRef(f"{schema}{country}")
                g.add((country_uri, RDF.type, Country))
                g.add((movie_uri, produced, country_uri))
                g.add((movie_uri, produced, Literal(c2)))

        # if the mdia is a tv-show
        else:
            tv_show_uri = rdflib.URIRef(f"{schema}{titre2}/{row['type']}")
            # Add triplets
            g.add((tv_show_uri, RDF.type, TV_show))

            # Date where the movie got added on Netflix
            g.add((tv_show_uri, added_in, date_uri))
            g.add((tv_show_uri, added_in, Literal(row['date_added'].replace(' ', '_'))))

            # release year
            g.add((tv_show_uri, releaseYear, Literal(row['release_year'])))

            # age limit triplets
            age_restriction = row['rating']
            age_restriction_uri = rdflib.URIRef(f"{schema}{age_restriction}")
            g.add((age_restriction_uri, RDF.type, Pegi))
            g.add((tv_show_uri, age_limit, age_restriction_uri))
            g.add((tv_show_uri, age_limit, Literal(row['rating'])))

            # which other movies have this age limitation ?
            g.add((age_restriction_uri, occursin, tv_show_uri))
            g.add((age_restriction_uri, occursin, Literal(row['title'])))

            # title triplets
            g.add((tv_show_uri, name, Literal(row['title'].replace('_', ''))))

            # id triplets
            g.add((tv_show_uri, id, Literal(row['show_id'])))

            # descfription triplets
            g.add((tv_show_uri, desc, Literal(row['description'].split(' '))))

            # duration
            duree = row['duration'].replace(" ", "_")
            if "min" in row['duration']:
                g.add((tv_show_uri, durationInMin, Literal(int(duree.replace("min", "")))))
            else:
                g.add((tv_show_uri, duration, Literal(duree.replace(" ", "_"))))

            # Add labels for casting, director, and Genres
            for cast_member in row['cast'].split(','):
                # Create URI for actors
                cast_member1 = cast_member.replace("_", "")
                cast_member2 = cast_member1.replace(" ", "")
                actors_uri = rdflib.URIRef(f"{schema}{cast_member}")
                g.add((actors_uri, RDF.type, Actors))

                g.add((tv_show_uri, casting, actors_uri))
                g.add((tv_show_uri, casting, Literal(cast_member2)))
                g.add((actors_uri, figuresIn, tv_show_uri))
                g.add((Literal(cast_member2), figuresIn, media_uri))

            for director in row['director'].split(','):
                # Create URI for directors
                dir1 = director.replace("_", "")
                dir2 = dir1.replace(" ", "")
                dir_uri = rdflib.URIRef(f"{schema}{director}")
                g.add((dir_uri, RDF.type, Directeur))

                g.add((tv_show_uri, directedBy, dir_uri))
                g.add((tv_show_uri, directedBy, Literal(dir2)))

            for genre in row['listed_in'].split(','):
                # Create URI for genre
                genre1 = genre.replace("_", "")
                genre2 = genre1.replace(" ", "")
                genre_uri = rdflib.URIRef(f"{schema}{genre}")
                g.add((genre_uri, RDF.type, Genre))
                g.add((tv_show_uri, listed_in, genre_uri))
                g.add((tv_show_uri, listed_in, Literal(genre2)))

            for country in row['country'].split(','):
                c1 = country.replace("_", "")
                c2 = c1.replace(" ", "")
                country_uri = rdflib.URIRef(f"{schema}{country}")
                g.add((country_uri, RDF.type, Country))

                g.add((tv_show_uri, produced, country_uri))
                g.add((tv_show_uri, produced, Literal(c2)))

    # Serialize RDF graph to file
    g.serialize(destination=rdf_file_name, format='xml')

    return g

chunk_size = 100  # Define the size of each chunk
df = pd.read_csv("netflix_titles.csv")
df_chunks = split_dataframe(df, chunk_size)


for i, chunk in enumerate(df_chunks):
    rdf_file_name = f"netflix_titles_transformer_update_part_{i + 1}.owl"
    csv_to_rdf(chunk, rdf_file_name)
