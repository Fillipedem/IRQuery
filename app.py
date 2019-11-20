"""
Servidor Flask para respostas no indice
"""
from flask import Flask, request
from query import Query, ZoneQuery
from score import CosineScore
from index import ReverseIndex
from flask import json

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

#
def load_json(path):
    data = {}
    with open(path, 'r') as json_file:
        data = json.load(json_file)

    return data

filtered_data = load_json('./filtered_datastore.json')

# docs
def get_docs(docIDs):
    ans = []

    for docID in docIDs:
        data = load_json('./extract/' + str(docID))
        for fd in filtered_data:
            if fd['id'] == docID:
                data['url'] = fd['url']
                ans.append(data)
                break

    return ans


# Flask interface
app = Flask(__name__)


@app.route('/search')
def search():
    free_text = request.args.get('text', default = '*', type = str)
    query = Query(free_text)
    scores = index_score.score(query)

    docs = get_docs(scores)

    response = app.response_class(
        response=json.dumps(docs),
        status=200,
        mimetype='application/json'
    )

    return response

@app.route('/advanced_search')
def advanced_search():
    parameters = request.args

    if not valid_params(parameters.keys()):
        return ""

    query = ZoneQuery(parameters)
    scores = advanced_score.score(query)

    docs = get_docs(scores)

    response = app.response_class(
        response=json.dumps(docs),
        status=200,
        mimetype='application/json'
    )

    return response


def valid_params(params):

    valid = ["title", "genre", "description",
    		 "dev", "pub", "Req_min", "Req_max"]

    for p in params:
        if p not in valid:
            return False

    return True


print("Inicializando Flask")
app.run()
