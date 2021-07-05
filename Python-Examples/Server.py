"""
This is the python implementation of a 0mq/protobuf comm stack server
"""

import zmq
from Protobuf_Messages import DataMessage_pb2
import time

class Server:
    def __init__(self,port):
        self.port = port
        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.REP)
        self.sock.bind("tcp://*:" + str(port))
        self.run_state = True
        self.count = 0

    def run(self):
        while self.run_state:
            client_msg = DataMessage_pb2.DataMessage()
            msg = self.sock.recv()
            client_msg.ParseFromString(msg)
            print("Received request")

            #Do work
            time.sleep(1)

            # Create the data message envelope
            example_msg = DataMessage_pb2.DataMessage()
            example_msg.Message_Name = "Example Message"
            example_msg.Message_ID = str(self.count)

            # Create an example data frame
            example_data_frame = DataMessage_pb2.DataFrame()
            example_data_frame.string_data.append("Hello World: " + str(self.count))
            example_data_frame.data.append(self.count)

            # Append the data frame to the data envelope
            example_msg.Message_Data.append(example_data_frame)

            # Send the data message across as a serialized byte string
            self.sock.send(example_msg.SerializeToString())
            self.count += 1

    def kill(self):
        self.sock.close()
        self.ctx.term()
        return True

if __name__ == "__main__":
    print("Starting Server")
    example_server = Server(5678)
    example_server.run()


