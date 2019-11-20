"""
Score functions
"""
import numpy as np


class Score:
    """
    Interface para class que computa scores
    dado um Index e uma Query
    """
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


        top_scores = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        return top_scores


class VectorScore(Score):

    def __init__(self, index):
        self.index = index
        self.lengths = {}

        self.__initialize_lengths()


    def score(self, query):
        """
        Retorna os top 20 com maiores ranks para a query
        """
        return self.__vector_score(query)


    def __initialize_lengths(self):
        # num de documentos
        docIDs = self.index.documents()
        N = len(docIDs)

        # inicializando o vetor de pesos dos documentos para zero
        vectors = {}
        for docID in docIDs:
            vectors[docID] = np.zeros(len(self.index.terms()))

        for idx, term in enumerate(self.index.terms()):

            posting_list = self.index.posting_list(term)

            for posting in posting_list:
                docID = posting['id']

                vectors[docID][idx] = 1

        for docID in docIDs:
            self.lengths[docID] = np.linalg.norm(vectors[docID])


    def __vector_score(self, query):
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

            for posting in posting_list:
                docID = posting['id']

                scores[docID] += 1

            for docID in scores:
                scores[docID] /= self.lengths[docID]


        top_scores = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        return top_scores


class BIMScore(Score):
    """
    Simple Binary Independent Model

    #Considerando Pt = 1/2 (Probabilidade do termo aparecer no doc
                            Relevante ou não relevante é igual)
    Logo o valor do rank é a soma dos idfs dos termos
    que aparecem nos documentos
    """

    def __init__(self, index):
        self.index = index


    def score(self, query):
        """
        Retorna os top 20 com maiores ranks para a query
        """
        return self.__bim_score(query)


    def __idf(self, df, num_docs):
        """
        Calcula o valor idf para o termo
        """
        idf = np.log(num_docs / df)

        return idf


    def __bim_score(self, query):

        N = self.index.collection_size
        scores = {}

        for docID in self.index.documents():
            scores[docID] = 0

        # 'Term-At-Time' BIM
        for term in query.terms:
            # posting_list
            posting_list = self.index.posting_list(term)

            if not posting_list:
                continue

            # calculando o idf do termo
            df = len(posting_list)
            idf = self.__idf(df, N)

            for posting in posting_list:
                docID = posting['id']
                scores[docID] += idf

        top_scores = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        return top_scores


class ZoneScore(Score):


    def __init__(self, index):
        self.index = index


    def score(self, query):
        """
        Retorna os top 20 com maiores ranks para a query
        """
        return self.__zone_score(query)

    def __zone_score(self, query):
        pass
        #TODO

###
###
###
