# py-crawler

This project is a Flask web application that captures screenshots of web pages. It uses Selenium for web scraping and screenshot capturing.

## Features

- **GET /isalive**: Endpoint for checking the server health.
- **POST /screenshots**: Endpoint to start the process of web page crawling and taking screenshots.
- **GET /screenshots/:id**: Endpoint to fetch the collected screenshots for a given task ID.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9 or higher
- pip
- Docker (optional, for running within a container)

### Installing

1. Clone the repository:

   ```sh
   git clone https://your-repository-url.git
   ```

2. Install the dependencies

   ```sh
   pip install -r requirements.txt
   ```

3. Start the app

   ```sh
   python app.py
   ```

### Running with Docker

1. Build the Docker image

   ```sh
   docker build -t py-crawler .
   ```

2. Run the container

   ```sh
   docker run -d -p 5000:5000 py-crawler
   ```

## Usage

1. Send a POST request to /screenshots with JSON payload containing start_url and number_of_links.
2. Use the returned task_id to fetch screenshots with a GET request to /screenshots/:id.

## Future improvements

1. Asynchronous Processing:
   Currently, screenshots are taken in a separate thread, but for better scalability, consider using asynchronous task queues like Celery with Redis or RabbitMQ as the message broker. This approach allows you to handle multiple screenshot tasks concurrently without blocking your main application thread.

2. Load Balancing:
   As traffic increases, use a load balancer (like Nginx or HAProxy) in front of your application to distribute requests efficiently across multiple instances of your application.

3. Optimize Selenium WebDriver Usage:
   Managing WebDriver instances efficiently is crucial. Consider using a pool of pre-initialized WebDriver instances to reduce the overhead of starting and stopping a browser for each task.

4. Image Compression:
   Apply image compression techniques to reduce the size of screenshots. This reduces storage requirements and bandwidth usage when transmitting these images.

5. Caching Mechanism:
   Implement caching for frequently accessed screenshots. Tools like Redis can be used for fast in-memory caching.

6. Application Performance Monitoring (APM) Tools:
   Use APM tools like New Relic, Datadog, or Prometheus with Grafana for monitoring your application's performance.

7. Key Metrics:
   Response Times: Monitor the response times of your endpoints.
   Error Rates: Keep track of any failed requests or application errors.
   System Resources: Monitor the CPU, memory, and disk usage of your servers.
   Queue Length: For asynchronous task processing, monitor the length of the task queues.

8. Logging:
   Implement comprehensive logging throughout the application. Tools like ELK Stack (Elasticsearch, Logstash, Kibana) or Graylog can help in centralizing and analyzing logs.

9. Database Scalability:
   If using a relational database, ensure it is properly indexed and consider read replicas for scaling. For non-relational workloads, NoSQL databases like MongoDB or Cassandra might be more suitable.
