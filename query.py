"""
Query classes
"""

class Query:
    """
    Processa as querys como free_text
    """
    def __init__(self, query_text):
        self.query_text = query_text
        self.terms = self.__terms()


    def __terms(self):
        terms = {}

        # lendo cada palavra
        processed_text = self.query_text.lower()

        for word in processed_text.split(" "):

            term = word
            if term in terms:
                terms[term] += 1
            else:
                terms[term] = 1

        return terms


class ZoneQuery:
    """
    Processa querys com textos para cada zona especifica
    """

    def __init__(self, query_zones):
        self.query_zones = query_zones
        self.terms = self.__terms()


    def __terms(self):
        terms = {}

        # para cada zona
        for zone in self.query_zones:
            processed_text = self.query_zones[zone].lower()

            # lendo cada palavra
            for word in processed_text.split(" "):
                term = self.__zone_term(zone, word)

                if term in terms:
                    terms[term] += 1
                else:
                    terms[term] = 1

        return terms

    def __zone_term(self, zone, term):

        return str(term) + '.' + str(zone)
