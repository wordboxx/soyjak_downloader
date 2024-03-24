from bs4 import BeautifulSoup
import requests
import logging
from utils import file_management

logging.basicConfig(level=logging.INFO)

# URL for the booru
booru_url = 'https://booru.soy'
post_url = booru_url + '/post/view/'


def get_image_info(post_id):
    """Gets the image source and variant info from the given post id."""
    logging.info('Getting image source...')

    # Get the page
    page = requests.get(post_url + str(post_id))
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get the image
    image = soup.find('img', {'id': 'main_image'})
    try:
        image_src = image.get('src')
    except AttributeError:
        logging.error('Failed to get image source')
        return None

    # Get image variant
    try:
        variant = soup.find('a', {'class': 'tag_name tag_category_variant'}).text
    except AttributeError:
        logging.error('Failed to get image variant')
        return None

    # Return the image info
    logging.info(f'Downloading from: {post_url + image_src}')
    return image_src, variant


def download_image(src, post_id, variant, destination):
    """Downloads the image from the given source and saves it to the given destination."""
    logging.info('Downloading image')

    image_url = booru_url + src
    response = requests.get(image_url, stream=True)
    image_extension = src.split('.')[-1]

    # Save the image
    if response.status_code == 200:
        logging.info(f'Response: {response.status_code} {response.reason}')
        logging.info('Saving image...')

        # Assign subdirectory for variant
        subdirectory = destination + f'{variant}/'

        # Save the image
        try:
            with open(subdirectory + f'{variant}_' + str(post_id) + '.' + image_extension, 'wb') as out_file:
                out_file.write(response.content)
            logging.info(f'Image saved in {subdirectory}')

        # If the subdirectory does not exist, create it and retry
        except FileNotFoundError:
            logging.error('Subdirectory not found')
            file_management.create_directory(subdirectory)
            logging.info('Retrying...')
            with open(subdirectory + f'{variant}_' + str(post_id) + '.' + image_extension, 'wb') as out_file:
                out_file.write(response.content)

    # Skip the image if the request fails
    else:
        logging.error(f'{response.status_code} {response.reason}')
        logging.error('Failed to download image')
        logging.info('Skipping...')
