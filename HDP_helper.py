## https://stackoverflow.com/questions/31543542/hierarchical-dirichlet-process-gensim-topic-number-independent-of-corpus-size

import pandas as pd

def extract_topic_probs (gensim_hdp, t = 20, w = 25, isSorted = True, check = False):
    """
    Input the gensim model to get the rough topics' probabilities
    """
    shown_topics = gensim_hdp.show_topics (num_topics = t, num_words = w, formatted = False)
    if check:
        print(shown_topics)
    topics_nos = [ x[0] for x in shown_topics ]
    weights = [ sum([item[1] for item in shown_topics[topicN][1]]) for topicN in topics_nos ]
    if ( isSorted ):
        return pd.DataFrame({'topic_id' : topics_nos, 'weight' : weights}).sort_values(by = "weight", ascending = False);
    else:
        return pd.DataFrame({'topic_id' : topics_nos, 'weight' : weights});

#
def reformat_topic (t: str, topn = 10):
    "given t as gensim.hdp.print_topic, returns topn terms with highest probabilities"
    X = [ x.strip() for x in t.split("+") ]
    Y = [ x.split("*") for x in X ]
    E = [ (float(y[0]), y[1].strip('"')) for y in Y ]
    E = sorted(E, key = lambda x: x[0], reverse = True)
    return " + ".join([ f"{x[0]} * {x[1]}" for x in E[:topn] ])

## term の階層クラスタリングの関数
def hc_clustering_terms_from_hdp (hdp_model, diction, term_type: str, n_topics: int, lowest_density: float, gap_mark: str, sampling_rate: float, max_length: int = None, min_length: int = None, linkage_method: str = 'ward', use_CJK: bool = False, check: bool = False):
    """produce hierarchical clustering of terms from a given HDP"""
    
    import pandas as pd
    import random
    import pprint as pp
    
    ## HDP model を LDP model に変換し encoding を得る
    lda = hdp_model.suggested_lda_model()
    ## get_term_topics(..) では　minimum_probability = 0 としても
    ## probabaly = 0 の topic IDs が得られないので，sparse encoding しか得られない
    term_enc = \
        { term : { x[0] : x[1] for x in lda.get_term_topics (tid, minimum_probability = 0) } for tid, term in diction.items() }
    if check:
        pp.pprint(random.sample(term_enc.items(), 3))
        print(f"Number of terms: {len(term_enc)}")

    ## pandas を使って sparse_enc を full enc に変換
    term_enc_df = pd.DataFrame.from_dict( { k : pd.Series(v) for k, v in term_enc.items()} )
    term_enc_df = term_enc_df.fillna(0)   # 上で生じたNaN を0に変換
    term_enc_df = term_enc_df.transpose() # データを転地
    if check:
        term_enc_df
    
    ## filtering terms: density で filtering
    size0 = len(term_enc_df)
    term_enc_df_density_filtered = term_enc_df[ term_enc_df.sum(axis = 1) >= lowest_density ]
    size1 = len(term_enc_df_density_filtered)
    print(f"{size1} rows remain after density filtering, discarding {size0 - size1} rows")
    
    ## term length で filtering
    term_enc_df = term_enc_df_density_filtered
    if max_length is None and min_length is None:
        pass
    else:
        if not max_length is None and not min_length is None:
            len_filter = [ len(x.replace(gap_mark, "")) >= min_length and len(x.replace(gap_mark, "")) <= max_length for x in term_enc_df.index ]
        elif max_length is None and not min_length is None:
            len_filter = [ len(x.replace(gap_mark, "")) >= min_length for x in term_enc_df.index ]
        elif not max_length is None and min_length is None:
            len_filter = [ len(x.replace(gap_mark, "")) <= max_length for x in term_enc_df.index ]
        term_enc_df = term_enc_df[len_filter]
    ##
    size2 = len(term_enc_df)
    print(f"{size2} rows remain after size filtering, discarding {size1 - size2} rows")
    ## sampling term_enc_df for hc
    sampled_term_enc_df = term_enc_df.sample(round(len(term_enc_df) * sampling_rate))
    size3 = len(sampled_term_enc_df)
    print(f"{size3} rows remain after size filtering, discarding {size2 - size3} rows")
    if check:
        sampled_term_enc_df
    
    ## term の階層クラスタリングの実行
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.cluster.hierarchy import dendrogram, linkage

    ## 日本語表示のための設定
    plt.rcParams['axes.unicode_minus'] = False   #These two lines need to be set manually
    if use_CJK:
        plt.rcParams["font.family"] = "Hiragino Sans" # Windows/Linux では別のフォントを指定
    else:
        plt.rcParams["font.family"] = "Lucida Sans Unicode"

    ## 描画サイズの指定
    plt.figure(figsize = (6, round(10 * len(sampled_term_enc_df) * 0.018)))

    ## 距離行列の構築
    #linkage_methods = [ 'centroid', 'median', 'ward' ]
    #linkage_method  = linkage_methods[-1]
    term_linkage    = linkage(sampled_term_enc_df, method = linkage_method, metric = 'euclidean')

    ## 事例ラベルの生成
    max_term_length = max([ len(x) for x in list(sampled_term_enc_df.index)])
    label_vals = [ x[:max_term_length] for x in list(sampled_term_enc_df.index) ] # truncate doc keys
    
    ## 樹状分岐図の作成
    dendrogram(term_linkage, orientation = 'left', labels = label_vals, leaf_font_size = 8)

    ## 題の指定
    term_df_size = len(sampled_term_enc_df)
    sampling_rate = f"{100 * sampling_rate:.2f}"
    title_header = f"Hierarchical clustering of {term_df_size} terms of lengths {min_length}-{max_length} (= {sampling_rate}% sample) via\n"
    title_body = f"LDA converted from HDP (max_n_topics: {n_topics}); term: {term_type})"
    title_val = title_header + title_body
    plt.title(title_val)
    #
    plt.show()

### end of file
