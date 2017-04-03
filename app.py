from __future__ import print_function
import httplib2
import os
import pprint

from apiclient import discovery
from googleapiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from flask import Flask, render_template

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive, https://www.googleapis.com/auth/drive.file'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
app = Flask(__name__)


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-commentCollector.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
    return credentials


credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('drive', 'v3', http=http)


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/authentication', methods=['POST'])
def retrieve_comments():
    id =get_fileid()
    try:
        comments = service.comments().list(fileId='1O79FEH8hY6I2FjwXUivuzmSFJ9D0VM5l7BJ5WDGk_MQ',
                                           fields="comments").execute()
        c=comments.get('comments', [])
        print(c)
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
    return render_template('index.html')


def get_fileid():
    results = service.files().list(
        pageSize=1, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files')
    print(items)
    return items

if __name__ == '__main__':
    app.run(debug=True)
