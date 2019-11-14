"""
Score functions
"""
import numpy as np


class Score:

    def __init__(self, index):
        self.index = index
        self.lengths = {}


    def cosine_score(self, query):
        """
        Retorna os top 20 com maiores ranks para a query
        """
        N = self.index.collection_size
        scores = {}
        lengths = {} #TODO

        for docID in self.index.documents_size:
            scores[docID] = 0
            self.lengths[docID] = 1

        # para cada termo da query - Term-At-Time
        for term in query.terms:
            # retrieve posting list
            posting_list = self.index.posting(term)

            # se o termo não existir no vocab
            if not posting_list:
                continue

            # calcular o peso do termo
            fr = query.terms[term]
            df =  len(posting_list)
            qweight = self.term_score(fr, df, N)

            for posting in posting_list:
                docID = posting['id']
                doc_fr = posting['frequency']

                dweight = self.term_score(doc_fr, df, N)

                scores[docID] += dweight*qweight

            for docID in scores:
                scores[docID] /= self.lengths[docID]

        # agora apenas selecionando os top20
        top20 = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:20]

        return top20

    def term_score(self, tf, df, num_docs):

        idf = np.log(num_docs / df)

        return tf*idf
