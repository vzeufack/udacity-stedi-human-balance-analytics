# udacity-stedi-human-balance-analytics
## Project Overview
The STEDI Team has been hard at work developing a hardware STEDI Step Trainer that:
- trains the user to do a STEDI balance exercise;
- and has sensors on the device that collect data to train a machine-learning algorithm to detect steps;
- has a companion mobile app that collects customer data and interacts with the device sensors.

STEDI has heard from millions of early adopters who are willing to purchase the STEDI Step Trainers and use them.

Several customers have already received their Step Trainers, installed the mobile application, and begun using them together to test their balance. The Step Trainer is just a motion sensor that records the distance of the object detected. The app uses a mobile phone accelerometer to detect motion in the X, Y, and Z directions.

The STEDI team wants to use the motion sensor data to train a machine learning model to detect steps accurately in real-time. Privacy will be a primary consideration in deciding what data can be used.

Some of the early adopters have agreed to share their data for research purposes. Only these customers’ Step Trainer and accelerometer data should be used in the training data for the machine learning model.

We will need to extract the data produced by the STEDI Step Trainer sensors and the mobile app, and curate them into a data lakehouse solution on AWS so that Data Scientists can train the learning model.

## Project Data
<img width="770" height="315" alt="image" src="https://github.com/user-attachments/assets/0dc4569c-4bbc-4c1e-b983-7e9ec33c45d1" />

### 1. Customer Records

This is the data from fulfillment and the STEDI website.

[Data Download URL](https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/tree/main/project/starter/customer/landing)

AWS S3 Bucket URI - s3://cd0030bucket/customers/

contains the following fields:

- serialnumber
- sharewithpublicasofdate
- birthday
- registrationdate
- sharewithresearchasofdate
- customername
- email
- lastupdatedate
- phone
- sharewithfriendsasofdate

### 2. Step Trainer Records

This is the data from the motion sensor.

[Data Download URL](https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/tree/main/project/starter/step_trainer/landing)

AWS S3 Bucket URI - s3://cd0030bucket/step_trainer/

contains the following fields:

- sensorReadingTime
- serialNumber
- distanceFromObject

### 3. Accelerometer Records

This is the data from the mobile app.

[Data Download URL](https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/tree/main/project/starter/accelerometer/landing)

AWS S3 Bucket URI - s3://cd0030bucket/accelerometer/

contains the following fields:

- timeStamp
- user
- x
- y
- z

## Workflow
<img width="2488" height="1268" alt="image" src="https://github.com/user-attachments/assets/786e3a67-8686-4502-b449-f99de298bf1e" />

### Landing zones

The following scripts contain the DDL to create the landing zone tables. The data was copied from the original Git repo to those tables:
- **customer_landing.sql**

  <img width="797" height="642" alt="image" src="https://github.com/user-attachments/assets/95fc668b-9eda-4e2e-9637-4dc51cec10fe" />
  <img width="1387" height="793" alt="image" src="https://github.com/user-attachments/assets/d97c4475-8b0e-4a0f-b96e-62c009b80bf1" />
  
- **accelerometer_landing.sql**
  
  <img width="627" height="637" alt="image" src="https://github.com/user-attachments/assets/47787cb2-7d47-458a-b871-abbe8c9d8b7d" />

- **step_trainer_landing.sql**
  
  <img width="766" height="646" alt="image" src="https://github.com/user-attachments/assets/dc2e04c1-a5a9-40b8-9d7c-08c612ad2045" />


### Trusted and curated zones
- **customer_landing_to_trusted.py**

  Has a node that drops rows that do not have data in the sharedWithResearchAsOfDate column
  <img width="2255" height="927" alt="image" src="https://github.com/user-attachments/assets/bc4ba847-5cc7-4506-a3ef-808335e95461" />
  <img width="2524" height="601" alt="image" src="https://github.com/user-attachments/assets/4bcd51c7-1d49-488c-9186-6df45e01a7c7" />

- **accelerometer_landing_to_trusted.py**

  Has a node that inner joins the customer_trusted data with the accelerometer_landing data by emails. The produced table should have only columns from the accelerometer table
  <img width="2550" height="921" alt="image" src="https://github.com/user-attachments/assets/c058ea83-9e56-4a0c-8227-6d9929fbd243" />
  <img width="1820" height="541" alt="image" src="https://github.com/user-attachments/assets/8bde2f7e-e5df-494c-84f5-f66f50c935b4" />


- **customer_trusted_to_curated.py**

  Has a node that inner joins the customer_trusted data with the accelerometer_trusted data by emails. The produced table should have only columns from the customer table.
  <img width="1884" height="679" alt="image" src="https://github.com/user-attachments/assets/cdddda37-911d-466d-a5ed-5ef2c5d5f5ce" />
  <img width="1863" height="677" alt="image" src="https://github.com/user-attachments/assets/0284842b-73d8-4d93-bb18-cabc2c5c484a" />


- **step_trainer_trusted.py**

  Has a node that inner joins the step_trainer_landing data with the customer_curated data by serial numbers
  <img width="1892" height="739" alt="image" src="https://github.com/user-attachments/assets/f0a923d1-fd51-4282-a0f3-3b2f8726f5e7" />
  <img width="1852" height="690" alt="image" src="https://github.com/user-attachments/assets/89621462-280e-4d49-993b-ebb4b6667ed5" />


- **machine_learning_curated.py**

  Has a node that inner joins the step_trainer_trusted data with the accelerometer_trusted data by sensor reading time and timestamps
  <img width="1544" height="704" alt="image" src="https://github.com/user-attachments/assets/76cd4b6f-8cbb-4c22-b8ab-d295fffa6e37" />
  <img width="1815" height="624" alt="image" src="https://github.com/user-attachments/assets/7bca4e55-6bcc-446f-8883-424fbab09576" />



