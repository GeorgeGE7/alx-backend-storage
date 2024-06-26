#!/usr/bin/env python3
""" Log nginx stats next version """
from pymongo import MongoClient


def nginx_stats_check():
    """ provides some stats about Nginx logs stored in Mongo database"""
    mongo_client = MongoClient()
    nginx_collection = mongo_client.logs.nginx

    num_of_docs = nginx_collection.count_documents({})
    print("{} logs".format(num_of_docs))
    print("Methods:")
    methods_list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods_list:
        method_count = nginx_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, method_count))
    state = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(state))

    print("IPs:")

    top_ips = nginx_collection.aggregate([
        {"$group":
         {
             "_id": "$ip",
             "count": {"$sum": 1}
         }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for top_ip in top_ips:
        count = top_ip.get("count")
        ip_address = top_ip.get("ip")
        print("\t{}: {}".format(ip_address, count))


if __name__ == "__main__":
    nginx_stats_check()
