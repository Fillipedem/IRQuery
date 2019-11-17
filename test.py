from score import Score
from index import ReverseIndex
from query import Query, ZoneQuery


# primeiro lendo o index
local_path = './indexes/advanced_reverse_index_dict.json'
index = ReverseIndex(local_path)

# simple query
query_text = {'title': 'batman Arkham', 'description':
                'batman fights againts'}
query = ZoneQuery(query_text)

query_text2 = {'title': 'the witcher', 'description':
                'blood and wine'}
query2 = ZoneQuery(query_text2)

# score
score = Score(index)

#
scores = score.cosine_score(query)
scores2 = score.cosine_score(query2)
