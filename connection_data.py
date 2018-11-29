import os


LOCAL = {'host':     os.environ.get('local_host'),
         'database': os.environ.get('local_database'),
         'user':     os.environ.get('local_user'),
         'password': os.environ.get('local_password')}

REMOTE = {'host':     os.environ.get('remote_host'),
          'database': os.environ.get('remote_database'),
          'user':     os.environ.get('remote_user'),
          'password': os.environ.get('remote_password')}
