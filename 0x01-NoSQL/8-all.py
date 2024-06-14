#!/usr/bin/env python3
"""
List all documents in a collection
"""
import pymongo


def list_all(mongo_collection):
    """
    function to get all docs in collection
    """
    if not mongo_collection:
        return []
    all_documents = mongo_collection.find()
    return [doc for doc in all_documents]
