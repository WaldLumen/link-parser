import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from linkparser import get_message, get_link, get_all_links, get_update

import logging

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/classroom.announcements",
          "https://www.googleapis.com/auth/classroom.courses.readonly"]


links = []
links_new = []

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO)
def main():
    """Shows basic usage of the Classroom API.
  Prints the names of courses the user has access to.
  """
    logging.info('Getting creds')
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        logging.info("Creds loaded from previous session")
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
        logging.info("Creds created")
    get_all_links(creds, links)

    while True:
        get_all_links(creds, links_new)
        get_update(links, links_new)


if __name__ == "__main__":
    logging.info('The script is running')
    main()
