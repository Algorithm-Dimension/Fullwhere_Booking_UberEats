#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Remy Adda & Arie Bonan
# Created Date: 2023
# =============================================================================
# Scrap UberEats reviews and insert them into Airtable
# =============================================================================

import os
import airtable_api
from scrap import start_response
import parameter
import logging
import warnings

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
warnings.filterwarnings('ignore', category=UserWarning, append=True)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

HEADERS = {'Authorization': 'Bearer ' + parameter.AIRTABLE_API_KEY}

if __name__ == "__main__":
    logger.info("Start Response: UberEatResponse/main.py")
    # Define the curl command
    current_dir = os.getcwd()
    curl_name = os.path.join(current_dir, "files", "script.sh")

    bases_id, tickets_id, stores_id = airtable_api.retrieve_all_bases_tickets_and_stores()

    for base_id, ticket_id, store_in in zip(bases_id, tickets_id, stores_id):
        airtable_connexion = airtable_api.airtable_access_specific_base_and_table(base_id, ticket_id)
        logger.info("Connexion to base id: {} and ticket id: {}".format(base_id, ticket_id))
        try:
            data_to_answer = airtable_api.get_data_from_table(base_id, ticket_id, store_in, HEADERS)
            logger.info(data_to_answer)
        except KeyError:
            continue
        for data in data_to_answer:
            response_output = start_response(data[0], data[1], data[3], data[2], data[4], curl_name)
            if response_output == 0:
                airtable_api.update_ar_reply_true(airtable_connexion, data[-1])
