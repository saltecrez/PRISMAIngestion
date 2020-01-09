# Events preprocessor

- **Goal**: Preprocessing of PRISMA events folders, sorted out and tar gzipped by station.

- **Description**: The tool checks the incoming events path, selects the folders that have not yet been archived, transfers them to a preprocess folder, renames the FITS file inside each station folder, adds the EVENT key, creates a *.tar.gz file for each of the stations and copies them to the ingestion folder.

- **Requirements**:
    - pip install astropy
    - pip install sqlalchemy 

- **Configuration parameters**:
    - "email": email address to be alerted in case of preprocessing failure
    - "sender": email address of the sender
    - "smtphost": hostname of the machine hosting the smtp server
    - "eventfolder": path to the folder where the events are rsynced from the French server
    - "dbhost": RadioDataImporter local database hostname
    - "dbuser": RadioDataImporter local database user
    - "dbpwd": RadioDataImporter local database password
    - "dbname": RadioDataImporter local database name
    - "preprocessfolder": path to the folder where the events folders are copied to be processed
    - "ingestfolder": path to the folder monitored by the inotify daemon of the RadioDataImporter
    - "stations": text file listing all the foreign stations
    - "thumbfolder": path to the folder where the thumbnails should be copied
    - "failuresfolder": path to the folder where the failed preprocessed events are moved

- **Usage**:
    - python main.py
