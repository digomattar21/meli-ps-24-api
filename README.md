# Ticket Management API

## Overview

This project is a Ticket Management API built with Python and Flask. It provides CRUD operations for tickets and categories, integrates with an external API for user management, and ensures data integrity through validation. 

## Installation and Setup

### Prerequisites

- **Python 3.11** or higher
- **Docker** and **Docker Compose**

### Clone the Repository

1. **Clone the repository**:

   ```bash
   git clone https://github.com/digomattar21/meli-ps-24-api
   cd your-repository
   ```

### Create a Virtual Environment

(Optional but recommended)

1. **Create the virtual environment**:

   ```bash
   python3 -m venv venv
    ```

2. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```

3. Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Run the Application with Docker Compose
    
 1. Build the containers: 

    ```bash
    docker-compose up --build
    ```

2. Acess the applcation

    The application should now be running and accessible. Typically, you can access it via http://localhost:5000 in your browser.


### Running tests

1. Ensure the Docker containers are running:

    ```bash
     docker-compose up
     ```

2. Run the tests:
    ```bash
    docker-compose run --rm web pytest
    ```

### Functionalities

- **CRUD Operations**: Provides Create, Read, Update, and Delete operations for tickets and categories.

- **External API Integration**: Integrates with JSONPlaceholder API to assign tickets to users based on external user IDs.

- **PostgreSQL Integration**: Uses PostgreSQL as the database to persist ticket, category and severity data.

- **Data Seeding**: Includes initial seed functionalities to populate the database with default categories, severities, and tickets.

- **Validation**: Ensures data integrity by validating category-subcategory relationships, severity levels, and other constraints.

- **Middleware**: Validates incoming requests before they reach the controller to ensure data integrity and security.

### Automated Testing with GitHub Actions

- **Continuous Integration**: GitHub Actions automatically runs tests on every push to the repository, ensuring stability and preventing errors from being introduced.

- **Test Suite**: Automated unit and integration tests, executed with `pytest`, cover essential parts of the application like controllers, gateways, models, and middleware.

- **Pre-commit Hooks**: `black`, `flake8`, and `isort` are configured as pre-commit hooks to enforce code formatting and linting before commits, maintaining consistent code quality.


- **GitHub Actions Configuration**: The CI pipeline is configured in the `.github/workflows/` directory. It automatically:
  - Sets up the environment with the required dependencies.
  - Runs the test suite using `pytest`.
  - Checks code formatting and linting with `black`, `flake8`, and `isort`.
  - Reports any issues or failures directly on the pull request or commit status.


### Unit and Integration Tests

The project includes both unit and integration tests to ensure the functionality and reliability of the application:

- **Unit Tests**: 
  - Unit tests on major funcitons, models, services and middlemans

- **Integration Tests**: 
  - Integration test covering controllers and gateways 


### Monitoring and Analysis Metrics
1. Metrics for the Datadog Dashboard

- Request Success Rate (HTTP Status Codes): Track the success of requests made to the application by monitoring the proportion of 2xx (success), 4xx (client errors), and 5xx (server errors) status codes over time.

- Request Latency: Measure the average response time of requests, including percentiles (p50, p95, p99), to ensure response times are within acceptable limits.

- Error Rate: Monitor the application's error rate (unhandled exceptions, database failures, etc.) to identify issues that affect system stability.

- Request Throughput (Requests Per Second - RPS): Analyze the number of requests per second to identify traffic spikes and assess infrastructure capacity.

- Resource Usage (CPU, Memory, I/O): Track CPU, memory, and disk usage on servers to ensure the infrastructure can handle the application's load without performance degradation.

- Database Metrics: Include query execution times, cache hit rates, and active connections to ensure the database is operating efficiently.

- Availability Metrics (Uptime): Monitor the application's availability, including downtime and outages, to ensure SLA compliance.

2. Metrics for New Relic

- Apdex Score: Measure user satisfaction with the application's performance.

- Transaction Response Time: Analyze the average and maximum response times of the application's critical transactions to identify potential bottlenecks.

- Transaction Errors: Identify and monitor failed transactions, allowing for quick response to critical issues.


### API Endpoints


#### 1.  Create a Ticket

- **Endpoint**: `POST /ticket`
- **Description**: Creates a new ticket in the system.
- **Request Body**:

  ```json
    {
      "title": "Issue with VPN",
      "description": "User cannot connect to VPN",
      "severity_id": 2,
      "category_id": 1,
      "subcategory_id": 6
    }
    ```

- **Response**:
    - Success (200)
    ```json
    {
      "ticket": {
        "id": "integer",
        "title": "string",
        "description": "string",
        "severity_id": "integer",
        "category_id": "integer",
        "subcategory_id": "integer",
        "user_id": "integer",
        "created_at": "timestamp",
      }
    }
    ```


#### 2  Update a Ticket

- **Endpoint**: `PATCH /ticket/{id}`
- **Description**: Updates an existing ticket
- **Request Body**:

  ```json
        {
      "title": "string",
      "description": "string",
      "severity_id": "integer",
      "category_id": "integer",
      "subcategory_id": "integer"
    }
    ```

- **Response**:
    - Success (200)
    ```json
    {
      "ticket": {
        "id": "integer",
        "title": "string",
        "description": "string",
        "severity_id": "integer",
        "category_id": "integer",
        "subcategory_id": "integer",
        "user_id": "integer",
        "created_at": "timestamp",
      }
    }
    ```

#### 3  Delete a Ticket

- **Endpoint**: `DELETE /ticket/{id}`
- **Description**: Deletes an existing ticket
- **Response**:
    - Success (200)


#### 4  Get a Ticket By ID

- **Endpoint**: `GET /ticket/{id}`
- **Description**: Retrieves a ticket by its ID
- **Response**:
    - Success (200)
    ```json
    {
      "ticket": {
        "id": "integer",
        "title": "string",
        "description": "string",
        "severity_id": "integer",
        "category_id": "integer",
        "subcategory_id": "integer",
        "user_id": "integer",
        "created_at": "timestamp",
      }
    }
    ```


#### 5 Get All Tickets

- **Endpoint**: `GET /ticket`
- **Description**: Retrieves a ticket by its ID
- **Response**:
    - Success (200)
    ```json
    {
      "tickets": [
        {
          "id": "integer",
          "title": "string",
          "description": "string",
          "severity_id": "integer",
          "category_id": "integer",
          "subcategory_id": "integer",
          "user_id": "integer",
          "created_at": "timestamp",
        },
        
      ]
    }
    ```

#### 6.  Create a Category

- **Endpoint**: `POST /category`
- **Description**: Creates a new category
- **Request Body**:

  ```json
    {
      "name": "string",
      "parent_id": "integer"
    }
    ```

- **Response**:
    - Success (200)
    ```json
    {
      "category": {
        "id": "integer",
        "name": "string",
        "parent_id": "integer",
        "created_at": "timestamp",
      }
    }
    ```

#### 7.  Update a Category

- **Endpoint**: `PATCH /category/{id}`
- **Description**: Updates an existing category
- **Request Body**:

  ```json
    {
      "name": "string",
      "parent_id": "integer"
    }
    ```

- **Response**:
    - Success (200)
    ```json
    {
      "category": {
        "id": "integer",
        "name": "string",
        "parent_id": "integer",
        "created_at": "timestamp",
      }
    }
    ```

#### 8  Delete a Category

- **Endpoint**: `DELETE /category/{id}`
- **Description**: Deletes an existing category
- **Response**:
    - Success (200)


#### 9  Get a Category By ID

- **Endpoint**: `GET /category/{id}`
- **Description**: Retrieves a category by its ID
- **Response**:
    - Success (200)
    ```json
    {
      "category": {
        "id": "integer",
        "name": "string",
        "parent_id": "integer",
        "created_at": "timestamp",
      }
    }
    ```


#### 10 Get All Categories

- **Endpoint**: `GET /category`
- **Description**: Retrieves all categories
- **Response**:
    - Success (200)
    ```json
    {
      "categories": [
        {
          "id": "integer",
          "name": "string",
          "parent_id": "integer",
          "created_at": "timestamp",
        },
        
      ]
    }
    ```

#### 6.  Create a Severity

- **Endpoint**: `POST /severity`
- **Description**: Creates a new severity
- **Request Body**:

  ```json
    {
      "level": "integer"
    }
    ```

- **Response**:
    - Success (200)
    ```json
    {
      "severity_id": "integer"
    }
    ```

#### 7.  Update a Severity

- **Endpoint**: `PATCH /severity/{id}`
- **Description**: Updates an existing severity
- **Request Body**:

  ```json
    {
      "level": "integer"
    }
    ```

- **Response**:
    - Success (200)
    ```json
    {
      "severity": {
        "id": "integer",
        "description": "string",
        "level": "integer",
      }
    }
    ```

#### 8  Delete a everity

- **Endpoint**: `DELETE /severity/{id}`
- **Description**: Deletes an existing severity
- **Response**:
    - Success (200)


#### 9  Get a Severity By ID

- **Endpoint**: `GET /severity/{id}`
- **Description**: Retrieves a severity by its ID
- **Response**:
    - Success (200)
    ```json
    {
      "severity": {
        "id": "integer",
        "description": "string",
        "level": "integer",
      }
    }
    ```


#### 10 Get All Severities

- **Endpoint**: `GET /severity`
- **Description**: Retrieves all severities
- **Response**:
    - Success (200)
    ```json
    {
      "severities": [
        {
          "id": "integer",
          "desription": "string",
          "level": "integer",
        },
        
      ]
    }
    ```






