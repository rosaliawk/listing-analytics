1) To input listings from csvs
python input-listings.py [csv1, csv2, ...]

This will return a json containing new listings found in the csvs

2) To get common stats
curl -X POST  -H "Content-Type: application/json" --data '{"beds":2, "city":"San Francisco", "state":"CA"}' http://127.0.0.1:5000/dataset/common_stats/

This is will return a json containing mean, std, min, max, and mode
