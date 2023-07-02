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
from tqdm import tqdm

HEADERS = {'Authorization': 'Bearer ' + parameter.AIRTABLE_API_KEY}

if __name__ == "__main__":
    # Define the curl command
    current_dir = os.getcwd()
    curl_name = os.path.join(current_dir, "files", "script.sh")

    bases_id, tickets_id, stores_id = airtable_api.retrieve_all_bases_tickets_and_stores()

    for base_id, ticket_id, store_in in tqdm(zip(bases_id, tickets_id, stores_id)):
        airtable_connexion = airtable_api.airtable_access_specific_base_and_table(base_id, ticket_id)
        try:
            data_to_answer = airtable_api.get_data_from_table(base_id, ticket_id, store_in, HEADERS)
        except KeyError:
            continue
        if len(data_to_answer) > 0:
            print(len(data_to_answer))
        for data in data_to_answer:
            response_output = start_response(data[0], data[1], data[3], data[2], data[4], curl_name)
            if response_output == 0:
                airtable_api.update_ar_reply_true(airtable_connexion, data[-1])
