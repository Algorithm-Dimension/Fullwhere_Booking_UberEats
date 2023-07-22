#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By: Remy Adda & Arie Bonan
# Created Date: 2023
# =============================================================================
# Scrap UberEats reviews and insert them into Airtable
# =============================================================================

import os
import logging
import traceback
import warnings
from logging.handlers import RotatingFileHandler
import datetime
from datetime import timedelta
import time

import airtable_api
import utils
import scrap
import argparse


logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
warnings.filterwarnings('ignore', category=UserWarning, append=True)

# Chemin absolu du script
script_dir = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Gestionnaire pour le fichier de logs dans le répertoire du script
log_file_path = os.path.join(script_dir, 'logs.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(pathname)s:%(lineno)d - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Today Only')
    parser.add_argument('--today_only', action='store_true')
    args = parser.parse_args()

    start_time = time.time()

    # Log files
    airtable_api.setup_logging(logger)
    utils.setup_logging(logger)
    scrap.setup_logging(logger)

    # Define the current date
    current_date = datetime.date.today()
    yesterday_date = current_date - timedelta(days=1)

    TO_YEAR = current_date.strftime("%Y")
    TO_MONTH = current_date.strftime("%m")
    TO_DAY = current_date.strftime("%d")

    FROM_YEAR = yesterday_date.strftime("%Y")
    FROM_MONTH = yesterday_date.strftime("%m")
    FROM_DAY = yesterday_date.strftime("%d")

    logger.info(100 * "=")
    logger.info("{}/{}/{}".format(TO_DAY, TO_MONTH, TO_YEAR))
    logger.info(100 * "=")

    # Define the curl command
    current_dir = os.getcwd()
    curl_name = os.path.join(os.path.join(os.path.dirname(__file__), "files", "script.sh"))
    print(curl_name)
    print(os.path.join(os.path.dirname(__file__)))

    total_reviews = 0

    # Retrieve all uuids (restaurants), records id, base, tickets and stores ids
    UUID_LIST, RECORDS_IDS_LIST, bases_id, tickets_id, stores_id = airtable_api.retrieve_all_uuids_and_records_ids()
    logger.info(" °°° End of retrieving restaurants, records, bases, tickets, stores ids °°° ")

    # 1 - Retrieve reviews for sub list of uuids (for each sublist of uuid, is associated a sub list
    # of records id, a base id, a ticket id and a store id
    for sub_uuid_list, sub_record_id_list, base_id, ticket_id, store_in in zip(UUID_LIST, RECORDS_IDS_LIST, bases_id, tickets_id, stores_id):

        logger.info("Sub uuid list: {} - sub record id list: {} - base_id: {} - ticket_id: {} - store_id: {}".format(sub_uuid_list, sub_record_id_list, base_id, ticket_id, store_in))

        if len(sub_uuid_list) != 0:
            # We scrap each restaurant one by one (otherwise there are errors,
            # we can not scrap a list of restaurant, values are wrong)
            for uuid, record_id in zip(sub_uuid_list, sub_record_id_list):
                logger.info("Scraping restaurant uuid: {}".format(uuid))
                logger.info("UUID: {} - Record id: {}".format(uuid, record_id))
                if args.today_only:
                    try:
                        reviews = scrap.start_scrap([uuid], TO_YEAR, TO_MONTH, TO_DAY, TO_YEAR, TO_MONTH, TO_DAY, curl_name)
                    except Exception as e:
                        traceback.print_exc()
                        logger.error("UUID: {} - Error: {}".format(uuid, str(e)))
                        reviews = None
                else:
                    try:
                        reviews = scrap.start_scrap([uuid], FROM_YEAR, FROM_MONTH, FROM_DAY, TO_YEAR, TO_MONTH, TO_DAY, curl_name)
                    except Exception as e:
                        traceback.print_exc()
                        logger.error("UUID: {} - Error: {}".format(uuid, str(e)))
                        reviews = None

                # 2 - Insert each review in airtable
                # We write in ticket id table
                logger.info("UUID: {} - Inserting data into Airtable".format(uuid))
                if reviews is None:
                    logger.info("UUID: {} - Reviews is None: Error when scraping UUID: {} on {}/{}/{}".format(uuid, uuid, TO_DAY, TO_MONTH, TO_YEAR))
                elif reviews and len(reviews) != 0:
                    logger.info("UUID: {} - There are reviews on {}/{}/{}".format(uuid, TO_DAY, TO_MONTH, TO_YEAR))
                    airtable_connexion = airtable_api.airtable_access_specific_base_and_table(base_id, ticket_id)

                    logger.info("UUID: {} - Reformatting and inserting all the reviews into Airtable".format(uuid))
                    for review in reviews:
                        # Reformat review following Airtable format
                        new_record = scrap.reformat_review(review)
                        new_record['🏠 Stores'] = [record_id]
                        # Check if review_id exists
                        review_id = review["uuid"]
                        logger.info("UUID: {} - Review id: {}".format(uuid, review_id))
                        review_id_exist = airtable_api.check_if_review_exist(review_id, base_id, ticket_id)

                        if not review_id_exist:
                            logger.info("UUID: {} - Review id {} does not exist. Inserting it".format(uuid, review_id))
                            airtable_api.create_new_record(airtable_connexion, new_record)
                            total_reviews += 1
                        else:
                            logger.info("UUID: {} - Review id {} already exists.".format(uuid, review_id))

                elif len(reviews) == 0:
                    logger.info("UUID: {} - No reviews on {}/{}/{}".format(uuid, TO_DAY, TO_MONTH, TO_YEAR))
                else:
                    pass

    logger.info("End for {}/{}/{}".format(TO_DAY, TO_MONTH, TO_YEAR))
    logger.info("Total reviews inserted: {}".format(total_reviews))
    end_time = time.time()
    total_time_script = end_time - start_time
    logger.info("Durée totale du script: {}".format(total_time_script))
