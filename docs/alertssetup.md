### Setting Up Alerting on Teams

**Overview:** To monitor our application effectively, we've set up alerting in Grafana for CPU usage and HTTP request hits. Notifications are sent to a Microsoft Teams channel when these alerts are triggered.

**Steps to Set Up Alerts:**
![image](https://github.com/user-attachments/assets/5acc5ce2-0d72-4fe3-9768-7855a6339cd1)


1.  **Create Alerts in Grafana:**

    -   **CPU Usage Alert:**
        -   **Query:** `rate(node_cpu_seconds_total{mode="idle"}[5m]) < 0.2`
        -   **Description:** Triggers when CPU usage is above 80% for 5 minutes.
    -   **HTTP Request Hits Alert:**
        -   **Query:** `flask_http_request_total`
        -   **Description:** Triggers based on HTTP request status codes.
2.  **Configure Contact Points:**

    -   **Go to Grafana Alerting > Contact Points.**
    -   **Create a new contact point for Microsoft Teams using the webhook URL provided by Teams.**
      ![image](https://github.com/user-attachments/assets/a15810c4-d28e-4452-a46d-0f13c981f17a)


    `Webhook URL: https://teams/webhook/your-webhook-url`

3.  **Set Up Notification Policies:**

    -   **Go to Grafana Alerting > Notification Policies.**
    -   **Create or update a policy to route alerts to the Teams contact point.**
      ![image](https://github.com/user-attachments/assets/bb4975a4-5e22-474f-93dd-4dac73c481a1)

4.  **Verify Alerts:**

    -   **Ensure that alerts are firing correctly in Grafana.**
    -   **Check that notifications are received in your Microsoft Teams channel.**
    ![image](https://github.com/user-attachments/assets/852bb847-7c08-4ec9-b3e4-396a15f98188)

    ![image](https://github.com/user-attachments/assets/c0c1e58c-2e89-4d10-98d0-e4bbcd99fe4a)


**Code and Query Examples:**

-   **CPU Usage Alert Query:**

    `alert: HighCPUUsage
    expr: rate(node_cpu_seconds_total{mode="idle"}[5m]) < 0.2
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High CPU usage detected"
      description: "CPU usage has been above 80% for the last 5 minutes."`

-   **HTTP Request Hits Alert Query:**

    `alert: HTTP_REQUEST
    expr: flask_http_request_total
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "High number of HTTP requests detected"
      description: "Number of HTTP requests has exceeded the threshold."`

This setup ensures that any critical issues with CPU usage or HTTP requests are promptly communicated to the relevant team via Microsoft Teams.
