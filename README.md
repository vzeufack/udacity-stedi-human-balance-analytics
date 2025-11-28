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
<img width="2648" height="1268" alt="image" src="https://github.com/user-attachments/assets/e2f72fc0-d402-4447-ab23-00ef9e19751e" />

### Landing zones

The following scripts contain the DDL to create the landing zone tables. The data was copied from the original Git repo to those tables:
- **customer_landing.sql**

  <img width="1845" height="618" alt="customer_landing" src="https://github.com/user-attachments/assets/c0e7f9f3-7f15-472f-9c67-750907dd06d0" />
  <img width="1387" height="793" alt="image" src="https://github.com/user-attachments/assets/d97c4475-8b0e-4a0f-b96e-62c009b80bf1" />
  
- **accelerometer_landing.sql**
  
  <img width="1857" height="650" alt="accelerometer_landing" src="https://github.com/user-attachments/assets/284852a3-4631-4cc4-bb5c-b7b9e7fd865b" />


- **step_trainer_landing.sql**
  
  <img width="1846" height="686" alt="step_trainer_landing" src="https://github.com/user-attachments/assets/c0a33999-423c-46bb-b541-9a93256be00f" />



### Trusted and curated zones
- **customer_landing_to_trusted.py**

  Has a node that drops rows that do not have data in the sharedWithResearchAsOfDate column
  <img width="2255" height="927" alt="image" src="https://github.com/user-attachments/assets/bc4ba847-5cc7-4506-a3ef-808335e95461" />
  <img width="2524" height="601" alt="image" src="https://github.com/user-attachments/assets/4bcd51c7-1d49-488c-9186-6df45e01a7c7" />

- **accelerometer_landing_to_trusted.py**

  Has a node that inner joins the customer_trusted data with the accelerometer_landing data by emails. The produced table should have only columns from the accelerometer table
  <img width="1572" height="771" alt="image" src="https://github.com/user-attachments/assets/9238a13a-b341-43aa-a3d4-b0028f4aa8d3" />
  <img width="1873" height="627" alt="image" src="https://github.com/user-attachments/assets/e7e15cd7-61b3-4192-9068-e1dd56a1590b" />


- **customer_trusted_to_curated.py**

  Has a node that inner joins the customer_trusted data with the accelerometer_trusted data by emails. The produced table should have only columns from the customer table.
  <img width="1572" height="708" alt="image" src="https://github.com/user-attachments/assets/4a1d74c9-4c2e-4821-9874-85f3753e210e" />
  <img width="1856" height="623" alt="image" src="https://github.com/user-attachments/assets/afb98563-41cd-4ac5-b3e6-ed1ea346d7d8" />
  

- **step_trainer_trusted.py**

  Has a node that inner joins the step_trainer_landing data with the customer_curated data by serial numbers
  <img width="1588" height="675" alt="image" src="https://github.com/user-attachments/assets/1374917c-9c6e-422e-a7bc-2476d3306678" />
  <img width="1841" height="607" alt="image" src="https://github.com/user-attachments/assets/1710eb69-c620-4720-ae83-3bf30c752b56" />


- **machine_learning_curated.py**

  Has a node that inner joins the step_trainer_trusted data with the accelerometer_trusted data by sensor reading time and timestamps
  <img width="1544" height="704" alt="image" src="https://github.com/user-attachments/assets/76cd4b6f-8cbb-4c22-b8ab-d295fffa6e37" />
  <img width="1815" height="624" alt="image" src="https://github.com/user-attachments/assets/7bca4e55-6bcc-446f-8883-424fbab09576" />



