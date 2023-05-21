# Fullwhere

### Booking Scrapping

Voir Confluence pr les details de ce projet


### Uber eat scrapping

airtable_api.py: functions related to airtable (insert new data, scrap all bases, tickets, stores ids, restaurants and records ids)
utils.py: some utils functions (curl command)
scrap.py: functions related to UberEats scrapping (retrieve reviews)
main.py: full pipeline:
    - retrieve all restaurants ids
    - scrap all the reviews for all the restaurants
    - insert all the reviews into airtable
