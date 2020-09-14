import urllib.parse
import urllib.request
import urllib.error
import json
import os


API_URI = os.environ['PTT_BACKEND_URL']

# post type
POST = '0'
COMMENT = '1'
TITLE = '2'


def get_all_boards():

    url = f"{API_URI}/fields/board?outputformat=json" 

    with urllib.request.urlopen(url) as f:
        response = json.loads(f.read().decode('utf-8'))
    
    return list(response['fieldValues'].keys())

def blacklab_get_concordance(query=None, board=None, text_type=None, show_pos=False, window_size=10, start_year=2020, end_year=2020, start_index=0, hits_per_page=50, cql_enable=False):

    if not cql_enable:
        query = ''.join([f'[word="{w}"]' for w in query.split(' ')])
        # query = f'[word="{query}"]'

    filter_str = ""

    if text_type == POST:
        filter_str = f'board:({board}) AND post_type:("body") AND year:[{start_year} TO {end_year}]'
    elif text_type == TITLE:
        filter_str = f'board:({board}) AND post_type:("title") AND year:[{start_year} TO {end_year}]'
    elif text_type == COMMENT:
        filter_str = f'board:({board}) AND post_type:("comment") AND year:[{start_year} TO {end_year}]'
    else:
        filter_str = f'board:({board}) AND year:[{start_year} TO {end_year}]'


    params = {
        'patt': query,
        'outputformat': 'json', 
        'first': start_index,
        'number': hits_per_page,       # concordance per page
        'wordsaroundhit': window_size, # context size
        'filter': filter_str

    }


    encoded_params = urllib.parse.urlencode(params)
    print(f"encoded_params: {encoded_params}")

    url = f"{API_URI}/hits?{encoded_params}"
    print(f"url: {url}")

    result = dict()

    try:
        f = urllib.request.urlopen(url)
        response = json.loads(f.read().decode('utf-8'))
    
    except urllib.error.HTTPError as e:
        response = (e.code, e.read())
        return response

    result['totalHits'] = response['summary']['numberOfHits']
    result['hits'] = response['hits']
    result['doc'] = response['docInfos']
    result['patt'] = query


    return result