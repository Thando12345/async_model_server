import asyncio
import json
import signal
import sys
import zmq
from model_server.ai_model_server import ModelServer
from logger.logger import setup_logger
import keyboard  # Import the keyboard library for global hotkeys

# Set the event loop policy for Windows
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load configuration
def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

# Shutdown handler for the server
async def shutdown_handler(request_port):
    print("Shutting down...")
    context = zmq.asyncio.Context()
    request_socket = context.socket(zmq.PUSH)
    request_socket.connect(f"tcp://127.0.0.1:{request_port}")
    
    # Notify the server to shutdown
    request_socket.send_json({"request_id": "INTERNAL_EXIT"})
    await asyncio.sleep(2)  # Increased sleep time to ensure the server receives the shutdown signal
    print("Shutdown signal sent")

async def main():
    global config
    config = load_config()
    
    # Setup logging
    logger = setup_logger()
    logger.info("Model server starting...")

    # Start the model server
    model_server = ModelServer(config['request_port'], config['response_port'])
    model_server.start()
    logger.info("Model server started")

    try:
        # Run the server and wait for shutdown signal
        while model_server.is_alive():
            await asyncio.sleep(1)  # Keep the event loop running
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        logger.info("Initiating shutdown...")
        await shutdown_handler(config['request_port'])
        model_server.terminate()
        model_server.join()
        logger.info("Application stopped.")

if __name__ == "__main__":
    # Define custom shutdown function
    def custom_shutdown():
        print("Custom shutdown triggered")
        sys.exit(0)

    # Register custom hotkey
    keyboard.add_hotkey('ctrl+alt+q', custom_shutdown)

    # Handle signals for graceful shutdown
    def signal_handler(sig, frame):
        print("Signal received, shutting down...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl + C
    signal.signal(signal.SIGTERM, signal_handler)  # Handle termination signals

    # Run the main function
    asyncio.run(main())
