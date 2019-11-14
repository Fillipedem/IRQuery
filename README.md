# IRQuery

---------------------------------------------------------------

Para rodar o servidor flask:

terminal: python3 app.py

---------------------------------------------------------------

Exemplos de algumas consultas na interface:


127.0.0.1:5000/search?text=batman joker
127.0.0.1:5000/search?text=The witcher game of the year


Realizar uma consulta por zona:

127.0.0.1:5000/advanced_search?title=batman&description=game of

Todas as zonas validas de consulta:

title
genre
description
dev
pub
req_min
req_max
