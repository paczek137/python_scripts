#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

import datetime
import os
import json
import facebook
from argparse import ArgumentParser

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\np9_facebook_graph.py"
print(s)

def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--page')
    parser.add_argument('--paczek')
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    print(args.paczek)

    page_id = "marvelstudios"
    page_me = "me"
    #access_token = "EAACEdEose0cBAICOyBXaLZCd8ze1xQEGttl4EPV1bOi2KSlStFMcp94Up0c6ZAyedW8qUmqTAJOOZAcZChvx8iNE9XiTOW6A3RgmFZBLOBs5Yw7mG64lisb2QYBtZCe341T3w2JQcOqyxnCFY8WG25OblfH9XZCOB1fBKU0dd7YBbhJfMQogPBZAQgq2UXFmVHgZD"
    access_token = "EAAG62GunmNwBADu95n5lubv9NYkdvDrAzvu7TtnjNoHa9sCUOHWTZCKZCUlaJDbgxplk9Xs0twVbNY8ZCXJFZANmEmrqYUcAI6hRoXr0JxNnZAA5IHeqUmUjOYIaZB3ShUvapSU1Nr5wytcyufYJDZA0101r04yBhenDeoOmZCAd5CWkZBGc0ZCWdwq2jA6AWoZA4Qg0a2T5PQfOAZDZD"

    #graph = facebook.GraphAPI(access_token)
    #page = graph.get_object(page_id)
    fields = ['id',
              'name',
              'about',
              ]
    fields = ','.join(fields)
    graph = facebook.GraphAPI(access_token)
    page = graph.get_object(page_me, fields=fields)
    print(json.dumps(page, indent=4))
