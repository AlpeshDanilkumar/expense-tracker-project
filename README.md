# Expense Tracker Application

## Overview

This Expense Tracker application is a web app built with Flask and PostgreSQL, designed to help users manage their expenses. The application is containerized using Docker and managed with Docker Compose. Metrics are collected with Prometheus and visualized using Grafana. This README includes setup instructions, running the application, monitoring setup, and GitHub Actions integration.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Monitoring and SRE](#monitoring-and-sre)
- [GitHub Actions Pipeline](#github-actions-pipeline)
- [Future Improvements](#future-improvements)

## Prerequisites

1. **Docker**: Ensure Docker is installed on your system. [Install Docker](https://docs.docker.com/get-docker/) if not already installed.
2. **Docker Compose**: Required for managing multi-container Docker applications. [Install Docker Compose](https://docs.docker.com/compose/install/) if not already installed.
3. **Prometheus** and **Grafana**: For monitoring and visualization. [Install Prometheus](https://prometheus.io/docs/prometheus/latest/installation/) and [Grafana](https://grafana.com/docs/grafana/latest/installation/) if not already installed.

## Setup and Installation

1. **Clone the Repository**

   ```bash
   git clone (https://github.com/AlpeshDanilkumar/expense-tracker-project.git)
   cd expense-tracker

2. **Create Dockerfile**

Define the environment for your Flask application:

dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]


Certainly! Here’s the README.md with all the content organized in markdown format:

markdown
Copy code
# Expense Tracker Application

## Overview

The Expense Tracker application is a web-based tool to help users track their expenses. Built using Flask and PostgreSQL, this application is containerized with Docker and managed with Docker Compose. It includes monitoring through Prometheus and visualization with Grafana. This README provides a detailed guide for setting up, running, monitoring, and deploying the application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Monitoring and SRE](#monitoring-and-sre)
- [GitHub Actions Pipeline](#github-actions-pipeline)
- [Future Improvements](#future-improvements)

## Prerequisites

1. **Docker**: Required for containerization. Install from [Docker's official website](https://docs.docker.com/get-docker/).
2. **Docker Compose**: Needed to manage multi-container Docker applications. Install from [Docker Compose installation guide](https://docs.docker.com/compose/install/).
3. **Prometheus** and **Grafana**: For monitoring and visualization. Install from [Prometheus installation guide](https://prometheus.io/docs/prometheus/latest/installation/) and [Grafana installation guide](https://grafana.com/docs/grafana/latest/installation/).

## Setup and Installation

### 1. Create Dockerfile

Define the environment for the Flask application:

```dockerfile

# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
2. Create Docker Compose File
Define services in docker-compose.yml:

yaml
Copy code
version: '3.7'
services:
  expense-tracker:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://expense_user:password@db/expense_tracker
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: expense_user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: expense_tracker
    volumes:
      - postgres_data:/var/lib/postgresql/data

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  postgres_data:
  grafana_data:
3. Create Prometheus Configuration
Configure Prometheus with prometheus.yml:

yaml
Copy code
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'flask'
    static_configs:
      - targets: ['expense-tracker:5000']
4. Create Requirements File
List the Python dependencies in requirements.txt:

txt
Copy code
Flask
SQLAlchemy
psycopg2-binary
prometheus-flask-exporter
5. Create Flask Application
Implement the Flask application in app.py:

python
Copy code
# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://expense_user:password@db/expense_tracker'
db = SQLAlchemy(app)
metrics = PrometheusMetrics(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.json
    new_expense = Expense(description=data['description'], amount=data['amount'])
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added"}), 201

@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([{'id': e.id, 'description': e.description, 'amount': e.amount} for e in expenses])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
Running the Application
1. Build and Start Containers
Run the following command to build and start the containers:

bash
Copy code
docker-compose up --build
2. Access the Application
Flask App: http://localhost:5000
Grafana: http://localhost:3000 (Login with default username admin and password admin)
Prometheus: http://localhost:9090
Monitoring and SRE
Monitoring with Prometheus and Grafana
Prometheus collects metrics from your Flask application. Ensure your application exposes metrics at the /metrics endpoint using prometheus-flask-exporter.
Grafana visualizes these metrics. Add Prometheus as a data source in Grafana:
Go to Configuration > Data Sources > Add data source.
Select Prometheus.
Set the URL to http://prometheus:9090.
Click Save & Test.
Creating Dashboards in Grafana
Create a Dashboard:
Navigate to Dashboards > New Dashboard.
Add panels to visualize metrics like request counts, response times, etc.
Configure panels to use data from Prometheus.
GitHub Actions Pipeline
Setup GitHub Actions
Create a Workflow File

Create .github/workflows/deploy.yml in your repository:

yaml
Copy code
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

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Cache Docker layers
        uses: actions/cache@v3
        with:
          path: |
            ~/.cache/docker
            /tmp/.buildx-cache
          key: ${{ runner.os }}-docker-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-docker-

      - name: Build and push Docker image
        uses: docker/build-push-action@v3
        with:
          context: .
          push: true
          tags: your-dockerhub-username/your-repo:latest

      - name: Deploy to EC2
        env:
          HOST: ${{ secrets.EC2_HOST }}
          USERNAME: ${{ secrets.EC2_USERNAME }}
          PEM_FILE: ${{ secrets.EC2_PEM_FILE }}
        run: |
          echo "$PEM_FILE" > ec2-key.pem
          chmod 600 ec2-key.pem
          ssh -o StrictHostKeyChecking=no -i ec2-key.pem $USERNAME@$HOST "cd /home/ubuntu/expense-tracker && docker-compose pull && docker-compose up --build -d"
Set Up Secrets

Add the following secrets to your GitHub repository settings:

EC2_HOST: The public IP or DNS of your EC2 instance.
EC2_USERNAME: The username for SSH (typically ubuntu for EC2 instances).
EC2_PEM_FILE: The content of your .pem file for SSH access.
Future Improvements
Add More Metrics: Implement additional metrics in your Flask application for enhanced monitoring.
Improve Security: Secure Prometheus and Grafana instances and configure authentication for your Flask application.
Automate Deployments: Enhance the GitHub Actions pipeline for more sophisticated deployment workflows.
Enhanced Monitoring: Integrate with other monitoring tools or services for comprehensive application health tracking.
