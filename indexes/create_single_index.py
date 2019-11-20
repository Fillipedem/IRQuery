import os
import json

local_path = './advanced_reverse_index_dict.json'
new_path = './single_term.json'

def load_index(lp):
    """
    Ler o arquivo em Json do index
    """
    index = {}

    with open(lp) as file:
        file_text = file.read()
        index = json.loads(file_text)

    return index


def merge_posting_list(post1, post2):
    """
    Merge duas posting list considerando que os docIDs estão em ordem
    """
    new_posting_list = []
    post1_iter = iter(post1)
    post2_iter = iter(post2)

    p1 = next(post1_iter, None)
    p2 = next(post2_iter, None)

    while p1 and p2:

        if p1['id'] < p2['id']:
            new_posting_list.append(p1)
            p1 = next(post1_iter, None)
        elif p1['id'] > p2['id']:
            new_posting_list.append(p2)
            p2 = next(post2_iter, None)
        else:
            new_posting_list.append(p1)
            new_posting_list[-1]['frequency'] += p2['frequency']

            p1 = next(post1_iter, None)
            p2 = next(post2_iter, None)

    if p1:

        while p1:
            new_posting_list.append(p1)
            p1 = next(post1_iter, None)

    if p2:

        while p2:
            new_posting_list.append(p2)
            p2 = next(post2_iter, None)


    return new_posting_list


new_single_index = {}
advanced_index = load_index(local_path)
zones = ['.title', '.genre', '.description', '.dev', '.pub', '.Req_min', '.Req_max']

for term in advanced_index:
    for zone in zones:
        if zone in term:
            new_term = term.split(zone)[0]

            if new_term in new_single_index:

                post1 = new_single_index[new_term]
                post2 = advanced_index[term]

                new_single_index[new_term] = merge_posting_list(post1, post2)
            else:
                # copy posting list
                new_single_index[new_term] = advanced_index[term]

            # if zone in term
            break

###
### save new index
###
with open('new_single_index.json', 'w') as fp:
    json.dump(new_single_index, fp)
