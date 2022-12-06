from http import client
from django.conf import settings
from twilio.rest import Client
import random

ACCOUNT_SID='AC840de5535c88dd8135a4ea25c726f14c'
AUTH_TOKEN='596d81a61c974a357963d65e8861e6e7'

class MessageHandler:
    phone_number=None
    otp=None
    
    def __init__(self,phone_number,otp) :
        self.phone_number=phone_number
        self.otp=otp
    def send_otp_on_phone(self):  
        
        client =Client(ACCOUNT_SID,AUTH_TOKEN)

        message=client.messages \
            .create(
                body=f'Your Otp is{self.otp}',
                from_='+13143507005',
                to=self.phone_number
                            )
    # def send_otp_via_whatsapp(self):     
    #     client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
    #     message=client.messages.create(body=f'your otp is:{self.otp}',from_=f'{settings.TWILIO_WHATSAPP_NUMBER}',to=f'whatsapp:{settings.COUNTRY_CODE}{self.phone_number}')