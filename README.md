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

# CLI
python main.py --today_only: Scrap uniquement aujourd'hui
python main.py: Scrap hier et aujourd'hui

# Deployment

* sudo env VISUAL=vim crontab -e (au lieu de 'sudo crontab -e' car nano est l'editeur par defaut)
* on run avec sudo dans crontab donc on install les requirements.txt avec sudo
* attention a donner les bonnes autorisations au fichier logs.log (lecture & ecriture)
* ce n'est pas parce qu'on ecrit les commandes avec sudo qu'on est en root
* installer postfix
* log de cron: grep CRON /var/log/syslog

