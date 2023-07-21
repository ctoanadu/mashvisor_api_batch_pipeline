# Description
This project presents a **sophisticated event-driven microservices architecture** on AWS to conduct Airbnb property analysis. Leveraging AWS Lambda functions, S3, AWS Redshift, CloudWatch, and SNS, the pipeline seamlessly extracts, transforms, and loads data from the Mashvisor API into an AWS Redshift database. Event-driven triggers ensure data processing efficiency, while SNS notifications promptly alert stakeholders in case of any failures.

## Project Overview
This data engineering project showcases an advanced event-driven microservices architecture to analyze Airbnb property data for 100 cities in California using the Mashvisor API. The architecture comprises several loosely-coupled microservices that react to events and execute specific tasks, ensuring modularity, scalability, and efficient data processing.

## Main Components

### Data Extraction Microservice (Event-Driven Lambda Function):
- An event-driven AWS Lambda function performs data extraction from the Mashvisor API.
- Scheduled CloudWatch events trigger the Lambda function periodically.
- Upon invocation, the function sends API requests to fetch Airbnb property data from the 100 selected cities.
- The extracted data is stored in an S3 bucket, triggering the next microservice.

### Data Transformation Microservice (Event-Driven Lambda Function):
- Another Lambda function, triggered by S3 events, handles data transformation.
- As soon as new data is uploaded to the S3 bucket, the Lambda function automatically starts executing.
- It reads the data, applies necessary transformations, and converts it into the desired analysis-ready format.
- The transformed data is saved to a different S3 bucket, initiating the final microservice.

### Data Loading Microservice (Event-Driven Lambda Function):
- An event-driven Lambda function for data loading into AWS Redshift.
- S3 events trigger the function once new transformed data arrives in the designated S3 bucket.
- The Lambda function efficiently loads the data into an AWS Redshift database using a COPY command.
- AWS Redshift then stores the data for further analysis and reporting.

### Error Handling and Notifications:
- The microservices architecture integrates an SNS topic for error handling.
- In case of any Lambda function failures, SNS sends immediate notification emails to subscribed stakeholders.
- This proactive approach ensures prompt resolution and minimizes any potential downtime.

## Project Advantages:
- Scalable Architecture: The event-driven microservices architecture allows easy scaling of individual components based on demand.
- Decoupled Services: The loosely-coupled microservices ensure modularity and independence, making maintenance and updates more manageable.
- Real-time Responsiveness: The pipeline reacts instantly to events, optimizing data processing efficiency and ensuring timely analysis.
- Fault Tolerant: With SNS notifications, stakeholders are promptly alerted to address any failures, ensuring high reliability.
- Cost-Effective: The serverless AWS Lambda functions and managed services minimize operational costs by only paying for actual usage.

## Conclusion:
By employing an event-driven microservices architecture on AWS, this data engineering project provides a powerful solution for Airbnb property analysis. Leveraging AWS Lambda functions, S3, AWS Redshift, CloudWatch, and SNS, the pipeline efficiently extracts, transforms, and loads data, ensuring accurate and timely insights. The modular and scalable architecture empowers data engineers to seamlessly analyze Airbnb property data across California, while SNS notifications keep the team informed about any potential issues.
