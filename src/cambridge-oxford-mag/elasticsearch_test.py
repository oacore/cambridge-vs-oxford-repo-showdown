
from elasticsearch import Elasticsearch

def main():
    es = Elasticsearch(hosts=["172.31.9.45", "172.31.9.60"])
    result = es.search(index="citations", doc_type="citations", q="uuid:a35aa9de-a221-30a8-a7f5-95a2c914542")

    filehashes = result['hits']['hits'][0]['_source']
    print filehashes

if __name__ == '__main__':
    main()













