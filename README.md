Customer Risk Segmentation and Off-Boarding
The objective of this project is to segment customers based on risk using machine learning models and predict which users should be off-boarded based on the trained model. The project is split into two main components: Model Creation and Service API. After training, the results are stored both in a SQLite database and as a CSV file.

SQLite was chosen for its simplicity and ease of use, as the dataset in this project is not complex and performance requirements are minimal. Although SQLite may not be as performant as other databases, it is more than sufficient for this project.

Model Creation
This step involves training machine learning models (e.g., Random Forest and Naive Bayes) using labeled data. The models predict whether a user should be SUSPENDED (off-boarded) based on customer risk factors. The trained models were then used to generate a Suspension Score for each user, combining the strengths of different models. This final score helps determine the user's risk level.

Unit Tests
Unit tests have been implemented to ensure the reliability and accuracy of the core functions, such as data preprocessing, feature engineering, and model scoring. These tests validate that the code behaves as expected and that changes to the codebase do not introduce bugs. To run the tests, simply execute the following command:

* python unit_tests/convert_country_code_to_abbr_test.py
* python unit_tests/fill_null_values_test.py
* python unit_tests/reduce_mem_usage_test.py

Service API
Once the model predictions are generated, you can interact with the results using a REST API service. The service was developed using Flask and exposes multiple endpoints to retrieve the model's predictions. To simplify deployment, the service is Dockerized, making it easy to run the API in any environment.

Dockerization and Deployment
To deploy the API service, follow these steps:

1. Build the Docker image:
 - docker build --tag suspention-probability-app:1.0 .                                             
2. Run the Docker container:
 - docker run -p 1001:1001 --name suspention-probability-app suspention-probability-app:1.0        

After running the container, you can use Postman or any HTTP client to test the API.

Available Endpoints

* GET /get_all_results: Returns probability values for all transactions. No parameters are needed.
* GET /search_user_result: Takes user_id as a parameter and returns transaction results for that specific user.

All services return the results in JSON format.

Postman Collection
A Postman collection for testing the API is available in the collection folder.

This project can be easily scaled and deployed on Google Cloud Platform (GCP) using Google Kubernetes Engine (GKE) for container orchestration, ensuring scalability and reliability in a production environment.