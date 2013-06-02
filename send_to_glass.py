#!/usr/bin/python

import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import sys

def insert_timeline_item(service, text, content_type=None, attachment=None,
                         notification_level=None):
  """Insert a new timeline item in the user's glass.

  Args:
    service: Authorized Mirror service.
    text: timeline item's text.
    content_type: Optional attachment's content type (supported content types
                  are 'image/*', 'video/*' and 'audio/*').
    attachment: Optional attachment as data string.
    notification_level: Optional notification level, supported values are None
                        and 'AUDIO_ONLY'.

  Returns:
    Inserted timeline item on success, None otherwise.
  """
  timeline_item = {'text': text}
  media_body = None
  if notification_level:
    timeline_item['notification'] = {'level': notification_level}
  if content_type and attachment:
    media_body = MediaIoBaseUpload(
        io.BytesIO(attachment), mimetype=content_type, resumable=True)
  try:
    return service.timeline().insert(
        body=timeline_item, media_body=media_body).execute()
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


message = str(sys.argv[1])

# Copy your credentials from the APIs Console
#CLIENT_ID = ''
#CLIENT_SECRET = ''

# Check https://developers.google.com/drive/scopes for all available scopes
#OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/glass.timeline'

# Redirect URI for installed apps
#REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Path to the file to upload
#FILENAME = 'document.txt'

# Run through the OAuth flow and retrieve credentials
#flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
#authorize_url = flow.step1_get_authorize_url()
#print 'Go to the following link in your browser: ' + authorize_url
#code = raw_input('Enter verification code: ').strip()
#credentials = flow.step2_exchange(code)

storage = Storage('credentials')
#storage.put(credentials)
credentials = storage.get()


# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

mirror_service = build('mirror', 'v1', http=http)

insert_timeline_item(mirror_service, message, None, None, "DEFAULT")



