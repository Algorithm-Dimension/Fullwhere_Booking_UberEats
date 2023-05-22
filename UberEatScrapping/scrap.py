#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Remy Adda & Arie Bonan
# Created Date: 2023
# =============================================================================
# Functions related to UberEats scrap
# =============================================================================


import logging
import os
import utils
import subprocess
import json

from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)

current_dir = os.getcwd()


def setup_logging(logger):
    logger.setLevel(logging.DEBUG)
    file_handler = logging.handlers.RotatingFileHandler('logs.log', maxBytes=1048576, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def replace_comments_by_tag_if_none(review):
    if review["tags"]:
        if not review["comment"]:
            review["comment"] = ', '.join(str(element) for element in review["tags"])
    return review


def reformat_review(review):
    # First we replace comment by tag if tag not None and comment is None
    replace_comments_by_tag_if_none(review)
    output_ = dict()
    output_["Review ID"] = review["uuid"]
    output_["Note"] = review["rating"]
    output_["Review text"] = review["comment"]
    output_["Number of orders"] = review["eaterTotalOrders"]
    output_["Order amount"] = review["order"]["orderTotal"]
    output_["Reviewer ID"] = review["eater"]["uuid"]
    output_["Reviewer firstname"] = review["eater"]["name"].split(" ")[0]
    output_['🏠 Stores'] = review["order"]["restaurant"]["uuid"]
    output_["Review date"] = review["timestamp"][:10]  # format_date = "YYYY-MM-DD"
    output_["Platform"] = "UberEATS"
    output_["Rating"] = review["rating"]

    return output_


def start_scrap(uuid_list, year, month, day, curl_name):
    logger.info("Start scrap UberEats")
    with open(os.path.join(current_dir, "files", "cookies.txt"), "r") as file:
        cookies_final = file.read()

    curl_get_reviews = utils.define_curl_command(uuid_list, year, month, day)
    curl_get_reviews[5] = curl_get_reviews[5].format(cookies_final)
    with open(curl_name, "w") as file:
        for line_ in curl_get_reviews:
            file.write(line_[:-1])
            if "compressed" in line_:
                continue
            file.write("\n")

    os.chmod(curl_name, 0o755)
    result = subprocess.run(["bash", curl_name], capture_output=True, text=True)
    reviews = json.loads(result.stdout)["data"]["eaterReviews"]

    logger.info("End Scrap")
    return reviews
