#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By: Remy Adda & Arie Bonan
# Created Date: 2023
# =============================================================================
# Scrap UberEats reviews and insert them into Airtable
# =============================================================================

import os
import sys
import airtable_api
from scrap import start_response
import parameter
import logging
import warnings

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
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Gestionnaire pour la sortie de la console (stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

HEADERS = {'Authorization': 'Bearer ' + parameter.AIRTABLE_API_KEY}

if __name__ == "__main__":
    # Define the curl command
    logger.info("Start UberEats Response ...")
    current_dir = os.getcwd()
    curl_name = os.path.join(current_dir, "files", "script.sh")

    bases_id, tickets_id, stores_id = airtable_api.retrieve_all_bases_tickets_and_stores()

    for base_id, ticket_id, store_id in zip(bases_id, tickets_id, stores_id):
        logger.info("Connexion to base {} - ticket {} - store {}".format(base_id, ticket_id, store_id))
        airtable_connexion = airtable_api.airtable_access_specific_base_and_table(base_id, ticket_id)
        try:
            data_to_answer = airtable_api.get_data_from_table(base_id, ticket_id, store_id, HEADERS)
        except KeyError:
            continue
        if len(data_to_answer) > 0:
            logger.info("Total data_to_answer: {}".format(len(data_to_answer)))
        for data in data_to_answer:
            response_output = start_response(data[0], data[1], data[3], data[2], data[4], curl_name)
            if response_output == 0:
                airtable_api.update_ar_reply_true(airtable_connexion, data[-1])
