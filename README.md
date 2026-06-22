# Restaurant Operations Data Backend

Backend API for a restaurant operations data collection platform. The system gathers structured operational data that will later be processed through an ETL pipeline and used for data analysis.

This project is part of a **personal data engineering and data science project** focused on building a complete pipeline:

**Data collection** $\to$ **ETL** $\to$ **Analytical dataset**

## Getting Started
### Prerequisites
- Python 3.10 or higher
- Redis 7.0 or higher
- Git (optional)

### Quick Installation & Run

Follow these steps to get the backend up and running locally in just a few minutes:

1. **Clone the repository**

    ```bash
    git clone https://github.com/GenisPT/backend_f6b81ce5-51ac
    cd backend_f6b81ce5-51ac
    ```

    Replace ```your-username``` with your actual GitHub username. If you don't have **Git**, download this repository as zip from the green **Code** button located at the main page of the repo.

2. **Create and activate a virtual environment**

    ```bash
    python -m venv venv

    # On Windows:
    venv\Scripts\activate

    # On macOS/Linux:
    source venv/bin/activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Start Redis**
    
    Make sure Redis is installed and running before starting the API.

    Running example on Docker:

    ```bash
    docker run -d --name redis -p 6379:6379 redis:latest
    ```

    If Redis is installed locally, it can be started using:

    ```bash
    redis-server
    ```

5. **Run the FastAPI server**
    
    Uvicorn command with auto-reload (```--reload```) for development:
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```
    
    You may want to change port ```8000``` to another one of your choice...

    Also if you want to use more than 1 worker, you can specify the number of workers using ```--workers``` flag, for example ```--workers 4```.

### API Documentation & Interactive Testing

As this projects uses **FastAPI**, interactive API documentation is automatically generated, and is accessible at:
- **Swagger UI** — http://localhost:8000/docs
- **ReDoc** — http://localhost:8000/redoc

If you have changed ```--port 8000``` to set another port, remember to also change it here.

## Overview

The backend manages operational entities such as:
- Tables
- Menu items
- Orders and Tickets
- Kitchen operations
- Users and Sessions
- Notifications
- Licenses

Data is stored in a **NoSQL Aggregation Database** called **Redis**, using ```key-value``` pairs as a data storage element. This, provides fast in-memory access, shared state across processes, and better scalability for real-time restaurant operations.

The collected data will later be transformed into a structured dataset for analysis.

*Redis was chosen instead of file-based JSON storage (as it was initially done), because it provides a centrallized data sotre that can be safely shared accross multiple FastAPI workers and application instances.*

## Tech Stack

#### Backend
- Python
- FastAPI
- Pydantic models

#### Communication
- REST API
- WebSockets (real-time updates)

#### Storage
- Redis
- JSON-based persistence (for DB backups)

#### Future Data Pipeline
- Pentaho Data Integration (Spoon) for ETL
- Python / Pandas module for analysis

# Architecture

The system follows a simple operational data pipeline architecture.

            Restaurant Staff
                   │
                   ▼
           Flutter Mobile App
                   │
                   ▼
            FastAPI Backend
                   │
                   ▼
              Redis Store
                   │
                   ▼
       ETL Pipeline (PDI - Spoon)
                   │
                   ▼
           Analytical Dataset
                   │
                   ▼
    Data Analysis / Machine Learning

## Key Features

### Generic CRUD API

The backend implements a generic system capable of managing multiple entity types using the same endpoints.

Supported collections include:
- Tables
- Items
- Client Items
- Kitchens
- Tickets
- Ticket Items
- Users
- Sessions
- Notifications
- Licenses

---

### Real-Time Updates

Clients can subscribe to a WebSocket endpoint to receive notifications when collections change. This enables real-time synchronization between the backend and the frontend application.

---

### Authentication

Basic authentication system including:
- Password hashing (SHA-256)
- Session management
- Session expiration (checked primarily in application code)

## API Example

Basic endpoints:

```
GET /ping
GET /fetch/{collectionID}/{id}/{sessionID}/{authToken}
POST /create/{collectionID}/{sessionID}/{authToken}
PUT /update/{collectionID}/{sessionID}/{authToken}
DELETE /remove/{collectionID}/{id}/{sessionID}/{authToken}
```

Authentication:

```
GET /login/{userID}/{password}
GET /logout/{sessionID}/{authToken}
PUT /changepasswd/{userID}/{sessionID}/{oldPasswd}/{newPasswd}/{authToken}
```

Note that ```validateOperation(sessionID, authToken)``` is what determines the validity of the queries made. It checks that the ```authToken``` value given is valid for the corresponding session. In this repo, the function will always return **True** to avoid creating valid users and sessions, and to be able to test the API without complications.

## Example Data

Example operational records are available in the 'example_data/' folder.

These represents the type of structured data collected during restaurant operations, including:

- Timestamps
- Table usage
- Ordered items
- Number of people
- Contextual information (weather, time, etc.)

## Data Pipeline (Planned)

The collected data will be processed through an ETL pipeline.

#### Steps

1. **Extract**

    Operational data stored in Redis (pulling it and saving as JSON, ...)

2. **Transform**

    Cleaning, feature extraction and restructuring

3. **Load**

    Structured dataset for analysis

Target dataset size: **~2000-4000 operational records (tickets)**

## Project Status

Current progress:
- ✅ Backend API
- ✅ Flutter frontend
- ✅ Real-time system
- ⏳ Data collection
- ⏳ ETL pipeline

## Purpose

This project was developed to practise:
- Backend system design
- Real-time APIs
- Data collection pipelines
- Data engineering workflows

The goal is to simulate the **full lifecycle of a real-world data project**.

## Future Analysis

The collected dataset will be used to explore questions such as:
- Peak demand prediction
- Table turnover analysis
- Item popularity and association
- Demand forecasting
- Weather impact on restaurant activity
