# Leave Request API

This is a Flask application that provides an API for submitting leave requests.

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/p67428378-afk/Leave-Request.git
   ```
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a PostgreSQL database.
4. Set the `DATABASE_URL` environment variable to the database connection string.
5. Run the application:
   ```
   flask run
   ```

## API

### Submit Leave Request

- **Endpoint**: `POST /api/leaves/apply`
- **Method**: `POST`
- **Payload**:

  ```json
  {
    "employee_id": "string",
    "start_date": "MM/DD/YYYY",
    "end_date": "MM/DD/YYYY",
    "leave_type": "string"
  }
  ```

- **Success Response**:

  ```json
  {
    "message": "Leave request submitted successfully.",
    "request_id": "string",
    "status": "Pending",
    "days_requested": "integer",
    "remaining_balance": "integer"
  }
  ```

- **Error Response**:

  ```json
  {
    "error": {
      "code": "string",
      "message": "string"
    }
  }
  ```
