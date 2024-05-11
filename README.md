This project implements a backend service which using RDS as the data store and being deployed in AWS.
It provides two endpoints:

"/accounts": Allow an agency to retrieve the credit data for all customers provided by specific client. It also allow some query parameters such as "customer_name", "min_balcance" etc.
"/upload-csv": Allow a client to upload csv file in the specific format into the database. An agency is able to retrieve that data.
