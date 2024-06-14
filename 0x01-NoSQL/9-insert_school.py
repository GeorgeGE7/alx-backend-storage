#!/usr/bin/env python3
"""
Insert a new document in a collection
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    insert a new documents in a collection
    """
    new_data = mongo_collection.insert_one(kwargs)
    return new_data._id
