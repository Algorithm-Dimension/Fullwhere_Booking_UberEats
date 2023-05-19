from airtable import Airtable
import requests
import pandas as pd

AIRTABLE_API_KEY = 'pat0HdLihEwG7kT9n.bfa0cee24f25c4a2e23fcc3c7d4bfc498533c6b67bd8cb4c2ca9e897b0a7c4ae'


def airtable_access_specific_base_and_table(AIRTABLE_BASE_ID, AIRTABLE_STORE_ID):
    """

    :param AIRTABLE_BASE_ID: ID database dans airtable (BASE ID column)
    :param AIRTABLE_STORE_ID: Id de la table (store)
    :return: connexion
    """
    print("Connection to base: {} - table: {}".format(AIRTABLE_BASE_ID, AIRTABLE_STORE_ID))
    airtable_connexion = Airtable(AIRTABLE_BASE_ID, AIRTABLE_STORE_ID, AIRTABLE_API_KEY)
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
        print("Total elements in bases_id list: {}".format(len(bases_id)))
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
            #print("missing uuid in base: {} and table {}".format(base_id, store_id))
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


def retrieve_all_uuids_and_records_ids():
    # 1 - Retrieve Bases & Tables Ids
    bases_id, tickets_id, stores_id = retrieve_bases_tickets_stores_id()
    #bases_id, tickets_id, stores_id = bases_id[5:8], tickets_id[5:8], stores_id[5:8]

    all_uuids = []
    all_records_ids = []

    print("Scrapping of all restaurants uuids and records ids by base and store")
    print(100*"=")

    for base_id, store_id in zip(bases_id, stores_id):
        airtable_con = airtable_access_specific_base_and_table(base_id, store_id)
        uuids_by_base_and_store, record_id_by_base_and_store = retrieve_uuid(airtable_con,
                                                                             base_id, store_id, max_records=None)
        all_uuids.append(uuids_by_base_and_store)
        all_records_ids.append(record_id_by_base_and_store)

    print("Total uuids (sublists) for all bases and stores: {}".format(len(all_uuids)))
    print("Total records ids (sublists) for all bases and stores: {}".format(len(all_records_ids)))

    return all_uuids, all_records_ids, bases_id, tickets_id, stores_id







#new_record = {
#    'Name': 'John Doe',
#    'Email': 'johndoe@example.com',
#    'Phone': '+1234567890'
#}
#created_record = airtable.insert(new_record)
#print('Created record:', created_record['fields'])

# Example of updating an existing record
#record_id_to_update = 'RECORD_ID_TO_UPDATE'
#updated_record = airtable.update(record_id_to_update, {'Email': 'newemail@example.com'})
#print('Updated record:', updated_record['fields'])

# Example of deleting a record
#record_id_to_delete = 'RECORD_ID_TO_DELETE'
#deleted_record = airtable.delete(record_id_to_delete)
#print('Deleted record:', deleted_record['fields'])

