@MIANGOUILA Méril Emmanuel
@MURIE Zoe

------------------------------------------------------ FUSEKI -----------------------------------------------------------------




To explore the rdf files on FUSEKI:

1. Install Java (OpenJDK):
Fuseki requires Java to run. You can install OpenJDK using the package manager. For Ubuntu/Debian-based systems, run the following commands:


	sudo apt update
	sudo apt install openjdk-11-jre
	For other distributions, replace apt with the appropriate package manager (e.g., yum, dnf, pacman).

2. Download Fuseki:
Download the latest Fuseki release from the Apache Jena website (https://jena.apache.org/download/index.cgi). (latest version is 4.7.0) Adjust the version number in the commands below if necessary. Run the following commands to download and extract Fuseki:


	wget https://downloads.apache.org/jena/binaries/apache-jena-fuseki-4.2.0.tar.gz
	tar -xvzf apache-jena-fuseki-4.2.0.tar.gz
	

We already created a configuration file called config.ttl in the folder "databases". Feel free to modify it.The configuration file sets up a Fuseki service with a TDB (Jena's native RDF storage) backend and various service endpoints for querying, updating, and managing RDF data. The configuration defines various service endpoints and settings for the Fuseki server. Here's a breakdown of the key components in the configuration file:

Namespace declarations: The first six lines define the prefixes for the namespaces used in the configuration.

Service definition: The :service_tdb_all block defines a Fuseki service with the following settings:

fuseki:dataset: Associates the service with the dataset :tdb_all.
fuseki:name: Gives the service a name, "tdb".
fuseki:serviceQuery: Enables the SPARQL query endpoint with the path "sparql".
fuseki:serviceReadGraphStore: Enables the read-only Graph Store Protocol with the path "get".
fuseki:serviceReadWriteGraphStore: Enables the read-write Graph Store Protocol with the path "data".
fuseki:serviceUpload: Enables the file upload endpoint with the path "upload".
fuseki:serviceUpdate: Enables the SPARQL update endpoint with the path "update".
rdfs:label: Assigns a label "TDB-SPARQL" to the service.
Dataset definition: The :tdb_all block defines a TDB dataset with the following settings:

	tdb:location: Sets the location of the TDB dataset to the "databases" folder.
	ja:context: Specifies various context settings for the ARQ query engine (Jena's SPARQL query engine) like query timeout, update timeout, and enabling various internal optimizations.
	

3. Start Fuseki server:

	./fuseki-server --config=databases/config.ttl
By default, the Fuseki server will run on port 3030. You can change this by adding the --port=<port_number> option when starting the server.

4. Access Fuseki web interface:
	Open your web browser and navigate to http://localhost:3030/. You should see the Fuseki web interface, where you can manage datasets, run SPARQL queries, and perform updates.

5. Add the data
Click on add data and upload the rdf file. (.owl extension). If you want to make queries with smaller files I reccommand uploading the netflix_titles_transformer_update_part_1.owl, netflix_titles_transformer_update_part_2.owl, netflix_titles_transformer_update_part_3.owl...

6. Run SPARQL queries:
To run a SPARQL query,  enter your SPARQL query in the "query text" box. Click "run query" to execute the query and view the results.
The name of the dataset is displayed below "SPARQL Endpoint".



-----------------------------------------------  Sparklis ------------------------------------------------------------------------------
	

1. Open Sparklis in your browser at http://www.irisa.fr/LIS/ferre/sparklis/.

At the top of the Sparklis interface, you will see a text box labeled "SPARQL endpoint." Replace the default URL in that box with your local Fuseki endpoint URL for the "tdb" dataset:


	http://localhost:3030/tdb/sparql
	
Press the "Connect" button or hit Enter on your keyboard. Sparklis will now connect to your local Fuseki endpoint with the "tdb" dataset.

Once connected, you can use Sparklis to explore, query, and visualize your RDF data using its interactive and natural language-based interface.
Remember that both your Fuseki server and Sparklis must be running for this connection to work. Make sure you've started your Fuseki server and that it's accessible at the specified URL before attempting to connect Sparklis.
	

