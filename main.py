import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from linkparser import get_message, get_link

from flask import Flask, request

app = Flask(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/classroom.announcements",
          "https://www.googleapis.com/auth/classroom.courses.readonly"]

COURSES_ID = {"Англ": "637129488148",
              "Математика": "635843353358",
              "Укр мова": "620960346914",
              "Физ-ра": "620485897294",
              "Дискретная математика": "620844311340",
              "История": "620797854331",
              "Физика": "620408593297",
              "Укр Лит": "544956500670"}


@app.route('/webhook', methods=['POST'])
def main():
    """Shows basic usage of the Classroom API.
  Prints the names of courses the user has access to.
  """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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

    message = get_message(COURSES_ID["Англ"], creds)
    print(message)
    link = get_link(message)
    print(link)


if __name__ == "__main__":
    main()
