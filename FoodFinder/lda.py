import pandas as pd
import numpy as np
import pickle
from collections import Counter
from nltk.util import ngrams
from gensim import corpora
from gensim import models
from gensim import similarities
import os

# read files
path = os.path.abspath(os.getcwd())
restaurant_df = pd.read_csv(
    path + '/FoodFinder/static/restaurant_final_df.csv', index_col=[0])

comments = pickle.load(
    open(path+'/FoodFinder/static/comments_final', 'rb'))

index = pickle.load(open(path+'/FoodFinder/static/similarity.pkl', 'rb'))


def Recommend(selected_restaurant):
    topic = restaurant_df[restaurant_df['restaurant_name']
                          == selected_restaurant]['topic_id'].tolist()[0]
    restaurant_lst = restaurant_df.groupby('topic_id').get_group(topic).sort_values(
        ['ave_rating'], ascending=False)['restaurant_name'].tolist()
    return [r for r in restaurant_lst if r != selected_restaurant]


def preprocess_input(input_keyword):
    to_token = input_keyword.split()
    dictionary = corpora.Dictionary(comments)
    bow_vector = dictionary.doc2bow(to_token)
    bow_vector_ordered = sorted(bow_vector, key=lambda x: x[1], reverse=True)
    return bow_vector_ordered


def retrieve(preference):
    '''
    input: latent preference vector
    output: top five similar restaurants
    '''
    sims = index[preference]
    recommended_rest_id = sims.argsort()[-2:-7:-1]

    recommended = [restaurant_df[restaurant_df['restaurant_id'] == id]['restaurant_name'].tolist(
    )[0] for id in recommended_rest_id]  # retrieve five restaurants

    # Sorting by ave_rating
    recommended_ordered_index = np.argsort(
        [restaurant_df[restaurant_df['restaurant_name'] == restaurant]['ave_rating'].tolist()[0] for restaurant in recommended])
    if len(recommended_ordered_index) > 5:
        recommended_ordered_index = recommended_ordered_index[:5]
    recommended = [recommended[i] for i in recommended_ordered_index]
    return recommended
