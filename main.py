import utils.downloader as downloader
import utils.file_management as file_management
import utils.total_soyjaks as total_soyjaks
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    # Create the default directory
    file_management.create_directory(file_management.default_directory)

    # Get the maximum amount of soyjaks
    try:
        maximum_soyjaks = total_soyjaks.get_max_soyjak_id()
    # If the request fails, log the error and exit
    except AttributeError:
        logging.error('Failed to get maximum soyjak ID')
        logging.info('Exiting...')
        exit(1)

    post_id = file_management.count_local_soyjaks(file_management.default_directory)

    # Download all soyjaks
    while post_id <= maximum_soyjaks:
        logging.info(f'Getting soyjak {post_id} / {maximum_soyjaks}...')
        try:
            src, variant = downloader.get_image_info(post_id)
            downloader.download_image(src, post_id, variant, file_management.default_directory)
        except TypeError:
            logging.error('Failed to download image')
            logging.info('Skipping...')
        post_id += 1
    logging.info('All soyjaks downloaded')
