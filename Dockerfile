FROM python:3.12-slim

WORKDIR /app

COPY api_entrypoint.sh .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY hyperlink_data_models ./hyperlink_data_models


# Run the create_tables.py script before starting the API
CMD ["sh", "api_entrypoint.sh"]
