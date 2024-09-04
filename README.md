# Expense Tracker Application

## Overview

The Expense Tracker application is a web-based tool to help users track their expenses. Built using Flask and PostgreSQL, this application is containerized with Docker and managed with Docker Compose. It includes monitoring through Prometheus and visualization with Grafana. This README provides a detailed guide for setting up, running, monitoring, and deploying the application.


## Table of Contents

- [Prerequisites](#prerequisites)
- [Modules](#Modules)
- [Set up and Installation](#Set-up-and-Installation)
- [Running the Application](#Running-the-application)
- [Data Flow and Verification](#data-flow-and-verification)
- [Monitoring and SRE](#monitoring-and-sre)
- [GitHub Actions Pipeline](#github-actions-pipeline)
- [Future Improvements](#future-improvements)

## Prerequisites

1. **Docker**: Required for containerization. Install from [Docker's official website](https://docs.docker.com/get-docker/).
2. **Docker Compose**: Needed to manage multi-container Docker applications. Install from [Docker Compose installation guide](https://docs.docker.com/compose/install/).
3. **Prometheus** and **Grafana**: For monitoring and visualization. Install from [Prometheus installation guide](https://prometheus.io/docs/prometheus/latest/installation/) and [Grafana installation guide](https://grafana.com/docs/grafana/latest/installation/).

## Modules
1. **app.py**: defining routes for expense tracking and setting up database models and metrics.
2. **Dockerfile**: The Dockerfile is set up to create a self-contained image for the Flask app, including dependencies and the command to run the app.
3. **requirements.txt**: This file lists the Python libraries needed by the Flask app, which will be installed when building the Docker image.
4. **docker-compose.yml**: Define the services for the Flask app (expense-tracker), PostgreSQL database, and monitoring tools (Prometheus, Grafana, Node Exporter) in a Docker Compose file. This makes it easier to run all services together.
5. **prometheus.yml**:  Configures Prometheus to scrape metrics from the Flask app and system-level metrics from Node Exporter.

## Set up and Installation

### app.py
**Import necessary Libraries**
- **Flask**: The web framework that allows you to create the web app, define routes (URLs), and handle HTTP requests.
- **render_template**: Renders HTML templates.
- **request**: Used to access the expense data sent via an HTTP request.
- **redirect** and **url_for**: These are used for redirecting users after adding an expense.
- **SQLAlchemy**: An Object Relational Mapper (ORM) that simplifies database interactions by mapping Python objects to database tables.
- **PrometheusMetrics**: This integrates Prometheus monitoring into Flask, which tracks metrics (e.g., request duration, error rates).

**App Database Configuration**
- **app = Flask(name)**: This creates an instance of the Flask application.
- **app.config['SQLALCHEMY_DATABASE_URI']**: Sets the connection string for the PostgreSQL database (expense_tracker). The expense_user is the database user, and db is the database host.
- **db = SQLAlchemy(app)**: Initializes the database connection using SQLAlchemy.
- **metrics = PrometheusMetrics(app)**: Enables Prometheus monitoring for the app to expose metrics on different application performance indicators (e.g., request count, latency).

**Defining the Expense Model**
- **id**: A unique identifier for each expense, which is the primary key.
- **category**: A string field to store the category of the expense (e.g., food, transportation).
- **price**: A floating-point field to store the price of the expense.

**Index Route**
- **@app.route('/')**: This defines the route for the home page (/).
- **Expense.query.all()**: Queries all records from the Expense table.
- **sum(expense.price for expense in expenses)**: Calculates the total sum of all expense prices.
- **render_template('index.html', expenses=expenses, total=total)**: Renders the index.html template, passing the list of expenses and the total expense sum as variables.

**Expense route**
- **@app.route('/add', methods=['POST'])**: This defines the route to handle the addition of a new expense (via a POST request).
- **category** = request.form.get('category'): Gets the category value from the submitted form data.
- **price** = request.form.get('price'): Gets the price value from the submitted form data.
- **new_expense = Expense(category=category, price=float(price))**: Creates a new Expense object.
- **db.session.add(new_expense)**: Adds the new expense to the database session.
- **db.session.commit()**: Commits the changes to the database, saving the new expense.
- **redirect(url_for('index'))**: Redirects the user back to the home page after adding the expense.

**Application**
- Displays a list of all expenses and the total expense amount.
- Allows users to submit a form to add a new expense, which will then be saved in the PostgreSQL database.

### Dockerfile
Is a simple and efficient way to containerize the Flask-based Expense Tracker application.
- **WORKDIR /app**: This sets the working directory inside the container to /app. Any subsequent COPY, RUN, or CMD commands will be executed in this directory.
- **COPY and RUN requirements.txt**: Installs all of the required Python dependencies.
- Then copies all the files from the current directory (on your local machine) to the working directory inside the container. This will include your Python files, templates, static files, etc.
- **EXPOSE 5000**: lask, by default, runs on port 5000, so this ensures that the application will be accessible at that port when running inside the container.

  
### requirements.txt
- **Flask**: Flask is used to build the web application. It provides routing, request handling, and templating.
- **Flask-SQLAlchemy**: It is used to define and manage the Expense model, perform queries, and handle transactions. It simplifies database interactions by allowing you to manipulate database records using Python objects.
- **psycopg2-binary**: It allows your Flask app to communicate with the PostgreSQL database. The binary variant of psycopg2 includes precompiled wheels, making installation easier, especially in environments like Docker.
- **prometheus-flask-exporrter**: This library is responsible for exposing the Flask app’s performance metrics.


### docker-compose.yml
- There are four services: expense-tracker (Flask app), db (PostgreSQL database), prometheus, and grafana.
- **expense_user**: The database user.
- **password**: The user’s password
- **db**: The service name for the PostgreSQL database, used to resolve the hostname inside the Docker Compose network.
- **expense_tracker**: The database name.
- This section defines named volumes (postgres_data and grafana_data), which ensure that data from the PostgreSQL and Grafana services are stored persistently, even if the containers are stopped or restarted.


### prometheus.yml
Prometheus is an open-source monitoring and alerting system primarily designed to monitor systems, applications, and services, offering a powerful time-series database for storing metrics and an alerting mechanism. Prometheus allows you to monitor system health and application performance in real time. It can track system-level metrics like CPU usage, memory consumption, and disk space of the database and other services.

- **global**: Defines the global settings for Prometheus.
- **scrape_interval**: It scrapes every 15 seconds. You can adjust this based on your performance needs. Shorter intervals increase granularity but also increase storage and load on Prometheus and the target services.
- **job_name**: This names the scrape job, which in this case is expense-tracker. You can have multiple jobs, each with its own set of targets.
- **metrics_path**: This specifies the path from which Prometheus scrapes the metrics. In Flask, the prometheus_flask_exporter exposes metrics at /metrics.
- **static_configs**: Defines static targets (i.e., hard-coded endpoints that Prometheus will scrape).
- **targets**: This specifies that Prometheus should scrape metrics from the expense-tracker service on port 5000. Prometheus will use Docker’s internal DNS resolution, so expense-tracker refers to the Flask service running in the Docker Compose network.

## Running the application
1) **Docker**: Required for containerization. Install from [Docker's official website](https://docs.docker.com/get-docker/).
2) **Docker Compose**: Needed to manage multi-container Docker applications. Install from [Docker Compose installation guide](https://docs.docker.com/compose/install/).
3) Clone the Repository```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
4) Run the following command to build and start the containers: docker-compose up --build
5) Access the application
   a) Flask App: http://localhost:5000
   b) Grafana: http://localhost:3000 (Login with default username admin and password admin)
   c) Prometheus: http://localhost:9090
6) Stopping the application: docker-compose down

The Expense Tracker application is designed to help users manage their expenses effectively. It leverages a Flask web application, PostgreSQL for data storage, and is fully containerized using Docker and Docker Compose. Prometheus is used for monitoring, and Grafana provides visualization for the metrics.
   
**Expense tracker homepage**
<img width="548" alt="Screenshot 2024-09-04 at 12 20 14" src="https://github.com/user-attachments/assets/c899de3f-9c18-41a0-a467-ec32d5b809f8">

**Input Category and Price**
<img width="520" alt="Screenshot 2024-09-04 at 12 20 41" src="https://github.com/user-attachments/assets/594f1854-04d7-427a-8d2a-f7b4a8516192">

**Add expense**
<img width="502" alt="Screenshot 2024-09-04 at 12 20 48" src="https://github.com/user-attachments/assets/0dedffa3-31f5-4b1e-9626-a79c4094ab22">


## Monitoring and SRE

### Dashboard

**Data entries**
![1067db8d-7fb5-4849-8945-d00661a0870b](https://github.com/user-attachments/assets/450e675a-05e8-488c-b26d-002e8d3cab69)
The metric  counts the number of expense entries that have been made or added into the Expense Tracker application. By observing the growth of this metric over time, you can track how fast new entries are being added to your database. This can help in identifying trends in user activity or application usage.

**CPU**
![c3097ed4-4f42-43c0-bb6e-60424e242ba1](https://github.com/user-attachments/assets/88f81947-1a0f-4bf9-a9ab-a17e0ba2c6c5)
Retrieves the total amount of time that each CPU core has spent in various modes since the system started. This metric is exposed by Node Exporter, which collects and exports hardware and OS-level metrics for Prometheus. By understanding how your CPU is being utilized (idle vs. active time), you can make informed decisions about optimizing resources or scaling your infrastructure.

**Available memory**
![06bf004e-56a9-4609-9972-6a9c13ba2eac](https://github.com/user-attachments/assets/c9a72820-442c-4119-b49e-53cef7c89fb8)
This query is used to monitor the amount of available memory in the system, in bytes, and is being retrieved from the Node Exporter. By tracking available memory, you can ensure that your system has enough memory for current and future workloads. Running out of memory can cause applications to crash or lead to Out-Of-Memory (OOM) kills. Monitoring MemAvailable ensures you can detect and respond to low memory conditions before they become critical.

**Node exporter**
![06bf004e-56a9-4609-9972-6a9c13ba2eac](https://github.com/user-attachments/assets/d48bf1aa-f2cd-4ce7-a31e-3f038b5e8bd6)
Is used to monitor the total time spent on disk I/O operations (read and write) by a specific device. High disk I/O times indicate that the disk is spending a significant amount of time processing read/write requests. If this value is high relative to system uptime, it could suggest disk bottlenecks or disk performance issues. If a disk is consistently busy for long periods, it may be time to upgrade storage hardware or adjust workloads.


**Network Traffic**
![e3a9adf1-27d0-404d-9938-4897aabccf58](https://github.com/user-attachments/assets/6103b5fc-ad11-4a95-bd4a-c7a5f99ae571)
The purpose of this query is to monitor incoming network traffic on the system over the last 5 minutes, providing insights into the rate at which data is being received over different network interfaces. If the rate of network traffic is higher than expected, this could indicate potential bottlenecks or network-related issues.

## Data Flow and Verification
![e25610a4-e647-41b6-afd1-434e55e3ce19](https://github.com/user-attachments/assets/c9302db9-2e1d-45cc-af0c-ac39822bfbdf)

Here’s an overview of how application handles data from user input and stores it in the database, along with how to verify that this process is working correctly:
### 1. Application Flow
**User Interaction**:
- Users interact with HTML form hosted on the expense-tracker service. This form allows them to enter details such as category and price for various expenses.
**Form Submission**:
- When a user submits the form, the data is sent to the server via an HTTP POST request to the /add route.
**Data Handling**:
- The Flask app, running within the expense-tracker container, processes this POST request.
- In the /add route handler, the form data (category and price) is extracted.
**Database Operation**:
- A new Expense record is created with the submitted category and price.
- This record is then added to the database session and committed, which saves it to the PostgreSQL database.
**Redirect**:
- The user is redirected back to the main page (/), where they can see the updated list of expenses and the total amount spent.
### 2. Verification
**Verify Container Status**:
- We can check that all your Docker containers are running properly by using the command docker ps. Ensure you see containers for your expense-tracker, postgres, prometheus, node-exporter, and grafana services.
**Check Database Content**:
- Access the PostgreSQL container using docker exec -it expense-tracker-db-1 /bin/bash and log into the PostgreSQL database using psql -h localhost -U expense_user -d expense_tracker.
- Run SELECT * FROM expense; to view the entries in the expense table. This should reflect the expenses added through the HTML form.
### SRE Considerations
1.**Metrics Collection**:
  - Ensure that all relevant metrics are being collected to provide insights into application performance.
  - Implement additional custom metrics if needed.
2. **Security**:
Secure Prometheus and Grafana instances to prevent unauthorized access.
Configure authentication for Grafana and secure access to the Flask application.
3. **Automation**:
  - Use CI/CD pipelines, like GitHub Actions, to automate the build and deployment process.
Ensure that deployments are automated to reduce manual intervention and potential errors.
4. **Scalability**:
  - Consider scaling strategies for the application and database based on load.
  - Monitor resource usage and adjust infrastructure accordingly.
5. **Resilience**:
  - Implement failover strategies and backup plans for critical components like the database.
  - Regularly test recovery procedures to ensure system resilience.

## GitHub Actions Pipeline
![954cee26-8681-4ab3-8be3-211e98998a1f](https://github.com/user-attachments/assets/b13b1f0b-efb6-453e-903e-6a20487af2bb)
**Kubernetes Cluster Access and CI/CD Strategy Update**
As part of our deployment process, we initially faced a limitation when trying to run Kubernetes using Minikube on our local system. Since Minikube requires the system to be exposed to the internet for GitHub Actions to access the cluster, this posed a security and infrastructure challenge. Using Amazon EKS was considered but would have introduced additional costs, which we wanted to avoid.
 
To resolve this efficiently, we decided to switch to using Docker Compose for managing our multiple containers. With this setup, we’ve integrated a CI/CD pipeline via GitHub Actions, which handles the following:
- Builds new Docker images for the application
- Deletes existing containers
- Deploys new containers to ensure a seamless and updated application deployment
This solution avoids exposing the system externally, keeps costs down, and ensures our application runs smoothly in development environment.

