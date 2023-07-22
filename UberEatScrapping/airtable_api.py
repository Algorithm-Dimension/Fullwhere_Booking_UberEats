#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Remy Adda & Arie Bonan
# Created Date: 2023
# =============================================================================
# Functions related to Airtable
# =============================================================================


from airtable import Airtable
import requests
import pandas as pd
import logging

from parameter import *


logger = logging.getLogger(__name__)


def setup_logging(logger):
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    if not file_handlers:
        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


def check_if_review_exist(review_id, base_id, ticket_id):
    """

    """
    url = "https://api.airtable.com/v0/{}/{}?filterByFormula=" \
          "%7BReview+ID%7D%3D%22{}%22".format(base_id, ticket_id, review_id)

    headers = {
        'Authorization': 'Bearer ' + AIRTABLE_API_KEY
    }
    response = requests.get(url, headers=headers)
    logger.info(response)

    if response.status_code == 200:
        data = response.json()
        # if len == 0, it means that the request did not find this review id, so we can insert in Airtable
        if len(data["records"]) == 0:
            return False
        else:
            return True
    else:
        logger.debug("Request error to get the review_id: {}".format(review_id))
        return True


def airtable_access_specific_base_and_table(airtable_base_id, airtable_store_id):
    """

    :param airtable_base_id: ID database dans airtable (BASE ID column)
    :param airtable_store_id: Id de la table (store)
    :return: connexion
    """
    airtable_connexion = Airtable(airtable_base_id, airtable_store_id, AIRTABLE_API_KEY)
    return airtable_connexion


def retrieve_bases_tickets_stores_id():
    """

    :return: all the bases, tickets and stores id
    """
    url = 'https://api.airtable.com/v0/appmu35KAiLFx1MqF/tbln1nRchIc194abv'

    headers = {
        'Authorization': 'Bearer ' + AIRTABLE_API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["records"])[["fields"]]
        values_abc = df['fields'].apply(lambda x: (x['Base ID'], x['Ticket table ID'],
                                                   x['Stores table ID']) if 'Base ID'
                                                                            in x and 'Ticket table ID'
                                                                            in x and 'Stores table ID'
                                                                            in x else None)

        filtered_values_abc = values_abc.dropna()

        bases_id = [couple[0] for couple in filtered_values_abc.tolist()]
        tickets_id = [couple[1] for couple in filtered_values_abc.tolist()]
        stores_id = [couple[2] for couple in filtered_values_abc.tolist()]

        assert len(bases_id) == len(tickets_id) == len(stores_id)
        logger.debug("Total elements in bases_id list: {}".format(len(bases_id)))
        return bases_id, tickets_id, stores_id


def retrieve_uuid(airtable_connexion, base_id, store_id, max_records=None):
    """

    :param airtable_connexion: connexion
    :param base_id: base id
    :param store_id: store id
    :param max_records: allow to limit the size of the request
    :return: all the uuids and records id for a specific couple (base id, store id)
    """
    records = airtable_connexion.get_all(maxRecords=max_records)
    all_uuids = []
    all_records_ids = []
    for record in records:
        if "restaurant_uuid" in record['fields'].keys() and "Record ID" in record['fields'].keys():
            all_uuids.append(record['fields']["restaurant_uuid"])
            all_records_ids.append(record['fields']["Record ID"])
        else:
            pass
    print("Total uuids for base: {} and table {}: {}".format(base_id, store_id, len(all_uuids)))
    return all_uuids, all_records_ids


def create_new_record(airtable_connexion, new_record):
    """

    # new_record = {
    #    'Name': 'John Doe',
    #    'Email': 'johndoe@example.com',
    #    'Phone': '+1234567890'
    # }
    :param new_record: new item in airtable
    :return:
    """
    created_record = airtable_connexion.insert(new_record)
    print('Created record:', created_record['fields'])


def retrieve_all_uuids_and_records_ids(fast_run=None):
    # 1 - Retrieve Bases & Tables Ids
    logger.info("Retriving bases, tickets and stores ids ...")
    bases_id, tickets_id, stores_id = retrieve_bases_tickets_stores_id()
    if fast_run:
        bases_id, tickets_id, stores_id = bases_id[:fast_run], tickets_id[:fast_run], stores_id[:fast_run]
    #bases_id, tickets_id, stores_id = bases_id[5:8], tickets_id[5:8], stores_id[5:8]

    all_uuids = []
    all_records_ids = []

    logger.info("Retrieving  all restaurants uuids and records ids by base and store ...")

    for base_id, store_id in zip(bases_id, stores_id):
        airtable_con = airtable_access_specific_base_and_table(base_id, store_id)
        uuids_by_base_and_store, record_id_by_base_and_store = retrieve_uuid(airtable_con,
                                                                             base_id, store_id, max_records=None)
        all_uuids.append(uuids_by_base_and_store)
        all_records_ids.append(record_id_by_base_and_store)

    logger.info("Total uuids (sublists) for all bases and stores: {}".format(len(all_uuids)))
    logger.info("Total records ids (sublists) for all bases and stores: {}".format(len(all_records_ids)))

    return all_uuids, all_records_ids, bases_id, tickets_id, stores_id
