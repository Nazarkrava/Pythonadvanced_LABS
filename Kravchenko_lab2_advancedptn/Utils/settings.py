import os
from Database.database_class import DB_PATH as db_path
from Fileworker.doc_folder.doc_folder import doc_folder
from Fileworker.xlsx_folder.xlsx_folder import xlsx_folder

DB_PATH = db_path
XLSX_PATH = os.path.join(xlsx_folder, '')
DOC_PATH = os.path.join(doc_folder, '')

