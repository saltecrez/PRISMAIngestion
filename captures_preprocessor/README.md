# Captures preprocessor

- **Goal**: Preprocessing of PRISMA captures FITS and JPG files for the current month.

- **Description**: The tool checks the incoming captures path, for each of the cameras, selects the FITS and JPG files that have not yet been archived, copies the FITS files to the Nadir ingestion folder and the JPG files to their archiving folder. 

- **Requirements**:
    - pip install sqlalchemy 

- **Configuration parameters**:
    - "email": email address to be alerted in case of preprocessing failure
    - "sender": email address of the sender
    - "smtphost": hostname of the machine hosting the smtp server
    - "camerasfolder": path to the folder where the captures are rsynced from the French server
    - "dbhost": fitsImporter local database hostname
    - "dbuser": fitsImporter local database user
    - "dbpwd": fitsImporter local database password
    - "dbname": fitsImporter local database name
    - "ingestfolder": path to the folder monitored by the inotify daemon of the fitsImporter
    - "thumbsfolder": path to the folder where the thumbnails should be copied

- **Usage**:
    - python main.py
