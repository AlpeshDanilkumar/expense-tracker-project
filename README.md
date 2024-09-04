# Expense Tracker Application

## Overview

The Expense Tracker application is a web-based tool to help users track their expenses. Built using Flask and PostgreSQL, this application is containerized with Docker and managed with Docker Compose. It includes monitoring through Prometheus and visualization with Grafana. This README provides a detailed guide for setting up, running, monitoring, and deploying the application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Modules](#Modules)
- [Setup and Installation](#Set-up-and-Installation)
- [Running the Application](#running-the-application)
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
Prometheus is an open-source monitoring and alerting system primarily designed to monitor systems, applications, and services, offering a powerful time-series database for storing metrics and an alerting mechanism. Prometheus allows you to monitor system health and application performance in real time. It can track system-level metrics like CPU usage, memory consumption, and disk space of the database and other services.
Grafana allows you to query, visualize, and understand metrics and logs from various data sources in real-time. Grafana is often used with time-series databases like Prometheus, InfluxDB, and Graphite to monitor the health and performance of systems and applications.

- There are four services: expense-tracker (Flask app), db (PostgreSQL database), prometheus, and grafana.
- **expense_user**: The database user.
- **password**: The user’s password
- **db**: The service name for the PostgreSQL database, used to resolve the hostname inside the Docker Compose network.
- **expense_tracker**: The database name.
- This section defines named volumes (postgres_data and grafana_data), which ensure that data from the PostgreSQL and Grafana services are stored persistently, even if the containers are stopped or restarted.


### prometheus.yml
- **global**: Defines the global settings for Prometheus.
- **scrape_interval**: It scrapes every 15 seconds. You can adjust this based on your performance needs. Shorter intervals increase granularity but also increase storage and load on Prometheus and the target services.
- **job_name**: This names the scrape job, which in this case is expense-tracker. You can have multiple jobs, each with its own set of targets.
- **metrics_path**: This specifies the path from which Prometheus scrapes the metrics. In Flask, the prometheus_flask_exporter exposes metrics at /metrics.
- **static_configs**: Defines static targets (i.e., hard-coded endpoints that Prometheus will scrape).
- **targets**: This specifies that Prometheus should scrape metrics from the expense-tracker service on port 5000. Prometheus will use Docker’s internal DNS resolution, so expense-tracker refers to the Flask service running in the Docker Compose network.
