import base64

import config
import urlfetch


def send_sms(phone_number, message):
    payload = {
        "To": phone_number,
        "From": "+13067003369",
        "Body": message
    }

    user_info = config.twilio_user_info

    headers = {'Authorization':
                   'Basic %s' % base64.b64encode(user_info)}

    url = 'https://api.twilio.com/2010-04-01/Accounts/AC5dfaee46edd4a7c6d96e3de93cf0010e/Messages.json'

    res2 = urlfetch.fetch(
        url,
        headers=headers,
        method='POST',
        data=payload
    )

    if res2.status_code < 400:
        return True
    else:
        return False
