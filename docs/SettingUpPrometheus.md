### Setting Up Prometheus for Monitoring

**Overview:** We have configured Prometheus to monitor metrics from our application, database, and system. Prometheus scrapes these metrics and stores them, allowing us to set up alerts and visualize the data using Grafana.

**Setup Steps:**

1.  **Docker Compose Configuration:** We set up Prometheus as a service in our `docker-compose.yml` file to run alongside other services like the application and the database.


    `version: '3.7'
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

      node-exporter:
        image: prom/node-exporter
        ports:
          - "9100:9100"

      postgres_exporter:
        image: prometheuscommunity/postgres-exporter
        container_name: postgres_exporter
        environment:
          DATA_SOURCE_NAME: "postgresql://expense_user:password@db:5432/expense_tracker?sslmode=disable"
        depends_on:
          - db
          - prometheus
        ports:
          - "9187:9187"

    volumes:
      postgres_data:
      grafana_data:`

2.  **Prometheus Configuration:** The `prometheus.yml` file defines the scrape configurations and how Prometheus collects metrics from various sources.

 
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

**Metrics and Queries:**

Here are some queries you can use in Prometheus to view different metrics:

1.  **CPU Usage:**

    -   **Query:**
        `rate(node_cpu_seconds_total{mode="idle"}[5m])`

    -   **Description:** This query shows the rate of CPU idle time over the past 5 minutes. To find the CPU usage, you would subtract this from 1 (or 100% if expressed as a percentage).
2.  **Memory Usage:**

    -   **Query:**

        `(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes`

    -   **Description:** This query calculates the memory usage as a percentage of total memory.
3.  **HTTP Requests:**

    -   **Query:**

        `flask_http_request_total`

    -   **Description:** This query shows the total number of HTTP requests handled by your Flask application.
4.  **PostgreSQL Metrics:**

    -   **Query:**

        `pg_stat_activity_count`

    -   **Description:** This query shows the number of active PostgreSQL connections.
5.  **Node Exporter Metrics (System Metrics):**

    -   **Query:**

        `node_disk_io_time_seconds_total`

    -   **Description:** This query provides the total disk I/O time for the node.

**How It Works:**

1.  **Scraping Metrics:** Prometheus scrapes metrics from the application, database, and system exporters (Node Exporter for system metrics and PostgreSQL Exporter for database metrics) based on the `scrape_configs` defined in `prometheus.yml`.

2.  **Storing Data:** The metrics are stored in Prometheus' time-series database. This allows for historical data analysis and querying.

3.  **Querying Metrics:** Use Prometheus' query language (PromQL) to extract and analyze metrics data. These queries can be used in Grafana dashboards to visualize data and set up alerts based on predefined conditions.

4.  **Alerting:** Alerts are set up in Prometheus using the `alert.rules.yml` file, which defines the conditions for firing alerts. These alerts can be routed to notification systems like Microsoft Teams via Grafana.

This setup ensures that you have comprehensive monitoring and alerting for your application, system, and database, helping you proactively manage and maintain system health.
