from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.media import UploadFile
from wordpress_xmlrpc.methods.posts import NewPost
from xmlrpc import client as xmlrpc_client
import mimetypes
import random

from config import load_config

class WordPressUploader:

    def __init__(self):
        config = load_config()

        # Get credentials from config
        self.client = Client(
            config['wordpress']['url'],
            config['wordpress']['username'],
            config['wordpress']['password']
        )

    def upload(self, title, content, image_path, categories=None):

        # Upload image
        with open(image_path, 'rb') as img:
            data = {
                'name': f'{random.randint(1, 1000)}.png',
                'type': mimetypes.guess_type(image_path)[0],
                'bits': xmlrpc_client.Binary(img.read())
            }
            response = self.client.call(UploadFile(data))
            image_id = response['id']

        # Create post
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = 'publish'
        post.thumbnail = image_id

        # Assign categories
        if categories is not None:
            post.terms_names = {
                'category': categories
            }

        # Publish post
        self.client.call(NewPost(post))
