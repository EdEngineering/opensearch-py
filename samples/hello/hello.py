#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from opensearchpy import OpenSearch
import os

# connect to OpenSearch

host = os.getenv('HOST', default='44.218.44.148')
port = int(os.getenv('PORT', 9200))
auth = (
    os.getenv('USERNAME_OPENSEARCH', 'developer_andres'), 
    os.getenv('PASSWORD', 'BJ6c6F3g8NpVdm')
)
print("host: ", host, "port: ", port, "auth: ", auth)


client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    # client_cert = client_cert_path,
    # client_key = client_key_path,
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    # ca_certs = ca_certs_path
)

info = client.info()
print(f"Welcome to {info['version']['distribution']} {info['version']['number']}!")

# create an index

index_name = 'test-index'

index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

response = client.indices.create(
  index_name, 
  body=index_body
)

print(response)

# add a document to the index

document = {
  'title': 'Moneyball',
  'director': 'Bennett Miller',
  'year': '2011'
}

id = '1'

response = client.index(
    index = index_name,
    body = document,
    id = id,
    refresh = True
)

print(response)

# search for a document

q = 'miller'

query = {
  'size': 5,
  'query': {
    'multi_match': {
      'query': q,
      'fields': ['title^2', 'director']
    }
  }
}

response = client.search(
    body = query,
    index = index_name
)

print(response)

# delete the document

response = client.delete(
    index = index_name,
    id = id
)

print(response)

# delete the index

response = client.indices.delete(
    index = index_name
)

print(response)
