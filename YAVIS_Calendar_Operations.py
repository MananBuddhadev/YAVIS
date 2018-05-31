import datetime
import os
import time
# noinspection PyCompatibility
import tkinter

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import timedelta, datetime

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
#
# SCOPES = 'https://www.googleapis.com/auth/calendar'
# CLIENT_SECRET_FILE = 'client_id.json'
# APPLICATION_NAME = 'Google Calendar API Python Quickstart'
#
# def get_credentials():
#     """Gets valid user credentials from storage.
#     If nothing has been stored, or if the stored credentials are invalid,
#     the OAuth2 flow is completed to obtain the new credentials.
#     Returns:
#         Credentials, the obtained credential.
#     """
#     home_dir = os.path.expanduser('~')
#     credential_dir = os.path.join(home_dir, '.credentials')
#     if not os.path.exists(credential_dir):
#         os.makedirs(credential_dir)
#     credential_path = os.path.join(credential_dir,
#                                    'calendar-python-quickstart.json')
#
#     store = Storage(credential_path)
#     credentials = store.get()
#     if not credentials or credentials.invalid:
#         flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
#         flow.user_agent = APPLICATION_NAME
#         if flags:
#             credentials = tools.run_flow(flow, store, flags)
#     return credentials


def calender_google_add(date, time, event, service):
    print("Date: ", date)
    print("Time: ", time)
    print("Event: ", event)
    dt = datetime.strptime(date + "T" + time, "%Y-%m-%dT%H:%M:%S")
    dt = dt + timedelta(hours=1)
    event = {
        'summary': event,
        'start': {
            'dateTime': date + 'T' + time + '-04:00',
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': str(dt).replace(' ', 'T') + '-04:00',
            'timeZone': 'America/New_York',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()


def calendar_all(response):
    title = None
    for entity in response['entities']:

        if entity['entity'] == 'sys-date':
            date = entity['value']
        if entity['entity'] == 'sys-time':
            time = entity['value']
        if entity['entity'] == 'events':
            title = entity['value']

    expression = tkinter.re.findall(r'"([^"]*)"', response['input']['text'])

    if expression:
        title = expression[0]

    return date, time, title


def calendar_search(response):
    now = datetime.now()
    d = str(now)[:10]
    t = "00:00:00"
    day_interval = None
    time_interval = None
    for entity in response['entities']:

        if entity['entity'] == 'Time_periods':
            time_interval = entity['value']
        if entity['entity'] == 'sys-time':
            t = entity['value']
        if entity['entity'] == 'sys-date':
            d = entity['value']
        if entity['entity'] == 'Time_periods':
            time_interval = entity['value']
        if entity['entity'] == 'Day_Periods':
            day_interval = entity['value']

    return d, t, time_interval, day_interval


def calendar_google_search(date, t, time_interval, day_interval, service):
    response = ""

    if day_interval is None and time_interval is None:

        events_result = service.events().list(
                        calendarId='primary', timeMin=date + "T" + t + "-04:00",
                        timeMax=str(datetime.strptime(date + 'T' + t, "%Y-%m-%dT%H:%M:%S") + timedelta(hours=24)).
                                    replace(' ', 'T') + "-04:00",
                                    singleEvents=True,
                                    orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            response = 'You do not have events'
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            ts = time.strptime(start[:19], "%Y-%m-%dT%H:%M:%S")
            response = response + "on " + time.strftime("%d %b,%Y at %I:%M %p,", ts) + "you have" + "\"" + event[
                'summary'] + "\"\n"

    # show me tomorrow morning events
    elif day_interval == "morning":
        time_max = date + "T12:00:00-04:00"
        events_result = service.events().list(
            calendarId='primary', timeMin=date + "T" + "07:00:00-04:00",
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            response = 'You do not have events'
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            ts = time.strptime(start[:19], "%Y-%m-%dT%H:%M:%S")
            response = response + "on " + time.strftime("%d %b,%Y at %I:%M %p,", ts) + "you have" + "\"" + event[
                'summary'] + "\"\n"

    # show me tomorrow afternoon events
    elif day_interval == "afternoon":
        time_max = date + "T18:00:00-04:00"
        events_result = service.events().list(
            calendarId='primary', timeMin=date + "T" + "12:00:00-04:00",
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            response = 'You do not have events'

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            ts = time.strptime(start[:19], "%Y-%m-%dT%H:%M:%S")
            response = response + "on " + time.strftime("%d %b,%Y at %I:%M %p,", ts) + "you have" + "\"" + event[
                'summary'] + "\"\n"


    # show me tomorrow evening events
    elif day_interval == "evening":
        time_max = date + "T23:59:59-04:00"
        events_result = service.events().list(
                                        calendarId='primary', timeMin=date + "T" + "18:00:00-04:00",
                                        timeMax=time_max,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            response = 'You do not have events'

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            ts = time.strptime(start[:19], "%Y-%m-%dT%H:%M:%S")
            response = response + "on " + time.strftime("%d %b,%Y at %I:%M %p,", ts) + "you have" + "\"" + event[
                'summary'] + "\"\n"


    # show me events after 5 pm --> dayinterval = none and time_period=after
    elif time_interval == 'after':
        time_max = date + "T23:59:59-04:00"
        events_result = service.events().list(
            calendarId='primary', timeMin=date + "T" + t + "-04:00",
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            response = 'You do not have events'

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            ts = time.strptime(start[:19], "%Y-%m-%dT%H:%M:%S")
            response = response + "on " + time.strftime("%d %b,%Y at %I:%M %p,", ts) + "you have" + "\"" + event[
                'summary'] + "\"\n"


    elif time_interval == 'at':
        # time_max = date + "T23:59:59-04:00"
        events_result = service.events().list(
            calendarId='primary', timeMin=date + "T" + t + "-04:00",
            maxResults=1,
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            response = 'You do not have events'

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            ts = time.strptime(start[:19], "%Y-%m-%dT%H:%M:%S")
            response = response + "on " + time.strftime("%d %b,%Y at %I:%M %p,", ts) + "you have" + "\"" + event[
                'summary'] + "\"\n"


    # show me events after 5 pm --> dayinterval = none and time_period=after
    elif time_interval == 'before':
        time_min = date + "T00:00:00-04:00"
        events_result = service.events().list(
            calendarId='primary', timeMin=time_min,
            timeMax=date + "T" + t + "-04:00",
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            response = 'You do not have events'

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            ts = time.strptime(start[:19], "%Y-%m-%dT%H:%M:%S")
            response = response + "on " + time.strftime("%d %b,%Y at %I:%M %p,", ts) + "you have" + "\"" + event[
                'summary'] + "\"\n"
    return response


def calendar_next(response):
    num_of_events = 5
    now = datetime.now()
    date = str(now)[:10]
    time = str(now)[11:19]

    for entity in response['entities']:

        if entity['entity'] == 'sys-number':
            num_of_events = entity['value']

    return date, time, num_of_events


def calendar_google_next(date, t, num_of_events, service):
    calendar_response = ''
    events_result = service.events().list(
        calendarId='primary', timeMin=date + "T" + t + "-04:00", maxResults=num_of_events, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        calendar_response = 'No upcoming events found.'

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        ts = time.strptime(start[:19], "%Y-%m-%dT%H:%M:%S")
        calendar_response = calendar_response + "on " + time.strftime("%d %b,%Y at %I:%M %p,", ts) + "you have" + "\"" + \
                            event['summary'] + "\""
        calendar_response = calendar_response + "\n"

    return calendar_response
