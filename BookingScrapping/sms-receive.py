from flask import Flask, request
from pprint import pprint
app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    if request.is_json:
        pprint(request.get_json())
        data = request.get_json()
    else:
        data = dict(request.form) or dict(request.args)
        pprint(data)
    return str(data)


if __name__ == "__main__":
    # OUVRIR GOOGLE CHROME (HIDDEN)
    # ALLER SUR ADMIN.BOOKING.COM
    # ENTRER LES CREDENTIALS  + DEMANDE D'ENVOI D'SMS
    app.run(debug=True)
    # LANCER SUR NGROK



    # Start our TwiML response
    # resp = MessagingResponse()

    # Add a message
    # resp.message("Thanks Booking")

    # return str(resp)