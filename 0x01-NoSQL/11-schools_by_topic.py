#!/usr/bin/env python3
"""
Where can I learn Python?
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    find by topic
    """
    return mongo_collection.find({"topics":  {"$in": [topic]}})
