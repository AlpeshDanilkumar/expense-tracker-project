# Expense Tracker Application

## Overview

The Expense Tracker application is a comprehensive web-based tool designed to help users efficiently track and manage their expenses. Built with Flask and PostgreSQL, the application is containerized using Docker and orchestrated with Docker Compose. It includes monitoring through Prometheus and visualization with Grafana. This README provides an in-depth guide on setting up, running, monitoring, and deploying the application.

### Development and Deployment Setup

-   **Development:** All development and testing are conducted directly on an Ubuntu EC2 instance from AWS. Code is written locally and synced to the server via SSH.
-   **Deployment:** Managed via GitHub Actions, which deploys updates to the EC2 instance by pulling the latest code, rebuilding Docker containers, and restarting them.

## Application Flow

1. **User Interaction**:
   - Users interact with the HTML form on the expense-tracker service to input expense details.
2. **Form Submission**:
   - Data is sent via HTTP POST request to the `/add` route.
3. **Data Handling**:
   - Flask processes the request, extracting the category and price from the form.
4. **Database Operation**:
   - A new `Expense` record is created and saved to the PostgreSQL database.
5. **Redirect**:
   - Users are redirected to the main page to view updated expense data.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Modules](#modules)
- [Set Up and Installation](#set-up-and-installation)
- [Running the Application](#running-the-application)
- [Data Flow and Verification](#data-flow-and-verification)
- [Monitoring and SRE](#monitoring-and-sre)
- [GitHub Actions Pipeline](#github-actions-pipeline)
- [Future Improvements](#future-improvements)

## Prerequisites

1. **Docker**: Required for containerization. Install Docker from the [official website](https://docs.docker.com/get-docker/).
2. **Docker Compose**: Needed to manage multi-container Docker applications. Install Docker Compose from the [installation guide](https://docs.docker.com/compose/install/).
3. **Prometheus** and **Grafana**: For monitoring and visualization. Install Prometheus from the [installation guide](https://prometheus.io/docs/prometheus/latest/installation/) and Grafana from the [installation guide](https://grafana.com/docs/grafana/latest/installation/).

## Modules

1. **`app.py`**: Defines routes for expense tracking and sets up database models and metrics.
2. **`Dockerfile`**: Contains instructions to build a Docker image for the Flask app, including dependencies and the command to run the app.
3. **`requirements.txt`**: Lists the Python libraries required by the Flask app, which are installed during the Docker image build.
4. **`docker-compose.yml`**: Defines the services for the Flask app, PostgreSQL database, and monitoring tools (Prometheus, Grafana, Node Exporter) in Docker Compose.
5. **`prometheus.yml`**: Configures Prometheus to scrape metrics from the Flask app and system-level metrics from Node Exporter.
6. **`deploy.yml`**: GitHub Actions workflow configuration for continuous integration and deployment.

## Set Up and Installation

### `app.py`

**Import Necessary Libraries**

- **Flask**: Web framework for creating the web app, defining routes, and handling HTTP requests.
- **render_template**: Renders HTML templates.
- **request**: Accesses expense data sent via HTTP requests.
- **redirect** and **url_for**: Redirect users after adding an expense.
- **SQLAlchemy**: ORM for mapping Python objects to database tables.
- **PrometheusMetrics**: Integrates Prometheus monitoring into Flask.

**App Database Configuration**

- **`app = Flask(__name__)`**: Creates an instance of the Flask application.
- **`app.config['SQLALCHEMY_DATABASE_URI']`**: Sets the connection string for the PostgreSQL database.
- **`db = SQLAlchemy(app)`**: Initializes the database connection with SQLAlchemy.
- **`metrics = PrometheusMetrics(app)`**: Enables Prometheus monitoring.

**Defining the Expense Model**

- **`id`**: Unique identifier for each expense (primary key).
- **`category`**: Stores the expense category (e.g., food, transportation).
- **`price`**: Stores the price of the expense.

**Routes**

- **Index Route (`/`)**:

  - **`Expense.query.all()`**: Retrieves all expense records.
  - **`sum(expense.price for expense in expenses)`**: Calculates the total amount spent.
  - **`render_template('index.html', expenses=expenses, total=total)`**: Renders the index page with expenses and total amount.

- **Add Expense Route (`/add`, POST)**:
- **`category = request.form.get('category')`**: Retrieves the category from the form.
- **`price = request.form.get('price')`**: Retrieves the price from the form.
- **`new_expense = Expense(category=category, price=float(price))`**: Creates a new Expense object.
- **`db.session.add(new_expense)`**: Adds the new expense to the session.
- **`db.session.commit()`**: Commits the transaction to save the expense.
- **`redirect(url_for('index'))`**: Redirects to the index page after adding an expense.

### Dockerfile

**Purpose:**
Containerizes the Flask-based Expense Tracker application.

- **`FROM python:3.9-slim`**: Uses a lightweight Python 3.9 image.
- **`WORKDIR /app`**: Sets the working directory in the container.
- **`COPY requirements.txt .`**: Copies the requirements file to the container.
- **`RUN pip install --no-cache-dir -r requirements.txt`**: Installs dependencies.
- **`COPY . .`**: Copies the application code to the container.
- **`EXPOSE 5000`**: Exposes port 5000 for the Flask app.
- **`CMD ["python", "app.py"]`**: Runs the Flask application.

### `requirements.txt`

- **Flask**: Web framework for building the application.
- **Flask-SQLAlchemy**: ORM for managing the Expense model and database interactions.
- **psycopg2-binary**: PostgreSQL adapter for Python.
- **prometheus-flask-exporter**: Library for exposing Flask app performance metrics to Prometheus.

### `docker-compose.yml`

**Purpose:**
Manages multi-container Docker applications.

**Services:**

- **expense-tracker**:

  - **Build Context**: Builds the Docker image from the Dockerfile.
  - **Ports**: Maps port 5000 on the host to port 5000 in the container.
  - **Environment Variables**: Configures database connectivity.
  - **Depends On**: Ensures the `db` service is available before starting.

- **db**:

  - **Image**: Uses PostgreSQL 13.
  - **Environment Variables**: Sets up PostgreSQL user, password, and database.
  - **Volumes**: Persists database data.

- **prometheus**:

  - **Image**: Uses the Prometheus image.
  - **Volumes**: Mounts configuration files.
  - **Ports**: Maps port 9090 for Prometheus UI.

- **grafana**:

  - **Image**: Uses the Grafana image.
  - **Ports**: Maps port 3000 for Grafana UI.
  - **Volumes**: Persists Grafana data.
  - **Environment Variables**: Sets the admin password.

- **node-exporter**:

  - **Image**: Uses the Node Exporter image for system metrics.
  - **Ports**: Maps port 9100 for Node Exporter.

- **postgres_exporter**:

  - **Image**: Uses the Postgres Exporter image.
  - **Environment Variables**: Configures PostgreSQL metrics source.
  - **Depends On**: Ensures dependencies on `db` and `prometheus`.

**Volumes:**

- **`postgres_data`**: Stores PostgreSQL data.
- **`grafana_data`**: Stores Grafana data.

### `prometheus.yml`

**Purpose:**
Configures Prometheus to scrape metrics.

**Configuration:**

- **Global Settings:**

  - **`scrape_interval`**: Sets the frequency for scraping metrics (15 seconds).

- **Scrape Jobs:**

  - **`expense-tracker`**: Scrapes metrics from the Flask app at `/metrics`.
  - **`node_exporter`**: Scrapes system metrics.
  - **`postgres`**: Scrapes PostgreSQL metrics.

- **Rule Files:**
  - **`alert.rules.yml`**: Contains alerting rules.

### `deploy.yml`

**Purpose:**
The `deploy.yml` file defines a GitHub Actions workflow for automating the build, test, and deployment process of the Expense Tracker application. It ensures that the application is built and deployed automatically whenever changes are pushed to the `main` branch of the repository.

**Key Sections:**

- **`name`**: Specifies the name of the workflow, in this case, "Deploy Application."

- **`on`**:

  - **`push`**: Triggers the workflow on pushes to the `main` branch. This means that every time changes are pushed to `main`, the workflow will run.

- **`jobs`**:

  - **`build-and-deploy`**: Defines the job responsible for building and deploying the application.

    - **`runs-on`**: Specifies the environment where the job will run, which is `ubuntu-latest` in this case.

    - **`steps`**: Lists the steps to execute in the job:
      - **`Checkout code`**: Uses the `actions/checkout` action to fetch the latest code from the repository.
      - **`Set up Docker Buildx`**: Configures Docker Buildx, a tool for building Docker images with advanced features like multi-platform support.
      - **`Build Docker image`**: Runs a command to build the Docker image for the application using the Dockerfile.
      - **`Log in to Docker Hub`**: Uses the `docker/login-action` to authenticate with Docker Hub using credentials stored in GitHub Secrets.
      - **`Push Docker image`**: Pushes the built Docker image to Docker Hub.
      - **`Deploy to Production Server`**: SSHs into the production server and executes commands to pull the latest Docker image and restart the application using Docker Compose.

## Running the Application

1. **Install Docker**: Follow the [official Docker installation guide](https://docs.docker.com/get-docker/).
2. **Install Docker Compose**: Follow the [Docker Compose installation guide](https://docs.docker.com/compose/install/).
3. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/expense-tracker.git
   cd expense-tracker `

   ```

4. **Build and Start Containers**:

```bash
 `docker-compose up --build`

```

5. **Access the Application**:

   - **Flask App**: <http://localhost:5000>
   - **Grafana**: <http://localhost:3000> (Login with default username `admin` and password `admin`)
   - **Prometheus**: <http://localhost:9090>

6. **Stopping the Application**:

   ```bash
   `docker-compose down`

   ```

**Expense Tracker Homepage**:
![newExpenseTracker1080](https://github.com/user-attachments/assets/466cda2b-80a8-4250-baee-853fdae13972)

 - Displays individual expense names, category and the cost in a table format.
 - Displays a Pie chart showing which categories money is split into as well as another visual by price range.
 - Total cost of all expenses displayed at top.
 - Expenses can be added by filling the details and clicking Add Expense.
 - Expenses can be updated by clicking the pen icon.
 - Expenses can be deleted by clicking the X.

**Add Expense**:
![newExpenseTrackerAdd1080](https://github.com/user-attachments/assets/839aa789-387d-44cd-9749-9480f8992c70)
- Adding a new expense updates the table and pie chart as shown above.



## Data Flow and Verification

**Check Database Content**:

```bash
`docker exec -it expense-tracker-db-1 /bin/bash`
`psql -h localhost -U expense_user -d expense_tracker`
`SELECT * FROM expense;`

```

![Data Flow](https://github.com/user-attachments/assets/c9302db9-2e1d-45cc-af0c-ac39822bfbdf)

### GitHub Actions CI/CD Pipeline

To automate our deployment process, we use GitHub Actions for continuous integration and deployment (CI/CD). This pipeline helps us build, test, and deploy our Docker containers.

**Configuration Steps:**

1.  **GitHub Actions Workflow File**:

    -   Create a `.github/workflows/ci-cd.yml` file in your repository.

    **Example Workflow File**:

    name: Deploy to EC2

on:
  push:
    branches:
      - main 

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up SSH
      uses: webfactory/ssh-agent@v0.5.3
      with:
        ssh-private-key: ${{ secrets.EC2_KEY }}

    - name: Deploy to EC2
      run: |
        ssh -o StrictHostKeyChecking=no ${{ secrets.EC2_USER }}@${{ secrets.EC2_HOST }} << 'EOF'
          cd ~/expense-tracker
          git pull origin main
          docker-compose down
          docker-compose build
          docker-compose up -d
        EOF

    This workflow file automates the process of:

    -   Checking out the latest code
    -   Building a new Docker image
    -   Pushing the image to a Docker registry
    -   Deploying the updated image using Docker Compose
![image](https://github.com/user-attachments/assets/a5532da6-97b4-4c1c-9b1c-c65d66b9f3f7)


2.  **Secrets Management**:

    -   Store sensitive information, such as Docker registry credentials, in GitHub Secrets. Go to **Settings** > **Secrets** in your GitHub repository and add the following secrets:
        -   `DOCKER_USERNAME`
        -   `DOCKER_PASSWORD`

![image](https://github.com/user-attachments/assets/7eabf386-8bfe-40b3-ba2a-b31c4b855d4b)

    -   Included  screenshots of the GitHub Secrets configuration.

3.  **New Docker images and containers**:
   ![image](https://github.com/user-attachments/assets/1300c3cd-45b2-4fcc-b18d-22d510206412)


Monitoring with Grafana and Prometheus
--------------------------------------

### Overview

In this project, we use Grafana and Prometheus for monitoring and alerting. Prometheus collects metrics from our services, while Grafana is used for visualizing these metrics and setting up alerts. Below is a detailed guide on how these tools are configured and how alerts are set up.

### 1\. **Setting Up Prometheus**

**Prometheus** is an open-source monitoring system and time series database. It collects and stores metrics as time series data, which can be queried using its powerful query language.

**Configuration Steps:**

1.  **Prometheus Installation**: Prometheus is included in our Docker setup. In the `docker-compose.yml` file, we have defined a service for Prometheus:

    `prometheus:
      image: prom/prometheus
      volumes:
        - ./prometheus.yml:/etc/prometheus/prometheus.yml
      ports:
        - "9090:9090"`

2.  **Prometheus Configuration**: The Prometheus configuration file `prometheus.yml` specifies which endpoints Prometheus should scrape metrics from:

    `global:
      scrape_interval: 15s

    scrape_configs:
      - job_name: 'expense-tracker'
        metrics_path: '/metrics'
        static_configs:
          - targets: ['expense-tracker:5000']

      - job_name: 'node_exporter'
        static_configs:
          - targets: ['node-exporter:9100']

      - job_name: 'postgres'
        metrics_path: '/metrics'
        static_configs:
          - targets: ['postgres_exporter:9187']`

    This configuration tells Prometheus to scrape metrics from the expense tracker application, Node Exporter, and PostgreSQL Exporter.

**Data Entries**: 

![Data Entries](https://github.com/user-attachments/assets/450e675a-05e8-488c-b26d-002e8d3cab69)

- **Description**: Tracks the number of expense entries over time to identify trends in user activity.

**CPU Usage**: 

![CPU Usage](https://github.com/user-attachments/assets/88f81947-1a0f-4bf9-a9ab-a17e0ba2c6c5)

- **Description**: Displays CPU usage across different modes (idle, user, system) to monitor performance.

**Available Memory**: 

![Available Memory](https://github.com/user-attachments/assets/c9a72820-442c-4119-b49e-53cef7c89fb8)

- **Description**: Shows available system memory to ensure adequate resources for applications.

**Node Exporter Metrics**: 

![Node Exporter](https://github.com/user-attachments/assets/d48bf1aa-f2cd-4ce7-a31e-3f038b5e8bd6)

- **Description**: Monitors disk I/O operations to identify potential bottlenecks or performance issues.

**Network Traffic**: 

![Network Traffic](https://github.com/user-attachments/assets/6103b5fc-ad11-4a95-bd4a-c7a5f99ae571)

- **Description**: Tracks incoming network traffic to monitor data rates and identify potential network issues.

-   Included all the screenshots of Prometheus queries that was tested:


### 2\. **Setting Up Grafana**

**Grafana** is an open-source platform for monitoring and observability that integrates with Prometheus to visualize metrics.

**Configuration Steps:**

1.  **Grafana Installation**: Grafana is also included in our Docker setup:

    `grafana:
      image: grafana/grafana
      ports:
        - "3000:3000"
      volumes:
        - grafana_data:/var/lib/grafana
      environment:
        - GF_SECURITY_ADMIN_PASSWORD=admin`

2.  **Add Prometheus as a Data Source**:

    -   Log in to Grafana (default URL: `http://localhost:3000`).
    -   Navigate to **Configuration** > **Data Sources**.
    -   Click **Add data source**, select **Prometheus**, and configure it with the Prometheus server URL (e.g., `http://prometheus:9090`).

    ![image](https://github.com/user-attachments/assets/62ef3ba5-0f05-4a17-b2b9-c692f8b3bb06)

    -   Included a screenshot of the Grafana data source configuration for Prometheus.
3.  **Create Dashboards**:

    -   Go to **Create** > **Dashboard** in Grafana.
    -   Add panels to visualize metrics from Prometheus. For example, you can visualize CPU usage, memory usage, etc., using PromQL queries.

    ![image](https://github.com/user-attachments/assets/7e9be012-3f5b-4395-9e41-1b19639009cd)

   - CPU Utilisations:
      ![image](https://github.com/user-attachments/assets/c0de37e1-6576-486c-a027-d5f6a329e769)
      ![image](https://github.com/user-attachments/assets/d925078a-966e-4d9c-b4a9-da90f56c433e)
      ![image](https://github.com/user-attachments/assets/0f1407d8-0f9d-4ad9-8d16-a859efabec4c)


   - Database:
![GrafanaPostgres1080](https://github.com/user-attachments/assets/7ed8a3b2-f598-4278-ab93-58a0202ab950)

     - Postgres general stat counters such as rows fetched, inserted and updated in current session.
     - Postgres Settings such as available shared buffer memory, WAL size and max worker processes.
     - Detailed graphs for database stats and other stats such as active sessions, cache hit rate, transaction conflicts or deadlocks.

   - HTTP Requests:
![httpGrafana](https://github.com/user-attachments/assets/985886f8-11ea-4759-869d-e193bf053f33)
      - Shows Total Requests and requests per minute sent to application.
      - Errors per second (4xx and 5xx errors)
      - Average response time of the application to requests.

### 3\. **Setting Up Alerts**

Alerts are configured in Grafana based on the metrics collected by Prometheus. Alerts can notify you when specific conditions are met, such as high CPU usage or application errors.

**Configuration Steps:**

1.  **Create Alert Rules**:

    -   Go to **Alerting** > **Alert Rules** in Grafana.
    -   Click **New alert rule**.

    **Define the Alert Rule:**

    -   **Name**: Enter a descriptive name for the alert rule.
    -   **Query**: Define the PromQL query to monitor. For example, to alert when CPU usage exceeds 80%, use:
    -   **Threshold**: Set the threshold condition. For CPU usage, you might set it to alert if the rate is below 0.2, which indicates above 80% CPU usage.

   ![image](https://github.com/user-attachments/assets/c0f86aa6-f8dc-4b78-85cf-51f0a4d9ba0d)

   -   Included screenshots of the alert rule configuration.
     
2.  **Configure Evaluation Behavior**:

    -   **Pending Period**: Set how long the condition must be met before an alert is triggered (e.g., 5 minutes).
    -   **Evaluation Interval**: Define how often the alert rule is evaluated (e.g., every 1 minute).

    ![image](https://github.com/user-attachments/assets/d63d0963-f8e9-496b-9c2a-4a42592007fa)

    -   Included a screenshot of the evaluation behavior configuration.
   
3.  **Set Up Notifications**:

   ### 1\. **Configure Contact Points**

**Contact Points** are the channels through which alerts are sent. To receive notifications on Microsoft Teams, you need to configure a contact point with the Teams webhook URL.

**Configuration Steps:**

1.  **Add a New Contact Point**:
![image](https://github.com/user-attachments/assets/18fc9223-6f4c-4ada-9faa-802b9f222c32)

3.  **Configure Microsoft Teams Notification**:

    -   **Name**: Enter a name for the contact point (e.g., "Teams Alerts").
    -   **Type**: Select **Webhook**.
    -   **URL**: Enter the Microsoft Teams webhook URL (obtained from Teams as described earlier).
    -   **Custom Headers**: (Optional) Add any required headers if needed.

### 2\. **Set Up Notification Policies**

**Notification Policies** determine how alerts are routed to contact points. You can configure policies to ensure that alerts are sent to the correct contact points based on conditions and labels.

**Configuration Steps:**

1.  **Create and Define Notification Policy**:

    -   **Name**: Enter a name for the policy (e.g., "CPU and URL Alerts").
    -   **Default Contact Point**: Select the Microsoft Teams contact point you created earlier.
    -   **Group By**: Optionally group alerts by labels if needed.
    -   **Grouping**: Configure how multiple alerts are grouped into a single notification (e.g., by alert name).
![image](https://github.com/user-attachments/assets/75ae08aa-d934-4083-9118-363c0bd1ce5e)

### 2\. **Alerts on Teams**
![image](https://github.com/user-attachments/assets/458f3b41-3f4c-4029-b2e6-60e3386c29d9)
![image](https://github.com/user-attachments/assets/2211186e-8fe0-459f-a9f0-99edb7066797)


### Monitoring summary  

In this project, we use Prometheus for metrics collection and Grafana for visualization and alerting. By setting up Prometheus to scrape metrics from various endpoints and configuring Grafana to visualize these metrics and set up alerts, we ensure that we are notified of critical issues in our application. This setup helps in proactive monitoring and maintaining system reliability.

### Limitations

**Kubernetes Cluster Access and CI/CD Strategy Update:**

As part of our deployment process, we initially faced a limitation when trying to run Kubernetes using Minikube on our local system. Since Minikube requires the system to be exposed to the internet for GitHub Actions to access the cluster, this posed a security and infrastructure challenge. Using Amazon EKS was considered but would have introduced additional costs, which we wanted to avoid.
![image](https://github.com/user-attachments/assets/d48df987-b986-413c-9cac-b6c623885d66)

To resolve this efficiently, we decided to switch to using Docker Compose for managing our multiple containers. With this setup, we've integrated a CI/CD pipeline via GitHub Actions, which handles the following:

-   Builds new Docker images for the application
-   Deletes existing containers
-   Deploys new containers to ensure a seamless and updated application deployment

This solution avoids exposing the system externally, keeps costs down, and ensures our application runs smoothly in the development environment.


Site Reliability Engineering (SRE) Principles:
---------------------------------------------

### Applied SRE Principles

1.  **Monitoring and Observability**:

    -   **Prometheus and Grafana Integration**: Integrated Prometheus for metrics collection and Grafana for visualization provides comprehensive observability into the application's health and performance. This setup facilitates proactive monitoring and timely issue detection.
    -   **Alerts and Notifications**: Alerts are configured to notify the team when critical metrics exceed predefined thresholds, such as CPU usage above 80% or HTTP status code anomalies. Notifications are sent via Microsoft Teams to ensure prompt action.
2.  **Automation**:

    -   **CI/CD Pipeline**: Utilizes GitHub Actions for automated deployments. The pipeline performs code checkout, builds Docker images, and deploys containers to EC2, reducing manual effort and ensuring consistent deployment processes.
    -   **Docker Compose**: Manages multiple containers and orchestrates service deployments, automating aspects of container management and scaling.
3.  **Reliability and Availability**:

    -   **Service Monitoring**: Monitors application performance using metrics like CPU usage and HTTP request rates. These metrics are crucial for maintaining application reliability and availability.
    -   **Alerting Configuration**: Configured to send alerts for critical issues such as high CPU usage and HTTP request errors, facilitating quick resolution and maintaining application uptime.
4.  **Incident Management**:

    -   **Alert Notifications**: Integrated with Microsoft Teams to ensure that critical alerts are communicated to the team efficiently, enabling faster response and incident resolution.
5.  **Continuous Improvement**:

    -   **Regular Updates**: The CI/CD pipeline supports continuous integration and delivery, allowing for regular updates and improvements to the application while minimizing manual effort.
    -   **Monitoring Feedback Loop**: Utilizes feedback from monitoring and alerting to continuously iterate and enhance system reliability.

### Toil Management

**Toil** refers to repetitive, manual, and operational work that does not contribute to the long-term improvement of the system and is often prone to human error. In the context of this project:

-   **Automated Deployments**: The CI/CD pipeline reduces toil by automating the deployment process, eliminating the need for manual interventions during code deployments and updates.
-   **Automated Monitoring and Alerts**: By setting up Prometheus and Grafana with automated alerting, we reduce the manual effort required to monitor application health and respond to issues.

**Future Improvements**:

-   **Reduce Manual Intervention**: Continuously look for opportunities to further automate operational tasks to minimize toil and improve operational efficiency.
-   **Define and Monitor SLOs**: Establish clear SLOs for application performance and reliability. Set up monitoring to ensure these SLOs are met and regularly review and adjust as necessary.
-   **Report on SLAs and SLOs**: Implement reporting mechanisms to track compliance with SLAs and SLOs, providing visibility into application performance and reliability.

## Contributors

- [Nabiha Sharif](https://github.com/Nabiha717)
- [Richard Lam](https://github.com/thebigburd)
- [Alpesh Danilkumar](https://github.com/AlpeshDanilkumar)

