"""
Index
"""
import json

class ReverseIndex:

    def __init__(self, local_path):
        # load index
        self.index = self.__load_index(local_path)
        # Número de palavras que tem no documento
        self.documents_size = self.__documents_size()
        # Número de documentos
        self.collection_size = len(self.documents_size)


    def __load_index(self, local_path):
        """
        Ler o arquivo em Json do index
        """
        index = {}

        with open(local_path) as file:
            file_text = file.read()
            index = json.loads(file_text)

        return index


    def __documents_size(self):
        """
        Calcula número de termos que aparecem no documento(contando com os repetidos)
        """
        ds = {}

        for term in self.index:
            for posting in self.index[term]:
                docID = posting['id']
                fr = posting['frequency']

                if docID not in ds:
                    ds[docID] = 0

                ds[docID] += fr    # Somando o número de vez que o termo
                                        # aparece no documento

        return ds


    def posting(self, term):
        """
        Retorna a posting_list do termo
        returns: list [('id': 12, 'frequency': 1), ...]
        """
        if term not in self.index:
            return []

        return self.index[term]



###       ###
### Teste ###
###       ###
local_path = './indexes/advanced_reverse_index_dict.json'
ReverseIndex(local_path)
