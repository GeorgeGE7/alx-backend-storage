#!/usr/bin/env python3
"""
Updates a school topics
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    update documents with by name
    """
    return mongo_collection.update_many({
            "name": name
        },
        {
            "$set": {
                "topics": topics
            }
        })
