from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

# Створюємо граф
g = Graph()

# Завантажуємо RDF-документ із файлу
rdf_file = "stalker2_detailed.rdf"
g.parse(rdf_file, format="turtle")

# Виводимо кількість триплетів
print(f"Граф завантажено! Містить {len(g)} триплетів.")

# Запит на підрахунок триплетів
query_count = prepareQuery("""
    SELECT (COUNT(*) as ?count)
    WHERE { ?s ?p ?o }
""")
results_count = g.query(query_count)
for row in results_count:
    print(f"Загальна кількість триплетів: {row['count']}")

# Запит для виведення одного ресурсу (dc:title)
query_title = prepareQuery("""
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    SELECT ?title
    WHERE { ?s dc:title ?title }
    LIMIT 1
""")
results_title = g.query(query_title)
for row in results_title:
    print(f"Назва одного ресурсу: {row['title']}")

# Запит для отримання всіх ресурсів класу wiki:Tool
query_class = prepareQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX wiki: <https://uk.wikipedia.org/wiki/S.T.A.L.K.E.R._2:_%D0%A1%D0%B5%D1%80%D1%86%D0%B5_%D0%A7%D0%BE%D1%80%D0%BD%D0%BE%D0%B1%D0%B8%D0%BB%D1%8F#>
    SELECT ?resource
    WHERE { ?resource rdf:type wiki:Tool }
""")
results_class = g.query(query_class)
print("Ресурси класу 'wiki:Tool':")
for row in results_class:
    print(f"- {row['resource']}")

# Запит для отримання значень властивості wiki:description для всіх ресурсів
query_property = prepareQuery("""
    PREFIX wiki: <https://uk.wikipedia.org/wiki/S.T.A.L.K.E.R._2:_%D0%A1%D0%B5%D1%80%D1%86%D0%B5_%D0%A7%D0%BE%D1%80%D0%BD%D0%BE%D0%B1%D0%B8%D0%BB%D1%8F#>
    SELECT ?resource ?description
    WHERE { ?resource wiki:description ?description }
""")

property_results = g.query(query_property)
print("Інформація про ресурси (властивість wiki:description):")
for row in property_results:
    print(f"Ресурс: {row['resource']}, Опис: {row['description']}")

# Запит для отримання всіх властивостей і значень обраного ресурсу (wiki:Artifact)
query_properties = prepareQuery("""
    PREFIX wiki: <https://uk.wikipedia.org/wiki/S.T.A.L.K.E.R._2:_%D0%A1%D0%B5%D1%80%D1%86%D0%B5_%D0%A7%D0%BE%D1%80%D0%BD%D0%BE%D0%B1%D0%B8%D0%BB%D1%8F#>
    SELECT ?property ?value
    WHERE { wiki:Artifact ?property ?value }
""")

properties_results = g.query(query_properties)
print("Характеристики ресурсу 'wiki:Artifact':")
for row in properties_results:
    print(f"Властивість: {row['property']}, Значення: {row['value']}")

# Запит для отримання всіх підкласів базового класу wiki:GameItem
query_subclasses = prepareQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX wiki: <https://uk.wikipedia.org/wiki/S.T.A.L.K.E.R._2:_%D0%A1%D0%B5%D1%80%D1%86%D0%B5_%D0%A7%D0%BE%D1%80%D0%BD%D0%BE%D0%B1%D0%B8%D0%BB%D1%8F#>
    SELECT ?subclass
    WHERE { ?subclass rdfs:subClassOf wiki:GameItem }
""")

subclasses_results = g.query(query_subclasses)
print("Підкласи базового класу 'wiki:GameItem':")
for row in subclasses_results:
    print(f"- {row['subclass']}")

# Запит для отримання всіх властивостей у графі
query_most_frequent = prepareQuery("""
    SELECT ?property (COUNT(?property) AS ?count)
    WHERE { ?s ?property ?o }
    GROUP BY ?property
    ORDER BY DESC(?count)
    LIMIT 1
""")

frequent_property_results = g.query(query_most_frequent)
for row in frequent_property_results:
    print(f"Найчастіше зустрічається властивість: {row['property']} (кількість: {row['count']})")

# CONSTRUCT-запит для створення зв'язку між wiki:Artifact і wiki:Detector
query_construct = prepareQuery("""
    PREFIX wiki: <https://uk.wikipedia.org/wiki/S.T.A.L.K.E.R._2:_%D0%A1%D0%B5%D1%80%D1%86%D0%B5_%D0%A7%D0%BE%D1%80%D0%BD%D0%BE%D0%B1%D0%B8%D0%BB%D1%8F#>
    CONSTRUCT {
        wiki:Artifact wiki:relatedTo wiki:Detector .
    }
    WHERE {
        wiki:Artifact a wiki:GameItem .
        wiki:Detector a wiki:Tool .
    }
""")

construct_results = g.query(query_construct)
print("Новий граф, створений CONSTRUCT-запитом:")
for subject, predicate, obj in construct_results:
    print(f"Subject: {subject}\nPredicate: {predicate}\nObject: {obj}\n")

# ASK-запит для перевірки, чи є wiki:Artifact екземпляром wiki:GameItem
query_ask = prepareQuery("""
    PREFIX wiki: <https://uk.wikipedia.org/wiki/S.T.A.L.K.E.R._2:_%D0%A1%D0%B5%D1%80%D1%86%D0%B5_%D0%A7%D0%BE%D1%80%D0%BD%D0%BE%D0%B1%D0%B8%D0%BB%D1%8F#>
    ASK {
        wiki:Artifact a wiki:GameItem .
    }
""")

ask_result = g.query(query_ask)
if ask_result.askAnswer:
    print("Ресурс 'wiki:Artifact' є екземпляром 'wiki:GameItem'.")
else:
    print("Ресурс 'wiki:Artifact' НЕ є екземпляром 'wiki:GameItem'.")

# DESCRIBE-запит для отримання всієї інформації про wiki:Artifact
query_describe = prepareQuery("""
    PREFIX wiki: <https://uk.wikipedia.org/wiki/S.T.A.L.K.E.R._2:_%D0%A1%D0%B5%D1%80%D1%86%D0%B5_%D0%A7%D0%BE%D1%80%D0%BD%D0%BE%D0%B1%D0%B8%D0%BB%D1%8F#>
    DESCRIBE wiki:Artifact
""")

describe_results = g.query(query_describe)
print("Інформація про ресурс 'wiki:Artifact':")
for subject, predicate, obj in describe_results:
    print(f"Subject: {subject}\nPredicate: {predicate}\nObject: {obj}\n")
