from ccc import Corpus

# post type
POST = 0
COMMENT = 1
TITLE = 2

def get_concordance(
    query=None,
    corpus_name=None,
    text_type=None,
    show_pos=False,
    start_index=0,
    end_index=0):

    corpus = Corpus(
        corpus_name=corpus_name.upper(),
        registry_path="/app/cwb/registry"
    )



    if not query.startswith('['):
        query = f'[word="{query}"]'

    # 如果使用者有指定text_type
    if text_type != '':
        if int(text_type) == POST:
            query += ' :: match.text_type = "body"'
        elif int(text_type) == COMMENT:
            query += ' :: match.text_type = "comment"'
        elif int(text_type) == TITLE:
            query += ' :: match.text_type = "title"'
        else:
            pass

    print(f"query: {query}")

    corpus.query(
        query,
        context=10,
    )

    # 是否顯示 pos tag
    if show_pos:
        concordance = corpus.concordance(p_show=['pos'])
    else:
        concordance = corpus.concordance()

    total_hits = concordance.df_node.shape[0]

    # 選擇要顯示的row
    


    result = concordance.lines()

    return result, total_hits


def lines(self, matches=None, p_show=[], order='first', cut_off=100):
    """ creates concordance lines from self.df_node """

    # take appropriate sub-set of matches
    topic_matches = set(self.df_node.index.droplevel('matchend'))

    if matches is None:
        if not cut_off or len(topic_matches) < cut_off:
            cut_off = len(topic_matches)
        if order == 'random':
            topic_matches_cut = sample(topic_matches, cut_off)
        elif order == 'first':
            topic_matches_cut = sorted(list(topic_matches))[:cut_off]
        elif order == 'last':
            topic_matches_cut = sorted(list(topic_matches))[-cut_off:]
        else:
            raise NotImplementedError('concordance order not implemented')
        df_node = self.df_node.loc[topic_matches_cut, :]

    else:
        df_node = self.df_node.loc[matches, :]

    # check if there's anchors
    anchor_keys = set(df_node.columns) - {'region_start', 'region_end', 's_id'}
    anchored = len(anchor_keys) > 0

    # fill concordance dictionary
    concordance = dict()
    for row_ in df_node.iterrows():

        # gather values
        match, matchend = row_[0]
        row = dict(row_[1])
        row['match'] = match
        row['matchend'] = matchend
        row['start'] = row['region_start']
        row['end'] = row['region_end']

        # create cotext
        df = DataFrame(node2cooc(row))
        df.columns = ['match', 'cpos', 'offset']
        df.drop('match', inplace=True, axis=1)

        # lexicalize positions
        for p_att in ['word'] + p_show:
            df[p_att] = df.cpos.apply(
                lambda x: self.corpus.cpos2token(x, p_att)
            )
        df.set_index('cpos', inplace=True)

        # handle optional anchors
        if anchored:
            anchors = dict()
            for anchor in anchor_keys:
                anchors[anchor] = int(row[anchor])
            df['anchor'] = None
            for anchor in anchors.keys():
                if anchors[anchor] != -1:
                    df.at[anchors[anchor], 'anchor'] = anchor

        # save concordance line
        concordance[match] = df

    return concordance