# async_model_server

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Logging](#logging)
- [License](#license)
- [Contact](#contact)

## Project Overview

`async_model_server` is an asynchronous model server application that utilizes ZeroMQ for inter-process communication and asyncio for managing asynchronous tasks. The application handles configuration through a JSON file, manages message routing between processes, and supports graceful shutdown, ensuring robust operation and clean exit.

## Features

- **Asynchronous Processing**: The application uses `asyncio` to handle multiple tasks concurrently, allowing efficient non-blocking operations.
- **Inter-Process Communication**: ZeroMQ is utilized to facilitate high-performance messaging between different parts of the application.
- **Configuration Management**: The application settings, such as ports for ZeroMQ, are managed via a JSON configuration file.
- **Graceful Shutdown**: The application supports smooth shutdown processes, ensuring all tasks and connections are properly terminated.
- **Logging**: Comprehensive logging is provided to track the application's activities and errors.

## Installation

To set up the `async_model_server` application, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Thando12345/async_model_server.git
   cd async_model_server



2. Set Up a Virtual Environment (Recommended)

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install Dependencies

Install the required Python packages using the provided requirements.txt.

pip install -r requirements.txt

## Configuration

The application's configuration is managed through a JSON file located at config/config.json. This file specifies the ports used by ZeroMQ for communication.

Example Configuration (config/config.json)

{
    "request_port": 60658,
    "response_port": 60659
}

## Usage

1. Starting the Model Server

The model server process listens for requests and processes them.
python model_server/ai_model_server.py

2. Starting the Main Application

Start the main application that handles ZeroMQ communication and routing.
python app.py

3. Testing the Server

A test client script is provided to send a test request to the server and receive a response.
python examples/test_client.py


## Logging

The application logs events and errors to a log file located in the logs directory. The logging behavior can be configured in logger/logger.py.

Log File Path: logs/app.log
Log Level: Configurable in logger/logger.py

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or support, please contact:

Name: Thando Nogemane
Email: thandonogemane13@gmail.com