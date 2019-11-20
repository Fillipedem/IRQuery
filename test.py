from score import CosineScore, BIMScore, VectorScore
from index import ReverseIndex
from query import Query, ZoneQuery
from rank_correlation import spearman


#
def create_rank(fst_rank, snd_rank):

    fst_top = fst_rank[:10]
    snd_top = snd_rank[:10]

    for docID in snd_rank[10:]:

        if docID in fst_rank[:10]:
            snd_top.append(docID)

    for docID in fst_rank[10:]:

        if docID in snd_rank[:10]:
            fst_top.append(docID)

    return fst_top, snd_top

# queries
with open('./tests/queries.txt', 'r') as f:
    file = f.read()

queries = file.split('\n')
print(queries)

# primeiro lendo o index
local_path = './indexes/new_single_index.json'
index = ReverseIndex(local_path)

# score
bim_score = BIMScore(index)
cosine_score = CosineScore(index)
vector_score = VectorScore(index)

# retornando o melhor resultado para as 5 queries
for idx, query_text in enumerate(queries):
    if not len(query_text):
        continue

    query = Query(query_text)

    bim_top = bim_score.score(query)
    cosine_top = cosine_score.score(query)
    vector_top = vector_score.score(query)
    fst, snd = create_rank(bim_top, cosine_top)
    correlacao1 = spearman(fst, snd)
    fst2, snd2 = create_rank(bim_top, vector_top)
    correlacao2 = spearman(fst2, snd2)
    fst3, snd3 = create_rank(cosine_top, vector_top)
    correlacao3 = spearman(fst3, snd3)
    # write results
    with open('./tests/results/query_' + str(idx), 'w') as f:
        f.write(query.query_text + '\n')
        f.write('BIM rank: ' + '\n')
        f.write(str(bim_top[:10]) + '\n')
        f.write('Cosine rank' + '\n')
        f.write(str(cosine_top[:10]) + '\n')
        f.write('Boolean rank' + '\n')
        f.write(str(vector_top[:10]) + '\n')
        f.write('Correlação BIM/Cosine: ' + str(correlacao1))
        f.write('\n')
        f.write('Correlação BIM/Vector: ' + str(correlacao2))
        f.write('\n')
        f.write('Correlação Cosine/Vector: ' + str(correlacao3))
        f.write('\n')
        # write spearm rank correlation
