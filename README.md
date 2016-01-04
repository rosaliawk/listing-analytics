<b>0) To run locally <br></b>
a. git clone https://github.com/rosaliawk/listing-analytics.git <br>
b. mkdir venv <br>
c. cd venv <br>
d. virtualevn venv <br>
e. . venv/bin/activate <br>
f. pip install Flask python numpy pandas <br>


<b>1) To input listings from csvs <br></b>
python input-listings.py [csv1, csv2, cvs3...] 

This will return a json containing new listings found in the csvs <br>


<b>2) To get common stats</b><br>
curl -X POST  -H "Content-Type: application/json" --data '{"beds":2, "city":"San Francisco", "state":"CA"}' http://127.0.0.1:5000/dataset/common_stats/

This is will return a json containing mean, std, min, max, and mode <br>


<b>3) To run Docker image<br></b> 
a. pull rosaliawk/listing-analytics<br>
b. mkdir data<br>
c. cd data<br>
d. cp [location of csv] .<br>
e. cd..

<b>3.1) To input new listings from csvs</b><br>
a. docker run -v [absolute path of csv location]:/data rosaliawk/listing-analytics python /src/input_listings.py data/listings1.csv<br>
e.g. docker run -v /Users/Rosie/input_listings/data:/data --name listing-analytics rosaliawk/listing-analytics python /src/input_listings.py data/listings1.csv

This will return a json containing new listings found in the csvs<br>

<b>3.2) To get common stats</b><br>
a. docker run -p 80:5000 -v [absolute path of current directory/data]:/data --name listing-analytics rosaliawk/listing-analytics python /src/input_listings.py<br>
e.g. docker run -p 80:5000 -v /Users/Rosie/input_listings/data:/data --name listing-analytics rosaliawk/listing-analytics python /src/input_listings.py<br>

b. curl -X POST -H 'Content-Type: application/json' --data '{"city":"San Francisco", "beds":2, "state":"CA"}' http://[mac IP found on Docker kitematic]/dataset/common_stats/<br>
e.g. curl -X POST -H 'Content-Type: application/json' -ty":"San Francisco", "beds":2, "state":"CA"}' http://192.168.99.100/dataset/common_stats/<br>

This will return a json containing mean, std, min, max and median
