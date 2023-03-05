# -*- coding: utf-8 -*-
"""Anime_Recommendation_System_Complete.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N9J9QURla6_5uLeztqpbJeKEhlebzjao
"""

import numpy as np
import numpy.ma as ma
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
# import tabulate
pd.set_option("display.precision", 1)
import warnings
warnings.filterwarnings('ignore')

"""### Loading the dataset"""

# The anime.csv dataset can also be called the movies dataset
anime = pd.read_csv('anime.csv')
anime.head(10)

# looking at the shape
anime.shape

# checking for nan values in the dataset

anime.isna().sum()

# dropping all nan_values in the dataset
anime = anime.dropna()

# confirming it's dropped.

anime.isna().sum()

# since some columns are dropped, it's best to reset the index to avoid key errors later
anime = anime.reset_index(drop=True)
anime

# it is discovered that some episodes are missing and they are filled with unknown
anime[anime['episodes']=='Unknown']

# A suggestion is to fill the episodes with random numbers
def change(x):
    value = np.random.randint(1, 1000)
    if x == 'Unknown':
        return value
    else:
        return x
anime['episodes'] = anime['episodes'].apply(lambda x: change(x))

anime

# Now the user rating dataset
rating = pd.read_csv('rating.csv')
rating.head(10)

# dataset source shows that rating out of 10 this user has assigned 
# (-1 if the user watched it but didn't assign a rating).
# dropping -1.

rating = rating[rating['rating'] > 0]
rating

# checking the rating size we have
# we have close to 8 million rating, this is a large one.
rating.shape

# considering the computational power that will be needed to process 6 millions rows,
# it is suggested to shuffle the rating data and pick 1.25 million from it.

rating = rating.sample(frac=1)
rating = rating[:1250000]
rating

# checking the unique users in the dataset
rating['user_id'].nunique()

rating['anime_id'].nunique()

# This shows that not all anime are rated.

"""### Creating training sets"""

# it is necessary to have 2 different sets in the dataset
# The first set is the movies (anime) set, the other is the user set.add

# User set contains user features, Movie set contains movie features.

# Movie features will include movie genres, movie type, number of episodes, members and ratings. 
# User features will contain user average rating per genre since it's the only feature we can derive from the dataset

# since we have the same anime_id, we can as well merge the rating and anime datasets on the anime_id
# using all the rating dataset because i need all user's data
rating_ = pd.read_csv('rating.csv')
data = anime.merge(rating_, on='anime_id')
data.head(20)

"""##### Feature engineering"""

# starting the the genres column, since it is common to all.
# getting all genres in the anime dataset with a for loop

genres = []
for genre in anime['genre']:
    sep = genre.split(',')
    for i in sep:
        if i not in genres:
            genres.append(i)

# print(genres)

# The split is having spaces in some cases
def remove(string):
    return "".join(string.split())
genres = [remove(i) for i in genres]
print(genres)

# some of the genres are repeated. removing them all
res = []
[res.append(x) for x in genres if x not in res]
genres = res
print(genres)

len(genres)

"""#### Anime Feature"""

# filling all genres 
# creating a dataset with the genres size and anime size
genre_df = pd.DataFrame(index=np.arange(anime['anime_id'].nunique()), columns=np.arange(len(genres)))
# setting the columns name to the genres
genre_df.columns = genres
# siince it will be created with nan values automatically, filling the nan values with 0.
genre_df = genre_df.fillna(0)
genre_df.head()

# checking the shape
genre_df.shape

# The anime feature needs the genres of each anime one hot encoded, since this can't be achieved automatically.
# it will be done manually
# Before one Hot encoding, we should have the anime id
genre_df.insert(loc=0, column='anime_id', value=anime['anime_id'].values)
genre_df.head()

"""##### One Hot Encoding"""

for i in range(len(genre_df)):
    anime_genre = anime['genre'][i].split(',')
    anime_genre = [remove(i) for i in anime_genre]
    for genre in anime_genre:
        genre_df[genre][i] = 1

genre_df

# let's confirm the last anime_id
anime.tail()

"""##### Other features"""

# Looking at the other features, they can be easily soeted out
others = anime[['type', 'episodes', 'rating', 'members']]
anime_feat = pd.concat([genre_df, others], axis=1)
anime_feat

# One hot encoding the type column using dummy variables
anime_feat = pd.get_dummies(anime_feat, columns=['type'])
anime_feat

anime_feat.rename(columns={'type_Movie':'Movie', 'type_Music':'Music', 'type_ONA':'ONA', 'type_OVA':'OVA',
'type_Special':'Special', 'type_TV':'TV'}, inplace=True)
anime_feat

# anime_feat.columns

# Now the anime feature is complete.

"""#### User Features"""

# # creating a new dataframe called user preference.

# user_pre = pd.DataFrame(index=np.arange(data.user_id.nunique()), columns=np.arange(len(genres)))
# user_pre.columns = genres
# user_pre

# user_pre.columns

