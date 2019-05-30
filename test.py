import pickle

# Init users dict - one for each social network
instagram_users = {}
facebook_users = {}
pinterest_users = {}
tumblr_users = {}

# users with no match to social network
general_users = {}

# Save the users dicts
# with open('./users_dicts/instagram_users.pkl', mode='wb') as f:
#     pickle.dump(instagram_users, f)
#
# with open('./users_dicts/facebook_users.pkl', mode='wb') as f:
#     pickle.dump(facebook_users, f)
#
# with open('./users_dicts/pinterest_users.pkl', mode='wb') as f:
#     pickle.dump(pinterest_users, f)

with open('./users_dicts/tumblr_users.pkl', mode='rb') as f:
    tumblr_users = pickle.load(f)

with open('./users_dicts/general_users.pkl', mode='rb') as f:
    general_users = pickle.load(f)

ben =4