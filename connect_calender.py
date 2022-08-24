from datetime import date, timedelta
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scope, delete the file token.pickle
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDER_ID = os.environ['CALENDER_ID']

def get_calender_events(start:date, end:date, count:int = 7):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens,
    # and is created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        time_max = f'{end.isoformat()}T00:00:00.000Z'
        time_now = f'{start.isoformat()}T00:00:00.000Z'

        # 今日から1ヶ月後までのイベントを取得する
        response = service.events().list(
            calendarId=CALENDER_ID,
            timeMin=time_now,
            timeMax=time_max,
            maxResults=count,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = response['items']
        sorted_events = []
        for event in events:
            start = event['start']['dateTime'] if 'dateTime' in event['start'].keys() \
                else event['start']['date']
            end = event['end']['dateTime'] if 'dateTime' in event['end'].keys() \
                else event['end']['date']
            sorted_events.append([event['summary'], start.split('T'), end.split('T')])
        sorted_events = sorted(sorted_events, key=lambda x: x[1])

        return [
            sorted_events
        ]
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    # 1週間の予定を取得するサンプル
    today = date.today()
    one_month_after = today + timedelta(days=7)
    result = get_calender_events(start=today, end=one_month_after, count=10)
    print(result)