# user_pre.insert(loc=0, column='user_id', value=data['user_id'].unique())
# user_pre

# user_index = 0
# # starting with unique users
# for user in user_pre['user_id']:
#     user_info = data[data['user_id'] == user]
#     # obviously a user can't rate an anime twice
#     # selecting the genre
#     genre_agg = 0
#     for genre in genres:
#         # setting initial genre aggregate as 0
#         # converting the anime_genres to a list
#         anime_genre = user_info['genre'].tolist()
#         # scalling through each string in the list
#         for selected_genre in anime_genre:
#             # spliting to get each genre
#             sep = selected_genre.split(',')
#             # removing spaces that comes from spliting ,using a function defined earlier
#             sep = [remove(i) for i in sep]
#             # eliminating possible genre repetition
#             res = []
#             [res.append(x) for x in sep if x not in res]
#             sep = res
#             # checking if genre is in the list of genre for each anime watched
#             if genre in sep:
#                 # adding 1 if it's there
#                 genre_agg += 1
#         # calculating the average of each genre on the scale of 10
#         genre_avg = genre_agg * 10/len(user_info)
#         # adding to the user_pre data for the genre and user
#         user_pre.loc[user_index, genre] = genre_avg
#         genre_agg = 0

#     user_index += 1

# user_pre

# user_pre.to_csv('user_preference.csv', index=False)

# Loading a prepared dataset
user_perf = pd.read_csv('user_preference.csv')
user_perf

# Now we have user data
# merging the rating and user_pref dataframe to see user's rating per anime


user_rating = rating.merge(user_perf, on='user_id')
user_rating

rated_anime_id = rating['anime_id'].unique()
rated_anime_id



# # saving this dataframe
# user_rating.to_csv('User_rating.csv', index=False)

rated_anime_id = rating['anime_id'].unique()
rated_anime_id

rated_anime = anime_feat[anime_feat['anime_id'].isin(rated_anime_id)]
rated_anime

# creating a new dataframe for rated animes.
anime_rating = rating.merge(rated_anime, on='anime_id')
anime_rating

# rating_x is the user rating, rating_y is the anime rating. It's best to raname to avoid issues 
anime_rating.rename(columns={'rating_x':'user_rating', 'rating_y':'anime_rating'}, inplace=True)
anime_rating

# dropping thr user_id and user_rating column
anime_rating = anime_rating.drop(['user_id', 'user_rating'], axis=1)
anime_rating

# # saving this dataframe
# anime_rating.to_csv('anime_rating.csv', index=False)

# A necessary condition is that the final user feature and anime feature have the same size
# Hence setting both to 1.5m

user_final = user_rating[:1200000]
anime_final = anime_rating[:1200000]

# setting rating column as the target variable
target = user_final['rating']
# dropping the rating column
user_final = user_final.drop(['rating', 'anime_id'], axis=1)
user_final

anime_final

"""### Preprocessing"""

from sklearn.preprocessing import StandardScaler, MinMaxScaler
# scaling the data

user_scaler = StandardScaler()

user_scaler = user_scaler.fit(user_final)
scaled_user_data = user_scaler.transform(user_final)

anime_scaler = StandardScaler()
anime_scaler = anime_scaler.fit(anime_final)
scaled_anime_data = anime_scaler.transform(anime_final)

minmax = MinMaxScaler((-1,1))
minmax.fit(target.values.reshape(-1, 1))
y_train = minmax.transform(target.values.reshape(-1, 1))

scaled_user_data

scaled_user_data.shape

scaled_anime_data

y_train

# splitting the data into train and test set
from sklearn.model_selection import train_test_split

user_train, user_test = train_test_split(scaled_user_data, test_size=0.20, random_state=42)
anime_train, anime_test = train_test_split(scaled_anime_data, test_size=0.20, random_state=42)
target_train, target_test = train_test_split(y_train, test_size=0.20, random_state=42)

user_train.shape, anime_train.shape, target_train.shape, user_test.shape, anime_test.shape, target_test.shape

"""### Content Based Filtering with Neural Network"""

# num_outputs = 32
# tf.random.set_seed(1)
# user_NN = tf.keras.models.Sequential([   
#     tf.keras.layers.Dense(256, activation='relu'),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(num_outputs)
# ])

# anime_NN = tf.keras.models.Sequential([   
#     tf.keras.layers.Dense(256, activation='relu'),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(num_outputs)
# ])

# # create the user input and point to the base network
# input_user = tf.keras.layers.Input(shape=(user_train.shape[1]))
# vu = user_NN(input_user)
# print(vu.shape)
# vu = tf.linalg.l2_normalize(vu, axis=1)


# # create the anime input and point to the base network
# input_anime = tf.keras.layers.Input(shape=(anime_train.shape[1]))
# vm = anime_NN(input_anime)
# print(vm.shape)
# vm = tf.linalg.l2_normalize(vm, axis=1)


# # compute the dot product of the two vectors vu and vm
# output = tf.keras.layers.Dot(axes=1)([vu, vm])

