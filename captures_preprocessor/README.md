# Captures preprocessor

- **Goal**: Collect PRISMA captures' FITS and JPG files from rsync folders and copy them to the ingestion folder.

- **Description**: The tool checks the incoming captures rsync path and for each of the cameras, according to the number of months specified in the configuration file, selects all the FITS and JPG files that have not been archived yet. The selected FITS files are copied to the NADIR ingestion folder (preProcessor folder). The JPG files are copied all together in one single folder. 

- **Configuration parameters**:
    - "email": email address to be alerted in case of preprocessing failure
    - "sender": email address of the sender
    - "smtp_host": smtp domain of the local machine sending the email 
    - "rsync_folder": path to the folder where the captures are rsynced from the captures collection server
    - "threads_nr": number of threads for performing a query on the DB
    - "months_nr": number of months to check the captures back from now
    - "db_host": hostname of the DB on which the datamodel is defined
    - "db_user": name of the user that has access on the DB on which the datamodel is defined
    - "db_pwd": password for accessing the DB on which the datamodel is defined
    - "db_name": name of the DB containing the datamodel 
    - "db_port": port on which the DB is listening
    - "tb_name": name of the table containing the captures metadata
    - "ingest_folder": path to the folder monitored by the inotify daemon of preProcessor
    - "thumbs_folder": path to the folder where the thumbnails have to be copied

- **Recommended**:
    - cd PRISMAIngestion
    - python3.6 -m venv env
    - source env/bin/activate
    - pip3 install sqlalchemy
    - pip3 install astropy
    - pip3 install pymysql
    
- **Usage**:
    - python3 main.py
