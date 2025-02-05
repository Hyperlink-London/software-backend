# Hyperlink-backend


This project, hyperlink-api, is a Python-based API designed to interface with hyperlink databases. It leverages the FastAPI and SQLModel libraries to provide a set of endpoints for managing and interacting with the data defined in the hyperlink_data_models. The API supports CRUD operations, allowing users to create, read, update, and delete data related to data defined in the hyperlink_data_models.

## Overview

hyperlink-api is a Python-based API designed to interface with hyperlink databases. It provides a set of endpoints to interact with data defined in the hyperlink_data_models.

You can install `hyperlink-api` via git:

    ```bash
    git clone https://github.com/Hyperlink-London/hyperlink-backend.git
    cd hyperlink-backend
    ```
    
    then build the docker compose (this will also then run the compose) (you should install docker [here](https://www.docker.com/products/docker-desktop/))
    
    ```bash
    docker compose up --build
    ```
    
    ## To run
    
    You can run the Hyperlink backend by running:
    
    ```bash
    docker compose up
    ```

## Sensor Data Information
### Breaking
- Temperature

### Propulsion
- Temperature
- Speed
- Acceleration

### Structures
- Temperature
- Vibrations
- Deformation