# # specify the inputs and output of the model
# model_1 = tf.keras.Model([input_user, input_anime], output)

# model_1.summary()

# # compiling the model
# tf.random.set_seed(1)
# cost_fn = tf.keras.losses.MeanSquaredError()
# opt = keras.optimizers.Adam(learning_rate=0.03)
# model_1.compile(optimizer=opt,
#               loss=cost_fn)

# # training the model
# tf.random.set_seed(1)
# model_1.fit([user_train, anime_train], target_train, epochs=10)

# model_1.evaluate([user_test, anime_test], target_test)

# model_1.save('New_model1')

model_1 = keras.models.load_model('New_model1')
model_1

"""#### New User Prediction"""

# The imagination is that, the new user will select anime genres prefrences. 
# Considering that the user chose those genres, the average rating given automatically to the genres will be 10
# Two datasets will be formed, the first will be that of user preference, the secod will be for the anime

def New_User(interest, anime_type):
    likes = interest + list(anime_type)
    sep = likes
    # removing spaces that comes from spliting ,using a function defined earlier
    sep = [remove(i) for i in sep]
    # eliminating possible genre repetition
    res = []
    [res.append(x) for x in sep if x not in res]
    liked = res
    # just in case there's a wrong input ,it's best to filter things out.
    likes = [i for i in liked if i in anime_feat.columns[1:]]
    types = ['Movie', 'Music','ONA', 'OVA', 'Special', 'TV']
    new_user = pd.DataFrame(index=np.arange(1), columns=np.arange(len(genres)))
    # setting the columns name to the genres
    new_user.columns = genres
    # siince it will be created with nan values automatically, filling the nan values with 0.
    new_user = new_user.fillna(0)
    newid = max(rating['user_id'].values) + 1
    new_user.insert(loc=0, column='user_id', value=newid)
    for k in likes:
        # auto capitalising
        cap = k.capitalize()
        if cap in new_user.columns:
            # setting it to 10 since user preferred it
            new_user[cap] = 10


    # -------------------------------------------------------------------------------------------

    # Anime feature
    new_user_anime = pd.DataFrame(index=np.arange(1), columns=np.arange(len(anime_feat.columns)))
    new_user_anime.columns = anime_feat.columns
    new_user_anime = new_user_anime.fillna(0)
    # Filling with values
    for i in likes:
        # auto capitalising
        cap = i.capitalize()
        if cap in new_user_anime.columns:
            new_user_anime[cap] = 1
        elif i in types:
            new_user_anime[i] = 1

    # keeping anime IDs
    ids = anime_feat['anime_id']
    # removing other features from the anime feat dataset
    search_anime_feat = anime_feat.drop(['anime_id', 'episodes', 'rating', 'members'], axis=1)
    # doing the same here.
    new_user_anime = new_user_anime.drop(['anime_id', 'episodes', 'rating', 'members'], axis=1)
    # converting them to arrays
    new_user_anime_arr = new_user_anime.values
    search_anime_feat = search_anime_feat.values

    # a list for Euclidean distance
    ED = []
    for feat in search_anime_feat:
        dist = np.linalg.norm(new_user_anime_arr - feat)
        ED.append(dist)

    # creating a dataframe for the Ids and distance
    distance = pd.DataFrame()
    distance['anime_id'] = ids
    distance['euc_dist'] = ED

    # sorting the result based on ascending order of the euc distance
    distance = distance.sort_values(by='euc_dist', ascending=True)
    # fetching the top 30 anime ids
    selected_animes = distance['anime_id'][:30]
    # extracting selected animes from anime feat
    selection = anime_feat[anime_feat['anime_id'].isin(selected_animes)]

    # -----------------------------------
    # now creating the user and anime features. starting with getting their arrays
    new_user_feat = new_user.values
    new_user_anime_feat = selection.values
    # since the selected anime size is 30, to avoid creating a loop when using the model it is suggested to use np.repeat to make the user shape like that of the anime
    new_user_feat = np.repeat(new_user_feat, len(selection), axis=0)


    # ----------------------------------------
    # preprocessing the data we have 
    prep_user_feat = user_scaler.transform(new_user_feat)
    prep_anime_feat = anime_scaler.transform(new_user_anime_feat)

    # -------------------------------------------
    # now passing it to our model
    model_prediction = model_1.predict([prep_user_feat, prep_anime_feat])
    # this result is in the scaled format, it needs to be reversed
    prediction = minmax.inverse_transform(model_prediction)
    # now we have our prediction, it should be presented in a dataframe
    # considering the fact that it was created according to it's proportion in the anime order, we can retrieve that first
    result = anime[anime['anime_id'].isin(selection['anime_id'].tolist())]
    # renaming rating column as anime rating
    result.rename(columns={'rating':'anime_rating'}, inplace=True)
    result['predicted_rating'] = prediction
    result = result.sort_values(by='predicted_rating', ascending=False)
    return result



# print(genres)

# New_User()







