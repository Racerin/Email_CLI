import smtplib
from email.mime.text import MIMEText
import os
from dataclasses import dataclass

from dotenv import load_dotenv

from PARAM import *


@dataclass
class Email:
    """ An object containing class information for sending email. """
    smtp_server = SMTP_SERVER
    smtp_port = SMTP_PORT
    smtp_username : str = None
    smtp_password : str = None
    email_from : str = None
    email_to : str = None
    email_subject : str = ""
    message = ""

    def get_env_variables(self):
        """ 
        Read environment variables (dotenv, env variables,) 
        to get values to populate object. 
        """
        # Load the dotenv file to environment variables
        load_dotenv()
        # Assign properties
        self.smtp_username = os.getenv("PYTHON_EMAIL_APP_USERNAME")
        self.smtp_password = os.getenv("PYTHON_EMAIL_APP_PASSWORD")
        self.email_from = os.getenv("PYTHON_EMAIL_APP_EMAIL_ADDRESS")
        milk = os.getenv("goatmilk")    # returns None?

    def __post_init__(self):
        """ Things to do after the object has been instantiated. """
        # Obdate object with configuration variables
        # Obdate object with environmental variables
        self.get_env_variables()

    def send_email__verification(self):
        """ A check to be done to determine if an email can be sent. """
        # Properties check
        if isinstance(self.smtp_username, str):pass
        else: raise AttributeError("Email username was not assigned.")
        if isinstance(self.smtp_password, str):pass
        else: raise AttributeError("Email password was not assigned.")
        if isinstance(self.email_from, str):pass
        else: raise AttributeError("Sender's email was not assigned.")
        if isinstance(self.email_to, str):pass
        else: raise AttributeError("Receiver's email was not assigned.")
        # Connection Check
        # Authentication check


    def send_email(self):
        # Verification
        self.send_email__verification()
        # Setup
        msg = MIMEText(self.message)
        msg['Subject'] = self.email_subject
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        debug_level = True
        mail = smtplib.SMTP(self.smtp_server, self.smtp_port)
        mail.set_debuglevel(debug_level)
        mail.starttls()
        # Login
        mail.login(self.smtp_username, self.smtp_password)
        # Send the email
        mail.sendmail(self.email_from, self.email_to, msg.as_string())
        mail.quit()


    def send_draft_email(self):
        """ Sends the email to the sender so that the sender can view the email. """
        self.email_to = self.email_from
        self.send_email()