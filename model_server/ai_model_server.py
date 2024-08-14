import zmq
import zmq.asyncio
import asyncio
import json
from multiprocessing import Process

class ModelServer(Process):
    def __init__(self, request_port, response_port):
        # Initialize the Process class with the given ports for request and response
        super().__init__()
        self.request_port = request_port
        self.response_port = response_port

    def run(self):
        # Create an asynchronous ZeroMQ context
        context = zmq.asyncio.Context()
        
        # Create a PULL socket to receive requests
        request_socket = context.socket(zmq.PULL)
        try:
            # Bind the request socket to the specified port
            request_socket.bind(f"tcp://127.0.0.1:{self.request_port}")
        except zmq.error.ZMQError as e:
            # Log an error if binding fails
            print(f"Failed to bind request socket: {e}")
            return
        
        # Create a PUSH socket to send responses
        response_socket = context.socket(zmq.PUSH)
        try:
            # Bind the response socket to the specified port
            response_socket.bind(f"tcp://127.0.0.1:{self.response_port}")
        except zmq.error.ZMQError as e:
            # Log an error if binding fails
            print(f"Failed to bind response socket: {e}")
            # Close the request socket before returning
            request_socket.close()
            return

        async def process_requests():
            while True:
                try:
                    # Asynchronously receive a JSON request
                    request = await request_socket.recv_json()
                    
                    # Check if the request is a shutdown signal
                    if request.get("request_id") == "INTERNAL_EXIT":
                        # Send a shutdown response and exit the loop
                        await response_socket.send_json({"response": "INTERNAL_EXIT"})
                        break
                    
                    # Simulate some processing with a sleep
                    await asyncio.sleep(1)
                    
                    # Create a response based on the request
                    response = {"response": "processed", "data": request}
                    # Send the response asynchronously
                    await response_socket.send_json(response)
                
                except zmq.error.ZMQError as e:
                    # Handle ZeroMQ-related errors
                    print(f"ZMQ Error: {e}")
                    break
                except json.JSONDecodeError as e:
                    # Handle JSON decoding errors
                    print(f"JSON Decode Error: {e}")
                    break
                except asyncio.CancelledError:
                    # Handle cancellation of the asynchronous task
                    print("Processing task was canceled")
                    break
        
        try:
            # Run the async function to process requests
            asyncio.run(process_requests())
        finally:
            # Close sockets and terminate the context when done
            request_socket.close()
            response_socket.close()
            context.term()
