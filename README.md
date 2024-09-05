# Expense Tracker Application

## Overview

The Expense Tracker application is a comprehensive web-based tool designed to help users efficiently track and manage their expenses. Built with Flask and PostgreSQL, the application is containerized using Docker and orchestrated with Docker Compose. It includes monitoring through Prometheus and visualization with Grafana. This README provides an in-depth guide on setting up, running, monitoring, and deploying the application.

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

**Expense Tracker Homepage**: ![Homepage](https://github.com/user-attachments/assets/c899de3f-9c18-41a0-a467-ec32d5b809f8)

**Input Category and Price**: ![Input Form](https://github.com/user-attachments/assets/594f1854-04d7-427a-8d2a-f7b4a8516192)

**Add Expense**: ![Add Expense](https://github.com/user-attachments/assets/0dedffa3-31f5-4a00-91cb-196dcd4c48a6)

## Monitoring and SRE

### Dashboard

**Data Entries**: ![Data Entries](https://github.com/user-attachments/assets/450e675a-05e8-488c-b26d-002e8d3cab69)

- **Description**: Tracks the number of expense entries over time to identify trends in user activity.

**CPU Usage**: ![CPU Usage](https://github.com/user-attachments/assets/88f81947-1a0f-4bf9-a9ab-a17e0ba2c6c5)

- **Description**: Displays CPU usage across different modes (idle, user, system) to monitor performance.

**Available Memory**: ![Available Memory](https://github.com/user-attachments/assets/c9a72820-442c-4119-b49e-53cef7c89fb8)

- **Description**: Shows available system memory to ensure adequate resources for applications.

**Node Exporter Metrics**: ![Node Exporter](https://github.com/user-attachments/assets/d48bf1aa-f2cd-4ce7-a31e-3f038b5e8bd6)

- **Description**: Monitors disk I/O operations to identify potential bottlenecks or performance issues.

**Network Traffic**: ![Network Traffic](https://github.com/user-attachments/assets/6103b5fc-ad11-4a95-bd4a-c7a5f99ae571)

- **Description**: Tracks incoming network traffic to monitor data rates and identify potential network issues.

## Data Flow and Verification

**Check Database Content**:

```bash
`docker exec -it expense-tracker-db-1 /bin/bash`
`psql -h localhost -U expense_user -d expense_tracker`
`SELECT * FROM expense;`

```

![Data Flow](https://github.com/user-attachments/assets/c9302db9-2e1d-45cc-af0c-ac39822bfbdf)

## Prometheus

**Purpose**: Monitors and collects metrics from the application and system.
**Configuration**: Defined in prometheus.yml

## Grafana

**Purpose**: Visualizes metrics collected by Prometheus.
**Configuration**: Connects to Prometheus as a data source.

### Dashboards:

**Overview Dashboard**: Displays general metrics and system status.
**Expense Tracker Dashboard**: Shows detailed metrics specific to the Expense Tracker application.

### Alerts:

**Metric**: Define thresholds for metrics such as CPU usage, memory usage, or specific application metrics.
**Notification Channels:**: Set up email or Slack notifications for alerting.

## Future Improvements

1.  **Enhanced Security**: Implement additional security measures for user data protection.
2.  **User Authentication**: Add user authentication and authorization features.
3.  **Advanced Analytics**: Integrate advanced data analytics and reporting features.
4.  **Performance Optimization**: Optimize application performance and scalability.
5.  **Container Orchestration**: Consider using Kubernetes for container orchestration and management.
