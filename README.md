# Restaurant Operations Data Backend

Backend API for a restaurant operations data collection platform. The system gathers structured operational data that will later be processed through an ETL pipeline and used for data analysis.

This project is part of a **personal data engineering and data science project** focused on building a complete pipeline:

**Data collection** $\to$ **ETL** $\to$ **Analytical dataset**

## Getting Started
### Prerequisites
- Python 3.10 or higher
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

4. **Run the FastAPI server**
    
    Uvicorn command with auto-reload (```--reload```) for development:
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```
    
    You may want to change port ```8000``` to another one of your choice...

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

Data is stored in **JSON collections loaded into memory**, allowing extremely fast access for real-time restaurant operations.

The collected data will later be transformed into a structured dataset for analysis.

## Tech Stack

#### Backend
- Python
- FastAPI
- Pydantic models

#### Communication
- REST API
- WebSockets (real-time updates)

#### Storage
- JSON-based persistence

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
        JSON Operational Storage
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
GET /fetch/{collectionID}/{id}
POST /create/{collectionID}
PUT /update/{collectionID}
DELETE /remove/{collectionID}/{id}
```

Authentication:

```
GET /login/{userID}/{password}
GET /logout/{sessionID}
PUT /changepasswd/{userID}/{oldPasswd}/{newPasswd}
```

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

    Raw JSON operational data

2. **Transform**

    Cleaning, feature extraction and restructuring

3. **Load**

    Structured dataset for analysis

Target dataset size: **~800-1000 operational records**

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
