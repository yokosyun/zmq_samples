import zmq
import time


def publisher():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")
    sequence_number = 0
    while True:
        message = f"{sequence_number}"
        socket.send_string(message)
        print("send:", message)
        sequence_number += 1
        time.sleep(1)


def subscriber():
    context = zmq.Context()

    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.CONFLATE, 1) # Set buffer size = 1
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        message = socket.recv_string()
        print("received:", message)
        time.sleep(5)


if __name__ == "__main__":
    import threading

    publisher_thread = threading.Thread(target=publisher)
    subscriber_thread = threading.Thread(target=subscriber)

    publisher_thread.start()
    subscriber_thread.start()

    publisher_thread.join()
    subscriber_thread.join()
