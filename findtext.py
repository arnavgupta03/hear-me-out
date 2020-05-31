from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']

# The ID of a sample presentation.
PRESENTATION_ID = '1Sj5cp0Cm-uvuhWIGb5OesZlA_mEI9XhSNe_q1WsgMbY'

def main():
    """Shows basic usage of the Slides API.
    Prints the number of slides and elments in a sample presentation.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
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

    service = build('slides', 'v1', credentials=creds)

    # Call the Slides API
    presentation = service.presentations().get(
        presentationId=PRESENTATION_ID).execute()
    slides = presentation.get('slides')

    #print(slides)
    print('The presentation contains {} slides:'.format(len(slides)))
    for i, slide in enumerate(slides):
        for el in slide.get('pageElements', []):
            #print(slide.get())
            if el['shape']['shapeType']=='TEXT_BOX':
                for textElement in el['shape']['text']['textElements']:
                    if (el['shape']['text']['textElements'].index(textElement)%2==1):
                       print(textElement['textRun']['content'])
        
        # print('- Slide #{} contains {} elements.'.format(
            #i + 1, slide.get('pageElements.shape.text.textElements.textRun.content')))


if __name__ == '__main__':
    main()