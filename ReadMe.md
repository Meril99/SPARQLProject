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
	

3. Start Fuseki server by running this command below in the apache-jena-fuseki-4.7.0 directory:

	./fuseki-server 
	
By default, the Fuseki server will run on port 3030. You can change this by adding the --port=<port_number> option when starting the server.

4. Access Fuseki web interface:
	Open your web browser and navigate to http://localhost:3030/. You should see the Fuseki web interface, where you can manage datasets, run SPARQL queries, and perform updates.

5. Add the data
Create a new database and give it a name.
Click on add data and upload the rdf file. (netflix.owl extension, approx 35MB). If you want to make queries with smaller files I reccommand uploading the netflix_part_1.owl, netflix_part_2.owl, netflix_part_3.owl...

6. Run SPARQL queries:
To run a SPARQL query,  enter your SPARQL query in the "query text" box. Click "run query" to execute the query and view the results.
The name of the dataset is displayed below "SPARQL Endpoint".



-----------------------------------------------  Sparklis ------------------------------------------------------------------------------
	

1. Open Sparklis in your browser at http://www.irisa.fr/LIS/ferre/sparklis/.

At the top of the Sparklis interface, you will see a text box labeled "SPARQL endpoint." Replace the default URL in that box with your local Fuseki endpoint URL for the "name of your dataset" dataset:


	http://localhost:3030/"name of your database"/sparql
	
Press the "Connect" button or hit Enter on your keyboard.


--------------------------------------------------- Protégé -------------------------------------------------------------------------------

Before you import the files on protégé, open Protégé with this command from your terminal (assuming you are on Ubuntu/Debian):
	./run.sh -Xmx[70M]m

This will allocate 70 MB to make sure the file can be imported on Protégé.
	

