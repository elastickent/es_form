"""Create index with mapping."""


from elasticsearch import Elasticsearch
es = Elasticsearch(
    ["https://ELASTICUSER:ELASTICPASSWD@ELASTICHOST:9200"],
    use_ssl=True,
    verify_certs=False
)
mapping = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
          "location": {
            "type": "geo_point"
          },
          "ip": {
            "type": "ip"
          }
        }
    }
}
es.indices.delete(index='cv19')
es.indices.create(index='cv19', body=mapping)
