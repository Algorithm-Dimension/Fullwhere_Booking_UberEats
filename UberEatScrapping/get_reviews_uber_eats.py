import subprocess
import os
import json
import logging
import traceback
import requests
import warnings

import airtable_api


logging.basicConfig(filename='log_ubereats_2MAI.txt', level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(lineno)d %(message)s')

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('log_ubereats_2MAI.txt')
logger.addHandler(file_handler)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)

logging.getLogger().addHandler(logging.NullHandler())

warnings.filterwarnings('ignore', category=UserWarning, append=True)



AIRTABLE_API_KEY = 'pat0HdLihEwG7kT9n.bfa0cee24f25c4a2e23fcc3c7d4bfc498533c6b67bd8cb4c2ca9e897b0a7c4ae'

# UUID_LIST = ["208d5aef-d809-4b0e-b06d-c70bc853d5b0", "9514659e-d353-408c-99c2-d7be771114d3",
#              "00f1d562-41ef-4749-8017-ca261d3d53a0", "434ad85d-0e2f-4442-88c3-f1154f8ea2d7",
#              "8d589eac-ce08-4dce-a7a9-79b3f9b776d7", "0b00b8b6-bbf2-494d-b50e-feedef92659a",
#              "afe55a32-aadf-4ad9-82cd-c43249023253"]

UUID_LIST, RECORDS_IDS_LIST, bases_id, tickets_id, stores_id = airtable_api.retrieve_all_uuids_and_records_ids()

#UUID_LIST = ["0b00b8b6-bbf2-494d-b50e-feedef92659a"]
#base_id = "app4sy6FFFwlcssKY"
#table_id = "tblgl57TfI3f9a90Q"
#ticket_id = "tblpCfgnHTYfUqonX"


YEAR = "2023"
MONTH = "05"
DAY = "03"

# TODO MATIN CHECK DE HIER ET AUJD, ET SOIR, CHECK DE AUJD AUJD


def define_curl_command(uuid_list, YEAR, MONTH, DAY):
    CURL_GET_REVIEWS = ["""curl 'https://merchants.ubereats.com/manager/graphql' \ """, """  -H 'authority: merchants.ubereats.com' \ """,
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
                        r"""  --data-raw $'{"operationName":"EaterReviews","variables":{"restaurantUUIDs":""" + str(uuid_list).replace("'", '"').replace(" ", "")  + r""","lastTimestamp":null,"lastWorkflowUUID":null,"filters":{"starRating":null,"tagsValue":null,"dateRange":{"start":""" + """ "{}-{}-{}" """.format(YEAR, MONTH, DAY) + r""" ,"end":"{}-{}-{}" """.format(YEAR, MONTH, DAY) + r"""}},"limit":50},"query":"fragment eaterReview on EaterReview {\\n  uuid\\n  timestamp\\n  rating\\n  comment\\n  tags\\n  menuItemReviews {\\n    id\\n    rating\\n    name\\n    comment\\n    tags\\n    __typename\\n  }\\n  eater {\\n    uuid\\n    name\\n    profileURL\\n    __typename\\n  }\\n  eaterTotalOrders\\n  order {\\n    workflowUUID\\n    deliveredAt\\n    orderTotal\\n    currencyCode\\n    appVariant\\n    restaurant {\\n      uuid\\n      name\\n      __typename\\n    }\\n    __typename\\n  }\\n  isReplyScheduled\\n  reply {\\n    uuid\\n    promotion {\\n      uuid\\n      flatValue\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\\n\\nquery EaterReviews($restaurantUUIDs: [ID\u0021]\u0021, $limit: Int, $lastTimestamp: String, $lastWorkflowUUID: String, $filters: EaterReviewFilterInput) {\\n  eaterReviews(\\n    restaurantUUIDs: $restaurantUUIDs\\n    limit: $limit\\n    lastTimestamp: $lastTimestamp\\n    lastWorkflowUUID: $lastWorkflowUUID\\n    filters: $filters\\n  ) {\\n    ...eaterReview\\n    __typename\\n  }\\n}\\n"}' \ """,
                        """  --compressed """]
    return CURL_GET_REVIEWS


current_dir = os.getcwd()
CURL_NAME = os.path.join(current_dir,"UberEatScrapping", "files", "script.sh")

#uuid_list = ["208d5aef-d809-4b0e-b06d-c70bc853d5b0", "9514659e-d353-408c-99c2-d7be771114d3",
#             "00f1d562-41ef-4749-8017-ca261d3d53a0", "434ad85d-0e2f-4442-88c3-f1154f8ea2d7",
#             "8d589eac-ce08-4dce-a7a9-79b3f9b776d7", "0b00b8b6-bbf2-494d-b50e-feedef92659a",
#             "afe55a32-aadf-4ad9-82cd-c43249023253"]


