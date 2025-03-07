from datetime import datetime, timedelta
from pytz import timezone
import os
import webbrowser
from flask import Flask, request, jsonify
import pyperclip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CREDENTIALS_FILE = 'credentials.json'

app = Flask(__name__)

# Funcția care creează Google Meet
def create_google_meet(meeting_datetime, emails=[]):
    creds = None
    # Verificăm dacă există un token valid
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Setăm data și ora pentru întâlnire
    start_time = meeting_datetime.isoformat()
    end_time = (meeting_datetime + timedelta(hours=1)).isoformat()

    # Creare întâlnire Meet
    event = {
        'summary': 'Google Meet Instant Meeting',
        'conferenceData': {
            'createRequest': {
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                'requestId': 'randomString'
            }
        },
        'start': {
            'dateTime': start_time,
            'timeZone': 'Europe/Bucharest',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Europe/Bucharest',
        },
        'attendees': [{'email': email} for email in emails],
        'conferenceDataVersion': 1,
    }

    event_result = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()

    meet_link = event_result['hangoutLink']
    return meet_link  # returnează link-ul de Google Meet


# Endpoint-ul POST pentru a crea întâlnirea
@app.route('/create_meeting', methods=['POST'])
def create_meeting():
    try:
        # Obținem datele din request-ul POST
        data = request.get_json()
        emails = data.get('emails', [])
        meeting_datetime_str = data.get('datetime', None)
        to_verify = True
        if meeting_datetime_str:
            # Dacă este specificată o dată, o convertim într-un obiect datetime
            meeting_datetime = datetime.strptime(meeting_datetime_str, '%Y-%m-%dT%H:%M:%S')
        else:
            to_verify = False
            meeting_datetime = datetime.now()

        # Creăm întâlnire
        meet_link = create_google_meet(meeting_datetime, emails)

        if (to_verify == False):
            webbrowser.open(meet_link)

        return jsonify({'meet_link': meet_link}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
