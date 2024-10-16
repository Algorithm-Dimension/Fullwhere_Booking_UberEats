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


logger = logging.getLogger(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))


def setup_logging(logger):
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    if not file_handlers:
        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(pathname)s:%(lineno)d - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


def start_response(review_id, restaurant_id, comments, reviewer_id, coupon_, curl_name):
    logger.info("Start response for review id: {} - restaurant id: {}".format(review_id, restaurant_id))
    logger.info("Reviewer id: {} - coupon: {} - comments: {}".format(reviewer_id, coupon_, comments))

    with open(os.path.join(current_dir, "files", "cookies.txt"), "r") as file:
        cookies_final = file.read()

    curl_response = utils.define_curl_command(cookies_final, review_id, restaurant_id, comments, reviewer_id, coupon_)

    with open(curl_name, "w") as file:
        for line_ in curl_response:
            file.write(line_[:-1])
            if "compressed" in line_:
                continue
            file.write("\n")

    os.chmod(curl_name, 0o755)
    result = subprocess.run(["bash", curl_name], capture_output=True, text=True)
    logger.info("Review_id: {} - restaurant id: {} - reviewer id: {} - "
                "comment: {}".format(review_id, restaurant_id, reviewer_id, comments))
    logger.info("Result: {}".format(result.stdout))
    logger.debug("Code linux command: {}".format(result.returncode))
    print("=" * 100)

    return result.returncode
