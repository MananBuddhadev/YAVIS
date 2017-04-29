YAVIS 
Your personal assistant made in Python programming language with the help of Watson Conversation API and Google Calendar API


Authors:
Nihar Vanjara (niv1676@rit.edu)
Atir Petkar (ap8185@g.rit.edu)
Manan Buddhadev (mcb5345@rit.edu)


Installation:


To run YAVIS, you need following dependencies

* Python
     	Install latest version of python3 from https://www.python.org/downloads/

* watson-developer-cloud
	Install using pip or easy_install,
		$ pip install --upgrade watson-developer-cloud
		$ easy_install --upgrade watson-developer-cloud
 
* google-api-python-client
	Install using pip or easy_install,
		$ pip install --upgrade google-api-python-client
        	$ easy_install --upgrade google-api-python-client

* pyaudio
	Install using pip,
        	$ pip install pyaudio

In case you want to run for your google account, follow the google calendar api quickstart for Python instructions on  
https://developers.google.com/google-apps/calendar/quickstart/python

Running the project
To run, use the Python file  YAVIS_GUI_support.py in your terminal using following command in the project folder
$python3 YAVIS_GUI_support.py

Once you run the above mentioned command the user interface for YAVIS will start running. Once the UI is running you can type in any command you want to execute. 
For example try giving YAVIS the command : "Set an event for tomorrow", following which YAVIS is ask,"What should be the event's name?" respond with an event 
you want to setup like, "Appointment with academic advisor". The follow-up question, "What time should I set for this event" and you should specify the time of 
the event say 8pm and finally YAVIS would give you a confirmation message saying: "The event has been added to the calendar."

Other than the command mentioned above there are various other ways to give a command to YAVIS which are:
* Set an appointment with ABC on Sunday at 2 pm
* Set a meeting with ABC on 30th May at 8 pm
* Set reminder for Quiz next week at 1 pm
* Show me events for tomorrow
* Show events on Monday morning
* Show upcoming events
