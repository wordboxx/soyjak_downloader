import os
import logging

logging.basicConfig(level=logging.INFO)

default_directory = 'soyjaks/'


def create_directory(directory):
    logging.info('Checking for soyjak directory...')
    if not os.path.exists(directory):
        logging.info('Directory not found!')
        logging.info('Creating directory...')
        os.makedirs(directory)
        logging.info(f'Directory {directory} created')
    else:
        logging.info(f'Directory "{directory}" found!')


def count_local_soyjaks(directory):
    logging.info('Checking for local soyjaks...')
    latest_downloaded_post_id = 0

    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            logging.info(f'Searching "{dir}" directory...')
            subdir = str(os.path.join(root, dir))
            for file in os.listdir(subdir):
                post_id = int(file.split('_')[1].split('.')[0])
                if post_id > latest_downloaded_post_id:
                    latest_downloaded_post_id = post_id

    logging.info(f'Latest downloaded post id: {latest_downloaded_post_id}')
    post_id_to_download = latest_downloaded_post_id + 1
    return post_id_to_download
