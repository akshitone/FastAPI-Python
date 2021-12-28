posts = [
    {"id": 1, "title": "Hello World", "content": "Welcome to my first post"},
    {"id": 2, "title": "Hello World 2", "content": "Welcome to my second post"},
]  # list of Post objects


# helper functions
def find_post(post_id):
    for post in posts:  # iterate over list of posts
        if post["id"] == post_id:  # if post id matches
            return post


def add_post(post):
    post_dict = post.dict()  # convert Post object to dict
    post_dict["id"] = len(posts) + 1  # assign new id
    posts.append(post_dict)   # add new post to list


def find_index_post(post_id):
    for index, post in enumerate(posts):  # iterate over list of posts
        if post["id"] == post_id:  # if post id matches
            return index


def modify_post(post_id, post):
    post_index = find_index_post(post_id)  # find index of post
    if not post_index:
        return None
    post_dict = post.dict()  # convert Post object to dict
    post_dict['id'] = post_id  # assign new id
    posts[post_index] = post_dict  # update post
    return True
