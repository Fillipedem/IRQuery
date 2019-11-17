"""
Score functions
"""
import numpy as np


class Score:

    def __init__(self, index):
        pass

    def score(self, query):
        pass


class CosineScore(Score):

    def __init__(self, index):
        self.index = index
        self.lengths = {}

        self.__initialize_lengths()


    def score(self, query):
        """
        Retorna os top 20 com maiores ranks para a query
        """
        return self.__cosine_score(query)


    def __term_score(self, tf, df, num_docs):

        idf = np.log(num_docs / df)

        return tf*idf


    def __initialize_lengths(self):
        # num de documentos
        docIDs = self.index.documents()
        N = len(docIDs)

        # inicializando o vetor de pesos dos documentos para zero
        vectors = {}
        for docID in docIDs:
            vectors[docID] = np.zeros(len(self.index.terms()))

        # Para cada termo calculamos o valor tfidf de cada documento
        for idx, term in enumerate(self.index.terms()):

            posting_list = self.index.posting_list(term)
            df = len(posting_list)

            for posting in posting_list:
                docID = posting['id']
                fr = posting['frequency']/self.index.documents_size[docID]

                vectors[docID][idx] = self.__term_score(fr, df, N)

        for docID in docIDs:
            self.lengths[docID] = np.linalg.norm(vectors[docID])


    def __cosine_score(self, query):
        """
        Retorna os top 20 com maiores ranks para a query com base
        na similariedade do coseno
        """
        N = self.index.collection_size
        scores = {}

        for docID in self.index.documents():
            scores[docID] = 0

        # para cada termo da query - Term-At-Time
        for term in query.terms:
            # retrieve posting list
            posting_list = self.index.posting_list(term)

            # se o termo não existir no vocab
            if not posting_list:
                continue

            # calcular o peso do termo
            fr = query.terms[term]
            df =  len(posting_list)
            qweight = self.__term_score(fr, df, N)

            for posting in posting_list:
                docID = posting['id']
                doc_fr = posting['frequency']/self.index.documents_size[docID]

                dweight = self.__term_score(doc_fr, df, N)

                scores[docID] += dweight*qweight

            for docID in scores:
                scores[docID] /= self.lengths[docID]

        # agora apenas selecionando os top20
        top20 = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:20]

        return top20
