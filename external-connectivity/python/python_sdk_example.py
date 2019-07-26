#!/usr/bin/env python
# Run this script on 5.5.X CB server, the cluster should have query and index node
# added to the cluster
from __future__ import print_function

from pprint import pprint

from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator 
from couchbase.exceptions import NotFoundError 
from couchbase.n1ql import N1QLQuery
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

cluster = Cluster('couchbase://localhost')
#cluster = Cluster('couchbase://10.52.1.6,10.52.6.5,10.52.4.5')
#cb = Cluster('http://13.56.228.134:8091/default')
authenticator = PasswordAuthenticator('Administrator', 'password')
cluster.authenticate(authenticator)
#print("CB Server node in this cluster are [" + str(cluster.server_nodes) + "]")
print("CB Server connection PASSED")
#cb.upsert('u:baby_arthur', {'name': 'Arthur', 'email': 'babyarthur@cb.com', 'interests' : ['Holy Grail', 'Kingdoms']})
#cb.upsert('u:baby_arthur', 'Rule the England', replicate_to=0)

# Open the bucket
print('Open the bucket...')
cb = cluster.open_bucket('default')
print('Done...')

print('Upserting a document...')
cb.upsert('u:baby_arthur', {'name' : 'K Arthur Jr', 'email' : 'arthujr@cb.com', 'type' : 'Royales', 'interests' : ['crawling', 'Hunting Unicorns']})
print('Done...')

# get non-existent key
print('Getting non-existent key. Should fail..')
try:
        cb.get('get-non-existent')
except NotFoundError:
        print('Got exception for missing doc')

print('Inserting a doc...')
cb.insert('u:babyliz_liz', {'name': 'Baby Liz', 'email': 'babyliz@cb.com', 'type' : 'Royales', 'interests' : ['Holy Grail', 'Kingdoms and Dungeons']})
print('Done...')

# get non-existent key
print('Getting an existent key. Should pass...')
try:
        print("Value for key 'babyliz_liz'\n")
        val = cb.get('u:babyliz_liz').value
        print("Value for key 'babyliz_liz'\n%s" %(val))
except NotFoundError as e:
        print('Got exception for missing doc with error %s' %(e))

# create primary index
print('Create a primary index...')
mgr = cb.bucket_manager()
mgr.n1ql_index_create_primary(ignore_exists=True)
#cb.n1ql_query('CREATE PRIMARY INDEX ON default').execute()
print('Done...')

# Fire a n1ql query
print('Fire a N1QL query...')
query = N1QLQuery("SELECT name, email FROM `default` WHERE type=\"Royales\"")
print('Output for a N1QL query...')
for row in cb.n1ql_query(query):
    pprint(row)

# Delete a document
print('Delete a doc with key \'u:baby_arthur\'...')
key = 'u:baby_arthur'
cb.remove(key)
print('Done...')
# check if doc is deleted or not
try:
        print("Value for key [%s]" % (key))
        val = cb.get(key).value
        print("Value for key [%s]\n%s" % (val))
except NotFoundError as e:
        print('Got exception for missing doc for key [%s] with error %s' % (key, e))

print('Closing connection to the bucket...')
cb._close()
