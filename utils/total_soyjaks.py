from bs4 import BeautifulSoup
import requests
import logging

logging.basicConfig(level=logging.INFO)

booru_url = 'https://booru.soy/post/list'


def get_max_soyjak_id():
    logging.info('Getting max soyjak ID...')

    # Get the page
    page = requests.get(booru_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    latest_post = soup.find('a', {'class': 'thumb shm-thumb shm-thumb-link'})
    max_soyjak_id = latest_post.get('data-post-id')

    # Return latest post id as max amount of soyjaks
    logging.info(f'Latest post id: {max_soyjak_id}')
    return int(max_soyjak_id)