def check_if_review_exist(review_id, base_id, ticket_id):
    """

    """
    url = "https://api.airtable.com/v0/{}/{}?filterByFormula=" \
          "%7BReview+ID%7D%3D%22{}%22".format(base_id, ticket_id, review_id)
    logger.info(url)

    headers = {
        'Authorization': 'Bearer ' + AIRTABLE_API_KEY
    }
    response = requests.get(url, headers=headers)
    logger.info(response)
    logger.info(response.json())

    if response.status_code == 200:
        data = response.json()
        # if len == 0, it means that the request did not find this review id, so we can insert in Airtable
        if len(data["records"]) == 0:
            return False
        else:
            return True
    else:
        print("Request error to get the review_id: {}".format(review_id))
        return True


def replace_comments_by_tag_if_none(review):
    if review["tags"]:
        if not review["comment"]:
            review["comment"] = ', '.join(str(element) for element in review["tags"])
    return review


def reformat_review(review_):
    # First we replace comment by tag if tag not None and comment is None
    replace_comments_by_tag_if_none(review)
    output_ = dict()
    output_["Review ID"] = review_["uuid"]
    output_["Note"] = review_["rating"]
    output_["Review text"] = review_["comment"]
    output_["Number of orders"] = review_["eaterTotalOrders"]
    output_["Order amount"] = review_["order"]["orderTotal"]
    output_["Reviewer firstname"] = review_["eater"]["name"].split(" ")[0]
    output_['🏠 Stores'] = review_["order"]["restaurant"]["uuid"]
    output_["Review date"] = review_["timestamp"][:10]  # format_date = "YYYY-MM-DD"
    output_["Platform"] = "UberEATS"
    output_["Rating"] = review_["rating"]

    return output_


def scrap(uuid_list):
    logging.info("SCRAP BEGIN")
    with open(os.path.join(current_dir, "UberEatScrapping", "files", "cookies.txt"), "r") as file:
        cookies_final = file.read()

    # TODO RECUPERER UUID DE AIRTABLE
    # TODO BOUCLE TOUT LES UUID ET TOUT LES JOURS
    # TODO ITERATION AUTOUR DE LA DATE
    CURL_GET_REVIEWS = define_curl_command(uuid_list, YEAR, MONTH, DAY)
    CURL_GET_REVIEWS[5] = CURL_GET_REVIEWS[5].format(cookies_final)
    with open(CURL_NAME, "w") as file:
        for line_ in CURL_GET_REVIEWS:
            file.write(line_[:-1])
            if "compressed" in line_:
                continue
            file.write("\n")

    os.chmod(CURL_NAME, 0o755)
    result = subprocess.run(["bash", CURL_NAME], capture_output=True, text=True)
    reviews = json.loads(result.stdout)["data"]["eaterReviews"]

    # TODO INCLURE DANS AIRTABLE
    logging.info("SCRAP END LEN REVIEW IS {}".format(len(reviews)))

    return reviews


if __name__ == "__main__":
    # 1 - Retrieve reviews for sub list of uuids (for each sublist of uuid, is associated a sub list
    # of records id, a base id, a ticket id and a store id
    for sub_uuid_list, sub_record_id_list, base_id, \
            ticket_id, store_in in \
            zip(UUID_LIST, RECORDS_IDS_LIST, bases_id, tickets_id, stores_id):

        logger.info("Sub uuid list: {} - sub record id list: {} - base_id: {}"
                    " - ticket_id: {} - store_id: {}".format(sub_uuid_list, sub_record_id_list,
                                                             base_id, ticket_id, store_in))

        if len(sub_uuid_list) != 0:
            # We scrap each restaurant one by one (otherwise there are errors, we can not scrap a list of restau, values are wrong)
            for uuid, record_id in zip(sub_uuid_list, sub_record_id_list):
                logger.info("We scrap restaurant uuid: {}".format(uuid))
                logger.info("Record id: {}".format(record_id))
                try:
                    reviews = scrap([uuid])
                except:
                    traceback.print_exc()
                    reviews = None

                # 2 - Insert each review in airtable
                # We write in ticket id table
                if reviews is None:
                    logger.info("Error when scrapping sub_uuid_list: {} on {}/{}/{}".format(uuid, DAY, MONTH, YEAR))
                elif reviews and len(reviews) != 0:
                    logger.info("There are reviews for restaurants: {} on {}/{}/{}".format(uuid, DAY, MONTH, YEAR))
                    airtable_connexion = airtable_api.airtable_access_specific_base_and_table(base_id, ticket_id)

                    for review in reviews:
                        # Reformat review following Airtable format
                        new_record = reformat_review(review)
                        new_record['🏠 Stores'] = [record_id]
                        # Check if review_id exist
                        review_id = review["uuid"]
                        logger.info("Review id: {}".format(review_id))
                        review_id_exist = check_if_review_exist(review_id, base_id, ticket_id)
                        if not review_id_exist:
                            logger.info("Review id {} does not exist. Lets insert it".format(review_id))
                            airtable_api.create_new_record(airtable_connexion, new_record)
                        else:
                            logger.info("Review id {} already exist.".format(review_id))

                elif len(reviews) == 0:
                    logger.info("No reviews for {} on {}/{}/{}".format(uuid, DAY, MONTH, YEAR))
                else:
                    pass
    logger.info("End for {}/{}/{}".format(DAY, MONTH, YEAR))








