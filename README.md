# Fast API Project

A FastAPI application for building modern APIs with Python.

This project is build to learn FastAPI, a Python framework. It exposes several dummy APIs just for testing.

## Project Structure

```
fast-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   └── services/
│       ├── __init__.py
│       └── data_modification.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/klemontea/fast-api.git
cd fast-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## API Endpoints

### 1. **GET /** 
Root endpoint that returns a welcome message.

### 2. **POST /modify-data** 
Modify source file data using reference file mapping. This endpoint performs data transformation by applying a reference mapping table to a target column in the source file.

**Request Parameters (multipart/form-data):**
- `source_file` (file): Excel file containing the data to be modified
  - Must have headers in the first row
- `reference_file` (file): Excel file with mapping rules
  - Must contain 3 columns: `KEY`, `AS-IS`, `TO-BE`
  - `KEY`: Mapping identifier (used to filter which mappings to apply)
  - `AS-IS`: Original value to find in the target column
  - `TO-BE`: New value to replace the original value with
- `key` (string): The mapping key to filter the reference file
- `target` (string): The column name in the source file to apply the mapping

**Example:**
```
POST /modify-data
- source_file: data.xlsx (contains columns like "Status", "Category", etc.)
- reference_file: mapping.xlsx (contains KEY, AS-IS, TO-BE columns)
- key: "status_mapping"
- target: "Status"
```

**Response:**
- Success: Returns the modified Excel file as a download
- Error: Returns JSON with error message and available options

**Example Use Case:**
If your source file has a "Status" column with values like "Active", "Inactive", and your reference file has mappings for key "status_mapping" that map "Active" → "Yes" and "Inactive" → "No", this endpoint will return a modified file with the transformations applied.

## Requirements

See `requirements.txt` for the list of dependencies.

## Testing

I prefer to use Postman to test the APIs. If you want to use it, you must download Postman first.
Alternatively, you can test the APIs via http://localhost:8000/docs. It is more simpler, but has limited capabilities compared to Postman.