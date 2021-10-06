import os
import pkg_resources


HOME_PATH = os.path.expanduser('~')
ASCHED_DIR_PATH = os.path.join(HOME_PATH, '.asched')
os.makedirs(ASCHED_DIR_PATH, exist_ok=True)

DB_PATH = os.path.join(ASCHED_DIR_PATH, 'deadlines.db')
CREATE_TABLES_FILE_PATH = pkg_resources.resource_filename('asched', 'static/tables/create_tables.sqlite')