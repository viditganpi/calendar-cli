from __future__ import print_function

import datetime
import os.path
from tabulate import tabulate

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Calendar():
    creds = None

    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']

    def login(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                #TODO: see if this can be replaced by own url
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def get_calendar(self, count_events):
        if self.creds == None:
            self.login()

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print(f'Getting the upcoming {count_events} events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=count_events, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            event_summaries = [["Start time", "End time", "Time Zone", "Details"]]
            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime')
                finish = event['end'].get('dateTime')
                zone = event['start'].get('timeZone')
                event_summaries.append([start, finish, zone, event['summary']])
            print(tabulate(event_summaries, headers="firstrow", tablefmt="rounded_grid"))

        except HttpError as error:
            print('An error occurred: %s' % error)

    def list_calendars(self):
        if self.creds == None:
            self.login()

        try:
            service = build('calendar', 'v3', credentials=self.creds)
            calendar_results = service.calendarList().list().execute()
            calendars = calendar_results.get('items', [])

            if not calendars:
                print("No calendars found")
                return
            
            calendar_headers = ["Id", "Summary", "Timezone"]
            calendar_list = [calendar_headers]
            for calendar in calendars:
                id = calendar.get("id", "")
                summary = calendar.get("summary", "")
                timezone = calendar.get("timeZone", "")
                calendar_list.append([id, summary, timezone])
            print(tabulate(calendar_list, headers="firstrow", tablefmt="rounded_grid"))
        
        except HttpError as error:
            print("An error occured while fetching calendars: %s" % error)

