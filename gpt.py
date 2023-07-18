import openai
from config import load_config

config = load_config()
openai.api_key = config['openai']['openai_api_key']

with open(config['folders']['prompts'] + '/user_content.txt') as f:
    user_content_prompt = f.read()

with open(config['folders']['prompts'] + '/user_title.txt') as f:
    user_title_prompt = f.read()

with open(config['folders']['prompts'] + '/system_content.txt') as f:
    system_content_prompt = f.read()

with open(config['folders']['prompts'] + '/system_title.txt') as f:
    system_title_prompt = f.read()


def generate_content(description, link):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_content_prompt},
            {"role": "user", "content": user_content_prompt.format(description=description, link=link)}
        ]
    )
    return response.choices[0].message['content'].strip()


def generate_title(content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_title_prompt},
            {"role": "user", "content": user_title_prompt + content}
        ]
    )
    return response.choices[0].message['content'].strip()
