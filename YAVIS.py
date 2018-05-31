from googleapiclient.discovery import build

import YAVIS_GUI
import os
import wave
import httplib2
import pyaudio

from os.path import join, dirname
from apiclient import discovery
from clint.textui import colored
from oauth2client import client, file
from oauth2client import tools
from watson_developer_cloud import AssistantV1
from watson_developer_cloud import TextToSpeechV1

import YAVIS_Calendar_Operations

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

try:
    import Tkinter
except ImportError:
    import tkinter

try:
    import ttk

    py3 = 0
except ImportError:
    import tkinter.ttk as ttk

    py3 = 1

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'YAVIS'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(httplib2.Http()))
    return creds


#########################
# message
#########################

watson_assistant = AssistantV1(
    url="https://gateway.watsonplatform.net/assistant/api",
    version='2018-02-16',
    username='7c7bc045-8fe0-4faf-b1c1-3dcaeb175eff',
    password='gbgOKu5nB7tN'
)

text_to_speech = TextToSpeechV1(
    username="a93ee1bd-f4b8-40ac-81f5-59b3b8e886b2",
    password="xPWlrJIepHYs")

num_of_events = 5


def voice(file_name):
    chunk = 1024
    # open a wav format music
    f = wave.open(file_name, "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)

    # read data (based on the chunk size)
    data = f.readframes(chunk)

    # play stream (looping from beginning of file to the end)
    while len(data) != 0:
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = f.readframes(chunk)

    # cleanup stuff.
    stream.close()
    p.terminate()


def text_to_speech_implementation(response):
    with open(join(dirname(__file__), 'output.wav'),
              'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(response, accept='audio/wav',
                                      voice="en-US_AllisonVoice").content)

    voice('output.wav')
    os.remove('output.wav')


def send_to_watson(data, context1):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    workspace_id = '087a5122-6020-4ebc-afa1-3445003d2c26'

    stop = False

    while not stop:
        calendar_response = ""

        # noinspection PyTypeChecker
        response = watson_assistant.message(workspace_id=workspace_id, input={'text': str(data)}, context=context1)
        # print(response)

        # Display to GUI
        watson_response = response['output']['text'][0]

        if (response['output']['nodes_visited'][0] == "Calendar_Entry_add_time"
                or response['output']['nodes_visited'][0] == "Calendar_Entry_add_date_time"
                or response['output']['nodes_visited'][0] == "Calendar_Entry_add_date"):
            response['context']['add'] = True

        for entity in response['entities']:
            if entity['entity'] == 'sys-date':
                response['context']['date'] = entity['value']
            if entity['entity'] == 'sys-time':
                response['context']['time'] = entity['value']
            if entity['entity'] == 'events':
                response['context']['event'] = response['input']['text']

        if response['output']['nodes_visited'][0] == "Calendar_Entry_add_All":
            date, time, title = YAVIS_Calendar_Operations.calendar_all(response)
            response['context']['add'] = True
            response['context']['date'] = date
            response['context']['time'] = time
            response['context']['event'] = title

        if response['intents']:
            if response['intents'][0]['intent'] == 'GoodBye':
                stop = True

        if response['intents']:
            if response['intents'][0]['intent'] == "Thank_You":
                response['context']['thank_count'] += 1

                # Google Calendar Add
        if (response['context']['date'] and response['context']['time'] and
                response['context']['event'] and response['context']['add']):
            YAVIS_Calendar_Operations.calender_google_add(response['context']['date'], response['context']['time'],
                                                          response['context']['event'],
                                                          service)
            response['context']['date'] = ""
            response['context']['time'] = ""
            response['context']['event'] = ""
            response['context']['add'] = ""

        # Search
        if response['output']['nodes_visited'][0] == "Calendar_search_events":
            d, t, time_interval, day_interval = YAVIS_Calendar_Operations.calendar_search(response)
            response['context']['date'] = d
            response['context']['time'] = t
            response['context']['time_interval'] = time_interval
            response['context']['day_interval'] = day_interval
            response['context']['search'] = True

        if response['output']['nodes_visited'][0] == "Calendar_next_events":
            d, t, num_of_events = YAVIS_Calendar_Operations.calendar_next(response)
            response['context']['date'] = d
            response['context']['time'] = t
            response['context']['number_of_events'] = num_of_events
            response['context']['next'] = True

            # Google Calendar Next Events
        if (response['context']['date'] and response['context']['time']
                and response['context']['next']):
            calendar_response = YAVIS_Calendar_Operations.calendar_google_next(response['context']['date'],
                                                                               response['context']['time'],
                                                                               response['context'][
                                                                                       'number_of_events'], service)
            response['context']['date'] = ""
            response['context']['time'] = ""
            response['context']['number_of_events'] = 10
            response['context']['next'] = False

        # Google Calendar Search Events

        if response['context']['search']:
            calendar_response = YAVIS_Calendar_Operations.calendar_google_search(response['context']['date']
                                                                                 , response['context']['time']
                                                                                 , response['context'][
                                                                                         'time_interval']
                                                                                 , response['context'][
                                                                                         'day_interval'], service)

            response['context']['date'] = ""
            response['context']['time'] = ""
            response['context']['time_interval'] = ""
            response['context']['day_interval'] = ""
            response['context']['search'] = False
        print(watson_response + "\n" + " " + calendar_response + "***************")
        text_to_speech_implementation(watson_response)
        if calendar_response:
            text_to_speech_implementation(calendar_response)

        response_to_send = watson_response + "\n" + calendar_response
        print("Response to Send: ")
        context1 = response['context']
        calendar_response = ""
        return response_to_send, context1


def button__click(event=None):
    global yavis_active
    global context
    global new_context

    data = gui_object.Entry1.get()
    print(data)

    # print(yavis_active)
    if data is not "":
        if yavis_active is False:
            print(colored.red("Me: "))
            gui_object.scr49.insert(tkinter.INSERT, colored.red('Me: ') + data + "\n")
            gui_object.scr49.insert(tkinter.INSERT, "\n")
            yavis_active = True
            response, new_context = send_to_watson(data, context)
            print(response)
            gui_object.scr49.insert(tkinter.INSERT, "YAVIS: " + response + "\n")
            gui_object.scr49.insert(tkinter.INSERT, "\n")
        else:
            gui_object.scr49.insert(tkinter.INSERT, "Me: " + data + "\n")
            gui_object.scr49.insert(tkinter.INSERT, "\n")
            response, new_context = send_to_watson(data, new_context)
            print(response)
            gui_object.scr49.insert(tkinter.INSERT, "YAVIS: " + response + "\n")
            gui_object.scr49.insert(tkinter.INSERT, "\n")
    gui_object.Entry1.delete(0, 'end')

    if str(data).__contains__("Bye"):
        exit(0)
    # gui_object.scr49.insert(INSERT,"\n")

    tkinter.sys.stdout.flush()


def init(top, gui, *args, **kwargs):
    global w, top_level, root, gui_object, yavis_active, context, new_context
    w = gui
    top_level = top
    root = top
    gui_object = YAVIS_GUI.Container(top_level)
    yavis_active = False
    context = {"timezone": "America/New_York",
               "thank_count": 1,
               "date": "",
               "time": "",
               "event": "",
               "search": False,
               "add": False,
               "next": False,
               "number_of_events": 10,
               "time_interval": "",
               "day_interval": ""
               }
    new_context = {}


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


if __name__ == '__main__':
    YAVIS_GUI.vp_start_gui()
