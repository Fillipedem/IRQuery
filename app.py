"""
Servidor Flask para respostas no indice
"""
from flask import Flask, request
from query import Query, ZoneQuery
from score import Score
from index import ReverseIndex

#index
print("Lendo Indices")

index_path = './indexes/single_term_index_dict.json'
zone_index_path = './indexes/advanced_reverse_index_dict.json'

# index
index = ReverseIndex(index_path)
zone_index = ReverseIndex(zone_index_path)

# score function
index_score = Score(index)
advanced_score = Score(zone_index)

# Flask interface
app = Flask(__name__)


@app.route('/search')
def search():
    free_text = request.args.get('text', default = '*', type = str)
    query = Query(free_text)
    scores = index_score.cosine_score(query)

    return str(scores)

@app.route('/advanced_search')
def advanced_search():
    parameters = request.args

    if not valid_params(parameters):
        return ""

    query = ZoneQuery(parameters)
    scores = advanced_score.cosine_score(query)

    return str(scores)


def valid_params(params):
    #TODO
    return True


print("Inicializando Flask")
app.run()
