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

logger = logging.getLogger(__name__)


def setup_logging(logger):
    logger.setLevel(logging.DEBUG)
    file_handler = logging.handlers.RotatingFileHandler('logs.log', maxBytes=1048576, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def define_curl_command(uuid_list, year, month, day):
    curl_get_reviews = ["""curl 'https://merchants.ubereats.com/manager/graphql' \ """, """  -H 'authority: merchants.ubereats.com' \ """,
                        """  -H 'accept: */*' \ """, """  -H 'accept-language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7' \ """,
                        """  -H 'content-type: application/json' \ """, """  -H 'cookie: {}' \ """,
                        """  -H 'origin: https://merchants.ubereats.com' \ """,
                        """  -H 'referer: https://merchants.ubereats.com/manager/home/00f1d562-41ef-4749-8017-ca261d3d53a0/feedback/reviews' \ """,
                        """  -H 'sec-ch-ua: "Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"' \ """,
                        """  -H 'sec-ch-ua-mobile: ?0' \ """, """  -H 'sec-ch-ua-platform: "macOS"' \ """,
                        """  -H 'sec-fetch-dest: empty' \ """, """  -H 'sec-fetch-mode: cors' \ """,
                        """  -H 'sec-fetch-site: same-origin' \ """,
                        """  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36' \ """,
                        """  -H 'x-csrf-token: x' \ """,
                        r"""  --data-raw $'{"operationName":"EaterReviews","variables":{"restaurantUUIDs":""" + str(uuid_list).replace("'", '"').replace(" ", "")  + r""","lastTimestamp":null,"lastWorkflowUUID":null,"filters":{"starRating":null,"tagsValue":null,"dateRange":{"start":""" + """ "{}-{}-{}" """.format(year, month, day) + r""" ,"end":"{}-{}-{}" """.format(year, month, day) + r"""}},"limit":50},"query":"fragment eaterReview on EaterReview {\\n  uuid\\n  timestamp\\n  rating\\n  comment\\n  tags\\n  menuItemReviews {\\n    id\\n    rating\\n    name\\n    comment\\n    tags\\n    __typename\\n  }\\n  eater {\\n    uuid\\n    name\\n    profileURL\\n    __typename\\n  }\\n  eaterTotalOrders\\n  order {\\n    workflowUUID\\n    deliveredAt\\n    orderTotal\\n    currencyCode\\n    appVariant\\n    restaurant {\\n      uuid\\n      name\\n      __typename\\n    }\\n    __typename\\n  }\\n  isReplyScheduled\\n  reply {\\n    uuid\\n    promotion {\\n      uuid\\n      flatValue\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\\n\\nquery EaterReviews($restaurantUUIDs: [ID\u0021]\u0021, $limit: Int, $lastTimestamp: String, $lastWorkflowUUID: String, $filters: EaterReviewFilterInput) {\\n  eaterReviews(\\n    restaurantUUIDs: $restaurantUUIDs\\n    limit: $limit\\n    lastTimestamp: $lastTimestamp\\n    lastWorkflowUUID: $lastWorkflowUUID\\n    filters: $filters\\n  ) {\\n    ...eaterReview\\n    __typename\\n  }\\n}\\n"}' \ """,
                        """  --compressed """]
    return curl_get_reviews