#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Remy Adda & Arie Bonan
# Created Date: 2023
# =============================================================================
# Utils functions
# =============================================================================


from logging.handlers import RotatingFileHandler
import logging
import requests

logger = logging.getLogger(__name__)


def setup_logging(logger):
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    if not file_handlers:
        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


def define_curl_command(final_cookies, review_id, restaurant_id, comments, reviewer_id, coupon_):
    comments = comments.replace("'", "\\'").replace("\\n", " ").replace("\n\n", " ").replace("\n", " ")
    curl_get_reviews = ["""curl 'https://merchants.ubereats.com/manager/graphql' \ """,
                        """  -H 'authority: merchants.ubereats.com' \ """,
                        """  -H 'accept: */*' \ """,
                        """  -H 'accept-language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7' \ """,
                        """  -H 'content-type: application/json' \ """,
                        """  -H 'cookie: {}' \ """.format(final_cookies),
                        """  -H 'origin: https://merchants.ubereats.com' \ """,
                        """  -H 'referer: https://merchants.ubereats.com/manager/home/59ea8c82-e76e-571f-9d3d-ff8ddf6d7639/feedback/reviews/010dad85-aab4-4de7-9f17-c33e60cb8740?start=2023-05-24&end=2023-05-24' \ """,
                        """  -H 'sec-ch-ua: "Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"' \ """,
                        """  -H 'sec-ch-ua-mobile: ?0' \ """,
                        """  -H 'sec-ch-ua-platform: "macOS"' \ """,
                        """  -H 'sec-fetch-dest: empty' \ """,
                        """  -H 'sec-fetch-mode: cors' \ """,
                        """  -H 'sec-fetch-site: same-origin' \ """,
                        """  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36' \ """,
                        """  -H 'x-csrf-token: x' \ """,
                        r"""  --data-raw $'{"operationName":"SubmitReply","variables":{"workflowUUID":""" + review_id + r""","restaurantUUID":""" + restaurant_id + r""","comment":""" + comments + r""","promotionValue":""" + coupon_ + r""","eaterUUID":""" + reviewer_id + r""","appVariant":"UBEREATS"},"query":"mutation SubmitReply($workflowUUID: String\u0021, $restaurantUUID: String\u0021, $comment: String\u0021, $promotionValue: PromotionValue, $eaterUUID: String\u0021, $appVariant: String\u0021) {\\n  submitEaterReviewReply(\\n    reply: {workflowUUID: $workflowUUID, restaurantUUID: $restaurantUUID, comment: $comment, promotionValue: $promotionValue, eaterUUID: $eaterUUID, appVariant: $appVariant}\\n  ) {\\n    uuid\\n    userUUID\\n    timestamp\\n    comment\\n    promotion {\\n      uuid\\n      flatValue\\n      formattedValue\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n"}' \ """,
                        """  --compressed """]
    return curl_get_reviews

