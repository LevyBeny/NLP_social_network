import pickle

# Load the users dicts
with open('./users_dicts/instagram_users.pkl', mode='rb') as f:
    instagram_users = pickle.load(f)

with open('./users_dicts/facebook_users.pkl', mode='rb') as f:
    facebook_users = pickle.load(f)

with open('./users_dicts/pinterest_users.pkl', mode='rb') as f:
    pinterest_users = pickle.load(f)

with open('./users_dicts/tumblr_users.pkl', mode='rb') as f:
    tumblr_users = pickle.load(f)

with open('./users_dicts/general_users.pkl', mode='rb') as f:
    general_users = pickle.load(f)

users_dicts ={
    "pinterest":pinterest_users,
    "facebook":facebook_users,
    "instagram":instagram_users,
    "tumblr":tumblr_users
}




def get_dict_by_name(dict_name):
    return users_dicts[dict_name]

def get_dict_intersection(dict1, dict2):
    keys_1 = set(dict1.keys())
    print("The length of the first dict: {}".format(len(keys_1)))
    keys_2 = set(dict2.keys())
    print("The length of the second dict: {}".format(len(keys_2)))
    intersect = keys_1 & keys_2
    print("The length of the dicts intersection: {}".format(len(intersect)))
    return intersect


def get_dict_by_num_tweets(tweets_dict, min_tweets):
    dict_to_return = dict()
    for key in tweets_dict:
        if tweets_dict[key] > min_tweets:
            dict_to_return[key] = tweets_dict[key]
    return dict_to_return


def write_dict_to_pickle(_dict, path):
    with open(path, mode='wb') as f:
        pickle.dump(_dict, f)


def reduce_dict_by_keys(_dict, keys):
    to_del = []
    for key in _dict:
        if key in keys:
            to_del.append(key)
    for key in to_del:
        del _dict[key]



def create_unique_dict_per_network(network):

    network_over_1 = get_dict_by_num_tweets(get_dict_by_name(network), 1)

    for _network in users_dicts:
        if _network == network:
            continue
        other_network_over_1 = get_dict_by_num_tweets(get_dict_by_name(_network),1)
        intersect = get_dict_intersection(network_over_1, other_network_over_1)
        reduce_dict_by_keys(network_over_1, intersect)

    with open('./unique_dicts/{}.pkl'.format(network), mode='wb') as f:
        print("The length of {} unique dict is {}".format(network,len(network_over_1)))
        pickle.dump(network_over_1, f)


# for network in users_dicts:
#     create_unique_dict_per_network(network)

# intersect_face_insta = get_dict_intersection(insta_over_1, face_over_1)
