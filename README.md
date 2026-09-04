Markdown
# Serverless Event-Driven User Submission Platform

A scalable, event-driven, fully serverless web application built on AWS. This project captures user registrations through an S3-hosted frontend, processes incoming requests asynchronously via API Gateway, AWS Lambda, and SQS, and persists the data in DynamoDB.

---

## ??? Architecture Overview

[ User Browser ]
¦
?
[ S3 Static Website Hosting ]
¦
(HTTP POST)
¦
?
[ Amazon API Gateway ]
¦
(Proxy Event)
¦
?
[ AWS Lambda 1: apiDataProducer ] ---? Generates Request ID & pushes payload
¦
?
[ AWS SQS: user-submissions-queue ] --? Decouples ingestion & buffers requests
¦
(SQS Trigger)
¦
?
[ AWS Lambda 2: apiDataProcessing ] --? Parses queue batch & writes to DB
¦
?
[ Amazon DynamoDB: UserSubmissions ]


---

## ? Features

- **Asynchronous Data Ingestion:** Decoupled architecture using SQS ensures fast response times for the frontend.
- **Fault Tolerant & Resilient:** Handles traffic spikes without dropping submission payloads.
- **CORS-Enabled REST API:** Configured with API Gateway Proxy Integration and preflight response handling.
- **Pay-per-Use Model:** Zero idle server cost, leveraging 100% native AWS serverless components.

---

## ??? Tech Stack & AWS Services

- **Frontend:** HTML5, Bootstrap 5, JavaScript (Fetch API)
- **Hosting:** Amazon S3 (Static Website Hosting)
- **API Management:** Amazon API Gateway (REST API)
- **Compute:** AWS Lambda (Python 3.x)
- **Messaging:** Amazon Simple Queue Service (SQS)
- **Database:** Amazon DynamoDB (NoSQL)

---

## ?? Setup & Deployment Guide

### 1. Database Provisioning
- **Service:** Amazon DynamoDB
- **Table Name:** `UserSubmissions`
- **Partition Key:** `request_id` (String)

---

### 2. Message Queue Provisioning
- **Service:** Amazon SQS
- **Queue Name:** `user-submissions-queue`
- **Type:** Standard Queue

---

### 3. Backend Lambda Functions

#### Consumer Function (`apiDataProcessing`)
- **Trigger:** SQS (`user-submissions-queue`)
- **IAM Permissions:** `AWSLambdaBasicExecutionRole`, `AmazonDynamoDBFullAccess`
- **Logic:** Reads SQS records and inserts `request_id`, `name`, `email`, `age`, `message`, and `timestamp` into DynamoDB.

#### Producer Function (`apiDataProducer`)
- **IAM Permissions:** `AWSLambdaBasicExecutionRole`, `AmazonSQSFullAccess`
- **Logic:** Parses API Gateway body, appends a generated `uuid4`, pushes the payload to SQS, and returns a `200 OK` response with CORS headers.

---

### 4. API Configuration
- **Service:** Amazon API Gateway (REST API)
- **Resource Route:** `/users`
- **Method:** `POST`
- **Integration Type:** Lambda Proxy Integration targeting `apiDataProducer`
- **CORS:** Enabled for `OPTIONS` and `POST` methods with Access-Control headers.

---

### 5. Static Frontend Deployment
1. Update `API_URL` in `index.html` with your deployed API Gateway stage endpoint:
   ```javascript
   const API_URL = "https://<your-api-id>[.execute-api.us-east-1.amazonaws.com/prod/users](https://.execute-api.us-east-1.amazonaws.com/prod/users)";
Upload index.html to your S3 bucket.

Enable Static Website Hosting on the bucket settings.

Ensure bucket access policies permit public read access for hosted files.

?? End-to-End Verification
Open the S3 public website endpoint in your browser.

Fill out and submit the User Registration Form.

Verify the immediate "Form submitted successfully!" response in the UI.

Check DynamoDB Console -> Explore Table Items on UserSubmissions to confirm data persistence.11:58 PM 02-09-202611:58 PM 02-09-202611:58 PM 02-09-202611:58 PM 02-09-2026
