import openai
import os
import base64
import requests
import utils
from config import load_config

config = load_config()
openai.api_key = config['openai']['openai_api_key']


def generate_image(title, content):
    with open(os.path.join(config['folders']['prompts'], 'dalle_system.txt')) as f:
        dalle_system_prompt = f.read()

    response = openai.Completion.create(
        engine="davinci",
        prompt=f"{dalle_system_prompt}\n{content}",
        temperature=config['temperature']
    )
    image_desc = response.choices[0].text
    cleaned_title = utils.clean_title(title)
    img = create_dalle_image(image_desc, cleaned_title)
    return img


def create_dalle_image(image_desc, title):
    response = openai.Image.create(
        prompt=image_desc,
        n=1,
        size=config['size']
    )
    image_url = response['data'][0]['url']

    # Download the image data
    image_data = requests.get(image_url).content

    # Clean and sanitize the title
    cleaned_title = utils.clean_title(title)
    image_filename = f"{cleaned_title}.png"

    image_path = os.path.join(config['folders']['images'], image_filename)
    with open(image_path, "wb") as f:
        f.write(image_data)
    return image_path
