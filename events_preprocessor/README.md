# Events preprocessor

- **Goal**: Preprocessing of PRISMA events folders, sorted out and tar gzipped by station.

- **Description**: The tool checks the incoming events path, selects the folders that have not yet been archived, transfers them to a preprocess folder, renames the FITS file inside each station folder, adds the EVENT key, creates a .tar.gz file for each of the stations and copies them to the ingestion folder.

- **Configuration parameters**:
    - "email" [string]: email address to be alerted in case of preprocessing failure
    - "sender" [string]: email address of the sender
    - "smtp_host" [string]: smtp domain of the local machine sending the email 
    - "rsync_folder" [string]: path to the folder where the events are rsynced from the French server
    - "db_host" [string]: RadioDataImporter local database hostname
    - "db_user" [string]: RadioDataImporter local database user
    - "db_pwd" [string]: RadioDataImporter local database password
    - "db_name" [string]: RadioDataImporter local database name
    - "db_port" [unsigned long]: RadioDataImporter local database port 
    - "process_folder" [string]: path to the folder where the events folders are copied to be processed
    - "ingest_folder" [string]: path to the folder monitored by the inotify daemon of the RadioDataImporter
    - "stations" [string]: text file listing all the foreign stations
    - "thumbs_folder" [string]: path to the folder where the thumbnails should be copied
    - "failure_folder" [string]: path to the folder where the failed preprocessed events are moved

- **Requirements**:
    - python3
    - pip3 install astropy
    - pip3 install pymysql
    - pip3 install sqlalchemy 

- **Usage**:
    - python3 main.py
