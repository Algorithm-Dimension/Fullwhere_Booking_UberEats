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
URL_ = """https://api.airtable.com/v0/{}/{}?filterByFormula=AND(%7BPlatform%7D%3D%22UberEATS%22%2C%7BPost+reply%7D%3D1%2C%7BAR+reply%7D%3D0)"""


def setup_logging(logger):
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    if not file_handlers:
        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


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


def retrieve_all_bases_tickets_and_stores():
    # 1 - Retrieve Bases & Tables Ids
    logger.info("Retriving bases, tickets and stores ids ...")
    bases_id, tickets_id, stores_id = retrieve_bases_tickets_stores_id()

    return bases_id, tickets_id, stores_id


def update_ar_reply_true(airtable_connexion, id_):

    created_record = airtable_connexion.update(record_id=id_, fields={"AR reply": True})
    logger.info('Created record:', created_record['fields'])


def get_rest_uuid(bases_id, stores_id, store_id, headers):
    url_get_rest_uuid = 'https://api.airtable.com/v0/{}/{}/{}'.format(bases_id, stores_id, store_id)
    response_rest_uuid = requests.get(url_get_rest_uuid, headers=headers)
    # TODO CHECK WHY FIELDS DOESN'T HAVE RESTAURANT UUID
    return response_rest_uuid.json()["fields"]["restaurant_uuid"]


def define_coupon(coupon_value):
    if coupon_value == 5:
        return '"TIER_1"'
    elif coupon_value == 10:
        return '"TIER_2"'
    elif coupon_value == 18:
        return '"TIER_3"'
    else:
        return '"NONE"'


def get_data_from_table(bases_id, tickets_id, stores_id, headers):

    url = URL_.format(bases_id, tickets_id)
    response = requests.get(url, headers=headers)
    number_of_reviews = len(response.json()["records"])
    final_data = list()
    coupon_ = 0
    for review_ in response.json()["records"]:
        review_id = '"' + review_["fields"]["Review ID"] + '"'
        store_id = review_["fields"]['🏠 Stores']
        store_id = '"' + get_rest_uuid(bases_id, stores_id, store_id[0], headers) + '"'
        reviewer_id = '"' + review_["fields"]["Reviewer ID"] + '"'
        response_client = '"' + review_["fields"]["Review reply"] + '"'
        if "Coupon" in list(review_["fields"].keys()):
            coupon_ = review_["fields"]["Coupon"]
        coupon_to_add = define_coupon(coupon_)
        final_data.append([review_id, store_id, reviewer_id, response_client, coupon_to_add, review_["id"]])
    return final_data