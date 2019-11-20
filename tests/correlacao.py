"""
Funções para calcular correção entre 2 ranks
"""

def index_dict(list_id):
    """
    Retorna um dicionario com o indice de cada entrada da lista
    """
    ans = {}

    for i in range(len(list_id)):
        ans[list_id[i]] = i

    return ans


def spearman(first_rank,  second_rank):
    """
    input: two list with ids
    output: correlação de spearman
    """

    if len(first_rank) != len(second_rank):
        raise ValueError("Ranks com tamanhos diferentes!")

    if not len(first_rank):
        raise ValueError("Tamanho do rank igual a 0!")

    # Filtrando ranks comuns
    fst_index = index_dict(first_rank)
    snd_index = index_dict(second_rank)

    # distancia
    square_distance = 0
    for docID in first_rank:
        # square distance da pos dos ranks
        square_distance += (fst_index[docID] - snd_index[docID])**2

    # tamanho
    K = len(first_rank)

    spearman = 1 - 6*square_distance/(K*(K**2 - 1))

    return spearman


###
### Teste
###
lista1 = [123, 84, 56, 6, 8, 9, 511, 129, 187, 25]
lista2 = [56, 123, 84, 8, 6, 187, 9, 511, 25, 129]

print(spearman(lista1, lista2)) #0.854
