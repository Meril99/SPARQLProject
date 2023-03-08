import pandas as pd
import rdflib
import re

from rdflib import RDF, RDFS, OWL


def csv_to_rdf(csv_path, rdf_file_name):
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv(csv_path)

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
    Person = schema['Person']
    Actors = schema['Actors']
    Country = schema['Country']
    Date = schema['Date']
    Genre = schema['Genre']
    Pegi = schema['Age_restriction']
    ID = schema['ID']
    Description = schema['Description']




    # Create classes
    g.add((Media, RDF.type, RDFS.Class))
    g.add((Person, RDF.type, RDFS.Class))
    g.add((Actors, RDF.type, RDFS.Class))
    g.add((Actors, RDFS.subClassOf, Person))
    g.add((Country, RDF.type, RDFS.Class))
    g.add((Date, RDF.type, RDFS.Class))
    g.add((Genre, RDF.type, RDFS.Class))
    g.add((Pegi, RDF.type, RDFS.Class))
    g.add((ID, RDF.type, RDFS.Class))
    g.add((Description, RDF.type, RDFS.Class))





    # properties namespaces
    id = schema['hasId']
    directedBy = schema['directedBy']
    casting = schema['casting']
    figuresIn = schema['figuresIn']
    produced = schema['producedIn']
    added_in = schema['added_in']
    duration = schema['hasDuration']
    listed_in = schema['listed_in']
    desc = schema['hasDescription']
    age_limit=schema['hasAge_categorization']
    name=schema['hasName']



    #create the properties
    g.add(((id,RDF.type, RDF.Property)))
    g.add((schema.name, RDF.type, RDF.Property))
    g.add((directedBy, RDF.type, RDF.Property))
    g.add((casting, RDF.type, RDF.Property))
    g.add((listed_in, RDF.type, RDF.Property))
    g.add((produced, RDF.type, RDF.Property))
    g.add((figuresIn, RDF.type, RDF.Property))
    g.add((casting, OWL.inverseOf, figuresIn))
    g.add((age_limit,RDF.type,RDF.Property))
    g.add((name, RDF.type,RDF.Property))

    # Create triples for each row in dataframe
    for _, row in df.iterrows():
        # Create URI for media
        media_uri = rdflib.URIRef(f"{schema}{row['type']}/{row['show_id']}")


        # Add properties for media
        g.add((media_uri, id, ID))
        g.add((media_uri, id, rdflib.Literal(row['show_id'])))
        g.add((media_uri, RDF.type, Media))
        g.add((media_uri, name, rdflib.Literal(row['title'])))
        g.add((media_uri, desc, rdflib.Literal(row['description'])))
        g.add((media_uri, added_in, Date))
        g.add((media_uri, added_in, rdflib.Literal(row['release_year'])))
        g.add((media_uri, duration, rdflib.Literal(row['duration'])))
        #g.add((media_uri, listed_in, rdflib.Literal(row['listed_in'])))

        g.add((media_uri, age_limit, Pegi))
        g.add((media_uri,age_limit, rdflib.Literal(row['rating'])))

        # add metadata for media
        #g.add((media_uri, RDF.type, Media))


        # Add labels for casting, director, and Genres
        for cast_member in row['cast'].split(','):
            cast_member1 = cast_member.replace("_", " ")
            cast_member2 = cast_member1.replace(" ", "", 1)
            g.add((media_uri, casting, Actors))
            g.add((media_uri, casting, rdflib.Literal(cast_member2)))
            g.add((Actors, figuresIn, Media))
            g.add((rdflib.Literal(cast_member2), figuresIn, media_uri))

        for director in row['director'].split(','):
            dir1 = director.replace("_", " ")
            dir2 = dir1.replace(" ", "", 1)
            g.add((media_uri, directedBy, Person))
            g.add((media_uri, directedBy, rdflib.Literal(dir2)))

        for genre in row['listed_in'].split(','):
            genre1=genre.replace("_"," ")
            genre2=genre1.replace(" ","",1)
            g.add((media_uri, listed_in, Genre))
            g.add((media_uri, listed_in, rdflib.Literal(genre2)))

        for country in row['country'].split(','):
            c1=country.replace("_"," ")
            c2=c1.replace(" ","",1)
            g.add((media_uri, produced, Country))
            g.add((media_uri, produced, rdflib.Literal(c2)))


    # Serialize RDF graph to file
    g.serialize(destination=rdf_file_name, format='turtle')

    return g
csv_to_rdf("netflix_titles.csv", "netflix_titles.ttl")
