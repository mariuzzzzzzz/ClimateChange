# new terminal
# cd spider/downloads
# python mongo_import.py -c mdmtemp -i ../temperature_data.jl -u 'mongodb+srv://toor:Xarfer-0hivfy-fuvqox@mdmmongo.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000' -db mdmtemp

import argparse
import json
import os
from pymongo import MongoClient

def to_document(item):
    return item

class JsonLinesImporter:
    def __init__(self, file, mongo_uri, db='mdmtemp', collection='temperature_data'):
        self.file = file
        self.mongo_uri = mongo_uri
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def read_lines(self):
        with open(self.file, 'r', encoding='UTF-8') as f:
            for line in f:
                yield json.loads(line)

    def save_to_mongodb(self):
        documents = [to_document(item) for item in self.read_lines()]
        if documents:
            self.collection.insert_many(documents)
            print(f"Inserted {len(documents)} documents into MongoDB.")
        else:
            print("No documents to insert.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uri', required=True, help="MongoDB URI with username/password")
    parser.add_argument('-i', '--input', required=True, help="Input file in JSON Lines format")
    parser.add_argument('-c', '--collection', required=True, help="Name of the MongoDB collection where the data should be stored")
    parser.add_argument('-db', '--database', required=True, help="Name of the MongoDB database")
    args = parser.parse_args()

    importer = JsonLinesImporter(args.input, args.uri, db=args.database, collection=args.collection)
    importer.save_to_mongodb()
