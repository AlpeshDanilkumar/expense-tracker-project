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
1. **app.py**: defining routes for expense tracking and setting up database models and metrics.
2. **requirements.txt**: This file lists the Python libraries needed by the Flask app, which will be installed when building the Docker image.
3. **Dockerfile**: The Dockerfile is set up to create a self-contained image for the Flask app, including dependencies and the command to run the app.
4. **docker-compose.yml**: Define the services for the Flask app (expense-tracker), PostgreSQL database, and monitoring tools (Prometheus, Grafana, Node Exporter) in a Docker Compose file. This makes it easier to run all services together.
5. **prometheus.yml**:  Configures Prometheus to scrape metrics from the Flask app and system-level metrics from Node Exporter.
