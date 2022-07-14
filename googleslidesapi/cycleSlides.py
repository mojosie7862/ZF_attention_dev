from __future__ import print_function

import os.path
import time
import threading
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations']

# The ID of a sample presentation.
PRESENTATION_ID = '1mUw4DA0VeIonuQ-5hi67aBrm40pu7drrIkKgJlnhJaQ'
toggle = 1
slide_ids = ["g13cbf6815b1_0_5","MyAwesomePage","g13cbf6815b1_0_10"]
def main():
    """Shows basic usage of the Slides API.
    Prints the number of slides and elments in a sample presentation.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        print("Started cycling through slides")
        #while True:
        def func():
            service = build('slides', 'v1', credentials=creds)

            presentation = service.presentations().get(
                presentationId=PRESENTATION_ID).execute()
            slides = presentation.get('slides')
        
            requests = [
                {
                    'updateSlidesPosition': {
                        "slideObjectIds": [
                            slide_ids[0]
                        
                        ],
                        "insertionIndex" : 3
                    }
                }
            
            ]
            slide_ids.append(slide_ids.pop(0))
                #       If you wish to populate the slide with elements,
                # add element create requests here, using the page_id.

                # Execute the request.
            body = {
                'requests': requests
            }
            response = service.presentations() \
                .batchUpdate(presentationId=PRESENTATION_ID, body=body).execute()
            updateslide_response = response.get('replies')[0].get('updateSlidePosition')

        def main_det():
            while(True):
                if(toggle == 1):
                    func()

                time.sleep(0.5)
        def tkinter_start():
            import tkinter
            import tkinter.messagebox as tkMessageBox

            top = tkinter.Tk()

            def action():
                global toggle
                toggle *= -1
                if(toggle==-1):
                    print("Paused cycling through slides")
                else:
                    print("Resumed cycling through slides")

            B = tkinter.Button(top, text ="Pause/Play", command = action)

            B.pack()
            top.mainloop()
            
        t1 = threading.Thread(target=main_det)
        t2 = threading.Thread(target=tkinter_start)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()