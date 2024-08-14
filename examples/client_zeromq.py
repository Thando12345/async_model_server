import zmq
import json
import time

def main():
    context = zmq.Context()
    
    # Create and connect request socket
    request_socket = context.socket(zmq.PUSH)
    request_socket.connect("tcp://127.0.0.1:60658")  # Port for sending requests
    
    # Create and connect response socket
    response_socket = context.socket(zmq.PULL)
    response_socket.connect("tcp://127.0.0.1:60659")  # Port for receiving responses
    
    # Prepare and send request
    request = {"request_id": "1234", "type": "training", "data": "data"}
    request_socket.send_json(request)
    print(f"Request sent: {request}")
    
    # Allow time for the server to process and send a response
    time.sleep(1)  # Sleep for 1 second to give the server time to respond
    
    # Receive and print response
    try:
        response_socket.setsockopt(zmq.RCVTIMEO, 5000)  # Set timeout to 5 seconds
        message = response_socket.recv()  # Receive message
        response = json.loads(message)  # Decode JSON
        print(f"Received response: {response}")
    except zmq.Again:
        print("No response received within timeout")
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")

    # Cleanup
    request_socket.close()
    response_socket.close()
    context.term()

if __name__ == "__main__":
    main()
