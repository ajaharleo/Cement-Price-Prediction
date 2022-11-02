import sqlite3
from datetime import datetime
import os
import re
import json,csv
import shutil
import pandas as pd
from CementStrength import logger
from pathlib import Path
from CementStrength.config import ConfigurationManager

class Raw_Data_validation:

    """
             This class shall be used for handling all the validation done on the Raw Training Data!!.

             Written By: Ajaharuddin
             Version: 1.0
             Revisions: None

             """

    def __init__(self,raw_input_path: Path = ConfigurationManager().config.raw_input,schema_file_path: Path = ConfigurationManager().config.schema_file_path):
        self.Batch_Directory = raw_input_path
        self.schema_path = schema_file_path
        self.data_ingestion_config = ConfigurationManager().get_data_ingestion_config()

    def valuesFromSchema(self):
        """
                        Method Name: valuesFromSchema
                        Description: This method extracts all the relevant information from the pre-defined "Schema" file.
                        Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
                        On Failure: Raise ValueError,KeyError,Exception

                         Written By: Ajaharuddin
                        Version: 1.0
                        Revisions: None

                                """
        try:
            with open(self.schema_path, 'r') as f:
                schema_dic = json.load(f)
    
            pattern = schema_dic['SampleFileName']
            LengthOfDateStampInFile = schema_dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = schema_dic['LengthOfTimeStampInFile']
            column_names = schema_dic['ColName']
            NumberofColumns = schema_dic['NumberofColumns']

            message ="LengthOfDateStampInFile:: %s" %LengthOfDateStampInFile + "\t" + "LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile +"\t " + "NumberofColumns:: %s" % NumberofColumns + "\n"
            logger.info(message)
        except ValueError:
            logger.info("ValueError:Value not found inside schema_training.json")
            raise ValueError
        except KeyError:
            logger.info("KeyError:Key value error incorrect key passed")
            raise KeyError
        except Exception as e:
            logger.info(str(e))
            raise e
        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns


    def manualRegexCreation(self):
        """
                                Method Name: manualRegexCreation
                                Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                                            This Regex is used to validate the filename of the training data.
                                Output: Regex pattern
                                On Failure: None

                                 Written By: Ajaharuddin
                                Version: 1.0
                                Revisions: None

                                        """
        regex = "['cement_strength']+['\_'']+[\d_]+[\d]+\.csv"
        return regex

    def createDirectoryForGoodBadRawData(self):

        """
                                      Method Name: createDirectoryForGoodBadRawData
                                      Description: This method creates directories to store the Good Data and Bad Data
                                                    after validating the training data.

                                      Output: None
                                      On Failure: OSError

                                       Written By: Ajaharuddin
                                      Version: 1.0
                                      Revisions: None

                                              """

        try:
            path = self.data_ingestion_config.good_files
            if not os.path.isdir(path):
                os.makedirs(path)
            path = self.data_ingestion_config.bad_files
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as ex:
            logger.info("Error while creating Directory %s:" % ex)
            raise OSError

    def moveBadFilesToArchiveBad(self):

        """
                                            Method Name: moveBadFilesToArchiveBad
                                            Description: This method deletes the directory made  to store the Bad Data
                                                          after moving the data in an archive folder. We archive the bad
                                                          files to send them back to the client for invalid data issue.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Ajaharuddin
                                            Version: 1.0
                                            Revisions: None

                                                    """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:

            source = self.data_ingestion_config.bad_files
            if os.path.isdir(source):
                path = self.data_ingestion_config.archive_bad_files 
                if not os.path.isdir(path):
                    os.makedirs(path)
                dest = self.data_ingestion_config.archive_bad_files + str(date)+"_"+str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source+f,  dest+f)

                logger.info("Bad files moved to archive")
                if os.path.isdir(source):
                    shutil.rmtree(source)
                logger.info("Bad Raw Data Folder Deleted successfully!!")

        except Exception as e:
            logger.info("Error while moving bad files to archive:: %s" % e)
            raise e

    def validationFileNameRaw(self,regex,LengthOfDateStampInFile,LengthOfTimeStampInFile):
        """
                    Method Name: validationFileNameRaw
                    Description: This function validates the name of the training csv files as per given name in the schema!
                                 Regex pattern is used to do the validation.If name format do not match the file is moved
                                 to Bad Raw Data folder else in Good raw data.
                    Output: None
                    On Failure: Exception

                     Written By: Ajaharuddin
                    Version: 1.0
                    Revisions: None
                """
        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        good_path = self.data_ingestion_config.good_files
        if os.path.isdir(good_path):
                shutil.rmtree(good_path)
                logger.info("BadRaw directory deleted before starting validation!!!")
        bad_path = self.data_ingestion_config.bad_files
        if os.path.isdir(bad_path):
                shutil.rmtree(bad_path)
                logger.info("good raw directory deleted before starting validation!!!")

        onlyfiles = [file_name for file_name in os.listdir(self.Batch_Directory)]
        try:
            # create new directories
            self.createDirectoryForGoodBadRawData()
            for filename in onlyfiles:
                if (re.match(regex, filename)):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = (re.split('_', splitAtDot[0]))
                    if len(splitAtDot[2]) == LengthOfDateStampInFile:
                        if len(splitAtDot[3]) == LengthOfTimeStampInFile:
                            shutil.copy(os.path.join(self.Batch_Directory,filename), good_path)
                            logger.info("Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                        else:
                            shutil.copy(os.path.join(self.Batch_Directory,filename), bad_path)
                            logger.info("Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                    else:
                        shutil.copy(os.path.join(self.Batch_Directory,filename), bad_path)
                        logger.info("Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy(os.path.join(self.Batch_Directory,filename), bad_path)
                    logger.info( "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
        except Exception as e:
            logger.info( "Error occured while validating FileName %s" % e)
            raise e

    def validateColumnLength(self,NumberofColumns):
        """
            Method Name: validateColumnLength
            Description: This function validates the number of columns in the csv files.
                        It is should be same as given in the schema file.
                        If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
                        If the column number matches, file is kept in Good Raw Data for processing.
                        The csv file is missing the first column name, this function changes the missing name to "Wafer".
            Output: None
            On Failure: Exception

            Written By: Ajaharuddin
            Version: 1.0
            Revisions: None

        """
        try:
            logger.info("Column Length Validation Started!!")
            good_path = self.data_ingestion_config.good_files
            bad_path = self.data_ingestion_config.bad_files
            for file in os.listdir(good_path):
                df = pd.read_csv(os.path.join(good_path, file))
                if df.shape[1] == NumberofColumns:
                    pass
                else:
                    shutil.move(os.path.join(good_path, file), bad_path)
                    logger.info( "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
            logger.info( "Column Length Validation Completed!!")
        except OSError:
            logger.info( "Error Occured while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            logger.info( "Error Occured:: %s" % e)
            raise e

    def validateMissingValuesInWholeColumn(self):
        """
                                  Method Name: validateMissingValuesInWholeColumn
                                  Description: This function validates if any column in the csv file has all values missing.
                                               If all the values are missing, the file is not suitable for processing.
                                               SUch files are moved to bad raw data.
                                  Output: None
                                  On Failure: Exception
                                   Written By: Ajaharuddin
                                  Version: 1.0
                                  Revisions: None
                              """
        try:
            logger.info("Missing Values Validation Started!!")
            good_path = self.data_ingestion_config.good_files
            bad_path = self.data_ingestion_config.bad_files
            for file in os.listdir(good_path):
                df = pd.read_csv(os.path.join(good_path, file))
                count = 0
                for columns in df:
                    if (len(df[columns]) - df[columns].count()) == len(df[columns]):
                        count+=1
                        shutil.move(os.path.join(good_path, file),bad_path)
                        logger.info("Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
                        break
                if count==0:
                    #df.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    #df.to_csv("Training_Raw_files_validated/Good_Raw/" + file, index=None, header=True)
                    pass
        except OSError:
            logger.info( "Error Occured while moving the file :: %s" % OSError)
            raise OSError
        except Exception as e:
            logger.info( "Error Occured:: %s" % e)
            raise e


class dataTransform:
     """
               This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.
               Written By: Ajaharuddin
               Version: 1.0
               Revisions: None
               """

     def __init__(self,good_raw_file_path: Path = ConfigurationManager().get_data_ingestion_config().good_files):
          self.goodDataPath = good_raw_file_path

     def addQuotesToStringValuesInColumn(self):
          """
                                           Method Name: addQuotesToStringValuesInColumn
                                           Description: This method converts all the columns with string datatype such that
                                                       each value for that column is enclosed in quotes. This is done
                                                       to avoid the error while inserting string values in table as varchar.

                                            Written By: Ajaharuddin
                                           Version: 1.0
                                           Revisions: None
                                                   """
          try:
               onlyfiles = [f for f in os.listdir(self.goodDataPath)]
               for file in onlyfiles:
                    data = pd.read_csv(os.path.join(self.goodDataPath, file))
                    data['DATE'] = data["DATE"].apply(lambda x: "'" + str(x) + "'")
                    
                    data.to_csv(os.path.join(self.goodDataPath, file), index=None, header=True)
                    logger.info(" %s: Quotes added successfully!!" % file)
          except Exception as e:
               logger.info("Data Transformation failed because:: %s" % e)

class dBOperation:
    """
      This class shall be used for handling all the SQL operations.
      Written By: Ajaharuddin
      Version: 1.0
      Revisions: None

      """
    def __init__(self,data_ingestion_config=ConfigurationManager().get_data_ingestion_config()):
        self.data_ingestion_config = data_ingestion_config
        self.local_db_path = data_ingestion_config.training_local_db
        self.badFilePath = data_ingestion_config.bad_files
        self.goodFilePath = data_ingestion_config.good_files

    def dataBaseConnection(self,DatabaseName):

        """
                Method Name: dataBaseConnection
                Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
                Output: Connection to the DB
                On Failure: Raise ConnectionError

                 Written By: Ajaharuddin
                Version: 1.0
                Revisions: None

                """
        try:
            #Make the local database ouput directory
            if not os.path.isdir(self.local_db_path):
                os.makedirs(self.local_db_path)
            conn = sqlite3.connect(os.path.join(self.local_db_path,DatabaseName))
            logger.info("Opened %s database successfully" % DatabaseName)
        except ConnectionError:
            logger.exception("Error while connecting to database: %s" %ConnectionError)
            raise ConnectionError
        return conn

    def createTableDb(self,DatabaseName,column_names):
        """
                        Method Name: createTableDb
                        Description: This method creates a table in the given database which will be used to insert the Good data after raw data validation.
                        Output: None
                        On Failure: Raise Exception

                         Written By: Ajaharuddin
                        Version: 1.0
                        Revisions: None

                        """
        try:
            conn = self.dataBaseConnection(DatabaseName)
            c=conn.cursor()
            c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")
            if c.fetchone()[0] ==1:
                conn.close()
                logger.info("Tables created successfully!!")

                logger.info("Closed %s database successfully" % DatabaseName)

            else:

                for key in column_names.keys():
                    data_type = column_names[key]

                    #in try block we check if the table exists, if yes then add columns to the table
                    # else in catch block we will create the table
                    try:
                        conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=data_type))
                    except:
                        conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=data_type))




                conn.close()

                logger.info("Tables created successfully!!")

                logger.info("Closed %s database successfully" % DatabaseName)
        except Exception as e:
            logger.exception("Error while creating table: %s " % e)
            #conn.close()
            logger.info("Closed %s database successfully" % DatabaseName)
            raise e


    def insertIntoTableGoodData(self,DatabaseName):

        """
                               Method Name: insertIntoTableGoodData
                               Description: This method inserts the Good data files from the Good_Raw folder into the
                                            above created table.
                               Output: None
                               On Failure: Raise Exception

                                Written By: Ajaharuddin
                               Version: 1.0
                               Revisions: None

        """

        conn = self.dataBaseConnection(DatabaseName)
        goodFilePath= self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in os.listdir(goodFilePath)]

        for file in onlyfiles:
            try:
                with open(os.path.join(goodFilePath,file), "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                logger.info(" %s: File loaded successfully!!" % file)
                                conn.commit()
                            except Exception as e:
                                raise e

            except Exception as e:

                conn.rollback()
                logger.error("Error while creating table: %s " % e)
                shutil.move(os.path.join(goodFilePath,file), badFilePath)
                logger.info("File Moved Successfully %s" % file)
                conn.close()

        conn.close()


    def selectingDatafromtableintocsv(self,DatabaseName):

        """
                               Method Name: selectingDatafromtableintocsv
                               Description: This method exports the data in GoodData table as a CSV file to a given location.
                               Output: None
                               On Failure: Raise Exception

                                Written By: Ajaharuddin
                               Version: 1.0
                               Revisions: None

        """

        cummilated_csv_path = self.data_ingestion_config.cummilated_csv
        self.fileName = 'InputFile.csv'
        try:
            conn = self.dataBaseConnection(DatabaseName)
            cursor = conn.cursor()

            cursor.execute("SELECT *  FROM Good_Raw_Data")

            results = cursor.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            #Make the CSV ouput directory
            if not os.path.isdir(self.cummilated_csv_path):
                os.makedirs(self.cummilated_csv_path)

            # Open CSV file for writing.
            csvFile = csv.writer(open(self.cummilated_csv_path + self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)

            logger.info("File exported successfully!!!")

        except Exception as e:
            logger.exception("File exporting failed. Error : %s" %e)


class train_validation:
    def __init__(self):
        self.raw_data = Raw_Data_validation()
        self.dataTransform = dataTransform()
        self.dBOperation = dBOperation()

    def train_validation(self):
        try:
            logger.info('Start of Validation on files for prediction!!')
            # extracting values from prediction schema
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.valuesFromSchema()
            # getting the regex defined to validate filename
            regex = self.raw_data.manualRegexCreation()
            # validating filename of prediction files
            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)
            # validating column length in the file
            self.raw_data.validateColumnLength(noofcolumns)
            # validating if any column has all values missing
            self.raw_data.validateMissingValuesInWholeColumn()
            logger.info("Raw Data Validation Complete!!")

            logger.info("Creating Training_Database and tables on the basis of given schema!!!")
            # create database with given name, if present open the connection! Create table with columns given in schema
            self.dBOperation.createTableDb('Training', column_names)
            logger.info("Table creation Completed!!")
            logger.info("Insertion of Data into Table started!!!!")
            # insert csv files in the table
            self.dBOperation.insertIntoTableGoodData('Training')
            logger.info("Insertion in Table completed!!!")
            logger.info("Deleting Good Data Folder!!!")
            # Delete the good data folder after loading files in table
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            logger.info("Good_Data folder deleted!!!")
            logger.info("Moving bad files to Archive and deleting Bad_Data folder!!!")
            # Move the bad files to archive folder
            self.raw_data.moveBadFilesToArchiveBad()
            logger.info("Bad files moved to archive!! Bad folder Deleted!!")
            logger.info("Validation Operation completed!!")
            logger.info("Extracting csv file from table")
            # export data in table to csvfile
            self.dBOperation.selectingDatafromtableintocsv('Training')

        except Exception as e:
            raise e