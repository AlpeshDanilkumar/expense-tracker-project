### Explanation of Ports Used in the Project

#### 1\. **Port 5000: Flask Application**

-   **Purpose:** This is the default port for the Flask web server running your expense tracker application.
-   **How It Works:** The Flask app listens for HTTP requests on this port. When users interact with the application (e.g., viewing or adding expenses), these requests are handled by the Flask server.
-   **Configuration:** Mapped in the `docker-compose.yml` as `"5000:5000"` to expose the container's port 5000 to the host's port 5000.

#### 2\. **Port 5432: PostgreSQL Database**

-   **Purpose:** This is the default port used by PostgreSQL for database communication.
-   **How It Works:** The Flask application connects to the PostgreSQL database using this port to store and retrieve expense records.
-   **Configuration:** The port is used internally within Docker Compose but is not exposed externally in this setup.

#### 3\. **Port 9090: Prometheus**

-   **Purpose:** This port is used by Prometheus for its web UI and API.
-   **How It Works:** Prometheus scrapes metrics from configured targets (like your Flask app and PostgreSQL exporter) and provides a web interface for querying and viewing these metrics.
-   **Configuration:** Mapped in the `docker-compose.yml` as `"9090:9090"` to expose Prometheus' web UI to the host's port 9090.

#### 4\. **Port 3000: Grafana**

-   **Purpose:** This port is used by Grafana for its web UI.
-   **How It Works:** Grafana provides dashboards and visualizations for the metrics collected by Prometheus. Users can access these dashboards through the Grafana web interface.
-   **Configuration:** Mapped in the `docker-compose.yml` as `"3000:3000"` to expose Grafana's web UI to the host's port 3000.

#### 5\. **Port 9100: Node Exporter**

-   **Purpose:** This port is used by the Node Exporter to expose system metrics.
-   **How It Works:** The Node Exporter runs on the host and exposes metrics about the system's hardware and OS, which Prometheus scrapes.
-   **Configuration:** Mapped in the `docker-compose.yml` as `"9100:9100"` to expose the Node Exporter's metrics endpoint to Prometheus.

#### 6\. **Port 9187: PostgreSQL Exporter**

-   **Purpose:** This port is used by the PostgreSQL Exporter to expose PostgreSQL-specific metrics.
-   **How It Works:** The PostgreSQL Exporter collects metrics from PostgreSQL and exposes them to Prometheus.
-   **Configuration:** Mapped in the `docker-compose.yml` as `"9187:9187"` to expose the PostgreSQL Exporter's metrics endpoint to Prometheus.

#### Summary of Port Configuration

-   **Flask Application (5000):** For handling web traffic related to the expense tracker.
-   **PostgreSQL Database (5432):** For internal communication between the Flask app and the database.
-   **Prometheus (9090):** For monitoring and querying collected metrics.
-   **Grafana (3000):** For visualizing metrics and creating dashboards.
-   **Node Exporter (9100):** For exposing system metrics to Prometheus.
-   **PostgreSQL Exporter (9187):** For exposing PostgreSQL metrics to Prometheus.

This configuration ensures that each component of your system is accessible and communicates effectively with other components and external interfaces.
