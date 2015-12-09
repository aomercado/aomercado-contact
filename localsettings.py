import os


DBNAME = os.environ.get(u'OPENSHIFT_APP_NAME')
HOST = os.environ.get(u'OPENSHIFT_MONGODB_DB_HOST')
PORT = os.environ.get(u'OPENSHIFT_MONGODB_DB_PORT')
USERNAME = os.environ.get(u'OPENSHIFT_MONGODB_DB_USERNAME')
PASSWORD = os.environ.get(u'OPENSHIFT_MONGODB_DB_PASSWORD')
