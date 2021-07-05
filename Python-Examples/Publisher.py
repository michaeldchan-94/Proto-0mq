"""
This is the python implementation of a 0mq/protobuf comm stack publisher
"""

import zmq
from Protobuf_Messages import DataMessage_pb2

class Publisher:
    def __init__(self, port, topic):
        self.topic = topic
        self.port = port
        ctx = zmq.Context()
        self.sock = ctx.socket(zmq.PUB)
        self.sock.bind("tcp://*:" + str(port))

    def send(self,msg):
        self.sock.send_string(self.topic,flags=zmq.SNDMORE)
        self.sock.send(msg)
        return True

if __name__ == "__main__":
    print("Staring Publisher")
    pub = Publisher(5678,"Example Topic")
    count = 0

    while(True):
        # Create the data message envelope
        example_msg = DataMessage_pb2.DataMessage()
        example_msg.Message_Name = "Example Message"
        example_msg.Message_ID = "Example ID"

        # Create an example data frame
        example_data_frame = DataMessage_pb2.DataFrame()
        example_data_frame.string_data.append("Hello World: " + str(count))
        example_data_frame.data.append(0)

        # Append the data frame to the data envelope
        example_msg.Message_Data.append(example_data_frame)

        # Send the data message across as a serialized byte string
        pub.send(example_msg.SerializeToString())
        count += 1