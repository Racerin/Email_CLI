import smtplib
from email.mime.text import MIMEText
import os
from dataclasses import dataclass

from dotenv import load_dotenv

import configparser
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

    def get_config(self):
        """ Read config.ini file and get config values. """
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_NAME)
        try:
            dict1 = config['DEFAULT']
            if dict1.get('PYTHON_EMAIL_APP_USERNAME'):
                self.smtp_username = dict1.get('PYTHON_EMAIL_APP_USERNAME', self.smtp_username)
            if dict1.get('PYTHON_EMAIL_APP_EMAIL_ADDRESS'):
                self.email_from = dict1.get('PYTHON_EMAIL_APP_EMAIL_ADDRESS', self.email_from)
            if dict1.get('PYTHON_EMAIL_APP_SERVER'):
                self.smtp_server = dict1.get('PYTHON_EMAIL_APP_SERVER', self.smtp_server)
            if dict1.get('PYTHON_EMAIL_APP_PORT'):
                self.smtp_port = dict1.get('PYTHON_EMAIL_APP_PORT', self.smtp_port)
            if dict1.get('PYTHON_EMAIL_APP_PASSWORD'):
                self.smtp_password = dict1.get('PYTHON_EMAIL_APP_PASSWORD', self.smtp_password)
            if dict1.get('PYTHON_EMAIL_APP_RECEIVING_EMAIL'):
                self.email_to = dict1.get('PYTHON_EMAIL_APP_RECEIVING_EMAIL', self.email_to)
            if dict1.get('PYTHON_EMAIL_APP_SUBJECT'):
                self.email_subject = dict1.get('PYTHON_EMAIL_APP_SUBJECT', self.email_subject)
        except AttributeError as e:
            print("Error in accessing config file information.", e)

    def get_env_variables(self):
        """ 
        Read environment variables (dotenv, env variables,) 
        to get values to populate object. 
        """
        # Load the dotenv file to environment variables
        load_dotenv()
        # Assign properties
        if os.getenv("PYTHON_EMAIL_APP_USERNAME"):
            self.smtp_username = os.getenv("PYTHON_EMAIL_APP_USERNAME")
        if os.getenv("PYTHON_EMAIL_APP_PASSWORD"):
            self.smtp_password = os.getenv("PYTHON_EMAIL_APP_PASSWORD")
        if os.getenv("PYTHON_EMAIL_APP_EMAIL_ADDRESS"):
            self.email_from = os.getenv("PYTHON_EMAIL_APP_EMAIL_ADDRESS")
        if os.getenv("PYTHON_EMAIL_APP_RECEIVING_EMAIL"):
            self.email_to = os.getenv("PYTHON_EMAIL_APP_RECEIVING_EMAIL")
        if os.getenv("PYTHON_EMAIL_APP_PORT"):
            self.smtp_port = os.getenv("PYTHON_EMAIL_APP_PORT")
        if os.getenv("PYTHON_EMAIL_APP_SERVER"):
            self.smtp_server = os.getenv("PYTHON_EMAIL_APP_SERVER")
        if os.getenv("PYTHON_EMAIL_APP_SUBJECT"):
            self.subject = os.getenv("PYTHON_EMAIL_APP_SUBJECT")

    def __post_init__(self):
        """ Things to do after the object has been instantiated. """
        # Obdate object with configuration variables
        self.get_config()
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
        print(self)
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