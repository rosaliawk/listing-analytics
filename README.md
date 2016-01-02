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


<b>3) To get Docker image<br></b> 
look up rosaliawk/listing-analytics

