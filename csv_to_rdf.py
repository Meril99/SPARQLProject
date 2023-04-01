import os
import pandas as pd
import rdflib
from rdflib import Graph, Literal, Namespace, RDF, URIRef, RDFS
import re




# seperate a camalCased word
def split_camel_case(text):
    if text == "TV":
        return text
    else:
        return re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', text)).strip()


def create_triples(df, g, schema):
    for _, row in df.iterrows():
        titre = row['title']

        if row['type'] == "Movie":
            create_movie_triples(row, g, schema)
        else:
            create_tv_show_triples(row, g, schema)


def create_movie_triples(row, g, schema):
    # ... code for creating movie triples ...


def create_tv_show_triples(row, g, schema):
    # ... code for creating tv show triples ...


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


def main():
    csv_path = input("Please enter the path to your CSV file: ").strip()
    if not os.path.isfile(csv_path):
        print("The file path provided does not exist. Please check the path and try again.")
        return

    # Load the CSV file into a pandas dataframe and preprocess it
    df = preprocess_data(csv_path)

    """ """"""""""""""""""""""""""""""""""Prepreocessing"""""""""""""""""""""""""""""""""""""

    # split rows that contain multiple values
    df["cast"].str.split(",")
    df['listed_in'].str.split(",")
    df['country'].str.split(",")
    df['director'].str.split(",")

    # Fill blank rows
    df = df.fillna("Unknown")

    # Put everything in CamelCase and remove some punctioncharacters
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
    g.add((hasId, RDFS.domain, Media))
    g.add((hasId, RDFS.range, XSD.string))
    g.add((hasId, RDF.type, OWL.FunctionalProperty))

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


g = Graph()
    schema = Namespace("http://schema.org/")
    g.bind("schema", schema)

    create_triples(df, g, schema)

    # Save the graph as an RDF file
    g.serialize("output.rdf", format="xml")


if __name__ == "__main__":
    main()
import pandas as pd
import rdflib
import re

from rdflib import RDF, RDFS, OWL, XSD, Literal




