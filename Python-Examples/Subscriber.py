"""
This is the python implementation of a 0mq/protobuf comm stack Subscriber
"""

import zmq
from Protobuf_Messages import DataMessage_pb2

class Subscriber:
    def __init__(self,port,topic):
        self.topic = topic
        self.port = port
        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.SUB)
        self.sock.connect("tcp://127.0.0.1:" + str(port))
        self.sock.subscribe(topic)

    def read(self):
        topic = self.sock.recv()
        msg = self.sock.recv()
        return topic,msg

    def kill(self):
        self.sock.close()
        self.ctx.term()
        return True

if __name__ == "__main__":
    print("Starting Subscriber")
    sub = Subscriber(5678,"Example Topic")
    while(True):
        recv_msg = DataMessage_pb2.DataMessage()

        topic,msg = sub.read()
        recv_msg.ParseFromString(msg)

        print("Got message: " + recv_msg.Message_Data[0].string_data[0])
