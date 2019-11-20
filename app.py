"""
Servidor Flask para respostas no indice
"""
from flask import Flask, request
from query import Query, ZoneQuery
from score import CosineScore
from index import ReverseIndex

#index
print("Lendo Indices")

index_path = './indexes/new_single_index.json'
zone_index_path = './indexes/advanced_reverse_index_dict.json'

# index
index = ReverseIndex(index_path)
zone_index = ReverseIndex(zone_index_path)

# score function
index_score = CosineScore(index)
advanced_score = CosineScore(zone_index)

# Flask interface
app = Flask(__name__)


@app.route('/search')
def search():
    free_text = request.args.get('text', default = '*', type = str)
    query = Query(free_text)
    scores = index_score.score(query)

    return str(scores)

@app.route('/advanced_search')
def advanced_search():
    parameters = request.args

    if not valid_params(parameters.keys()):
        return ""

    query = ZoneQuery(parameters)
    scores = advanced_score.score(query)

    return str(scores)


def valid_params(params):

    valid = ["title", "genre", "description",
    		 "dev", "pub", "Req_min", "Req_max"]

    for p in params:
        if p not in valid:
            return False

    return True


print("Inicializando Flask")
app.run()
