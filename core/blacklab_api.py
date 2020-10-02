import urllib.parse
import urllib.request
import urllib.error
import json
import os

# for production
API_URI = os.environ['PTT_BACKEND_URL']

# for debug
# API_URI = os.environ['PTT_BACKEND_PUBLIC_URL']

# post type
ALL = '0'
TITLE = '1'
BODY = '2'
COMMENT_POS = '3'
COMMENT_NEG = '4'
COMMENT_NEU = '5'
COMMENT_ALL = '6'


def get_all_boards():

    url = f"{API_URI}/fields/board?outputformat=json" 

    with urllib.request.urlopen(url) as f:
        response = json.loads(f.read().decode('utf-8'))
    
    return list(response['fieldValues'].keys())

def blacklab_get_concordance(query=None, board=None, text_type=None, show_pos=False, window_size=10, start_year=2020, end_year=2020, start_index=0, hits_per_page=50, cql_enable=False):

    # 非CQL的模式
    if not cql_enable:
        query = ''.join([f'[word="{w}"]' for w in query.split(' ')])

        if text_type == TITLE:
            query += ' within <title/>'
        elif text_type == BODY:
            query += ' within <body/>'
        elif text_type == COMMENT_ALL:
            query += ' within <comment/>'
        elif text_type == COMMENT_NEU:
            query += ' within <comment c_type="neu"/>'
        elif text_type == COMMENT_NEG:
            query += ' within <comment c_type="neg"/>'
        elif text_type == COMMENT_POS:
            query += ' within <comment c_type="pos"/>'
        else:
            pass

    # CQL的模式
    else:

        if "::" in query:
            if text_type == TITLE:
                query = " ".join(query.split("::").insert(1, 'within <title/>').insert(2, "::"))
            elif text_type == BODY:
                query = " ".join(query.split("::").insert(1, 'within <body/>').insert(2, "::"))
            elif text_type == COMMENT_ALL:
                query = " ".join(query.split("::").insert(1, 'within <comment/>').insert(2, "::"))
            elif text_type == COMMENT_NEU:
                query = " ".join(query.split("::").insert(1, 'within <comment c_type="neu"/>').insert(2, "::"))
            elif text_type == COMMENT_NEG:
                query = " ".join(query.split("::").insert(1, 'within <comment c_type="neg"/>').insert(2, "::"))
            elif text_type == COMMENT_POS:
                query = " ".join(query.split("::").insert(1, 'within <comment c_type="pos"/>').insert(2, "::"))
            else:
                pass
        else:
            if text_type == TITLE:
                query += ' within <title/>'
            elif text_type == BODY:
                query += ' within <body/>'
            elif text_type == COMMENT_ALL:
                query += ' within <comment/>'
            elif text_type == COMMENT_NEU:
                query += ' within <comment c_type="neu"/>'
            elif text_type == COMMENT_NEG:
                query += ' within <comment c_type="neg"/>'
            elif text_type == COMMENT_POS:
                query += ' within <comment c_type="pos"/>'
            else:
                pass

        # query = f'[word="{query}"]'

    filter_str = f'board:({board}) AND year:[{start_year} TO {end_year}]'

    # if text_type == POST:
    #     filter_str = f'board:({board}) AND post_type:("body") AND year:[{start_year} TO {end_year}]'
    # elif text_type == TITLE:
    #     filter_str = f'board:({board}) AND post_type:("title") AND year:[{start_year} TO {end_year}]'
    # elif text_type == COMMENT:
    #     filter_str = f'board:({board}) AND post_type:("comment") AND year:[{start_year} TO {end_year}]'
    # else:
    #     filter_str = f'board:({board}) AND year:[{start_year} TO {end_year}]'


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
    result['filter'] = filter_str


    return result