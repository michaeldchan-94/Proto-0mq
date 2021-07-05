"""
This is the python implementation of a 0mq/protobuf comm stack client
"""

import zmq
from Protobuf_Messages import DataMessage_pb2

class Client:
    def __init__(self):
        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.REQ)

    def connect(self,port):
        print("Connecting to hello world server…")
        self.sock.connect("tcp://127.0.0.1:" + str(port))
        return True

    def send(self,msg):
        self.sock.send(msg)
        return True

    def recieve(self):
        msg = self.sock.recv()
        return msg

    def kill(self):
        self.sock.close()
        self.ctx.term()
        return True

if __name__ == "__main__":
    print("Created Client")
    example_client = Client()
    example_client.connect(5678)

    for i in range(10):
        # Create the data message envelope
        example_request = DataMessage_pb2.DataMessage()
        example_request.Message_Name = "Example Message Request"

        # Create an example data frame
        example_data_frame = DataMessage_pb2.DataFrame()
        example_data_frame.string_data.append("Request: " + str(i))
        example_data_frame.data.append(i)

        # Append the data frame to the data envelope
        example_request.Message_Data.append(example_data_frame)

        # Send the data message across as a serialized byte string
        example_client.send(example_request.SerializeToString())
        print("Data Requested")

        example_response = DataMessage_pb2.DataMessage()
        return_msg = example_client.recieve()
        example_response.ParseFromString(return_msg)
        print("Data Received: " + example_response.Message_Data[0].string_data[0])

    example_client.kill()





