
import queue
import sys
import socket
import selectors
import types
import part as part
from threading import Thread, Event
import os
import multiprocessing
import time

# temp_part = part.Part(
#     "00796889",
#     "test_part",
#     "1THz, 56ohm",
#     "air tag",
#     "69420520",
#     "www.github.com",
#     ["www.github.com"],
# )

# yeah i know great database
# database = {}

# database.setdefault(
#     "00796889",
#     temp_part
# )

sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask, in_queue : queue.Queue, out_queue : queue.Queue):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            current_part_UID = ''.join('{:02x}'.format(x) for x in recv_data)
            # print(f"{current_part_UID=}")
            # print(f"{id(queue)=}")
            out_queue.put(current_part_UID, True)
            print("waiting")
            while in_queue.empty(): time.sleep(0.1)
            print("waited")
            p = in_queue.get()
            data.outb += p.make_packet()
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            # print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

def init_socket():
    print(f"server starting on {os.getpid()}")
    global sel
    host, port = (socket.gethostbyname(socket.gethostname()) , 2332)
    lsock : socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen()
    print(f"Listening on {(host, port)}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

should_stop = False

def main(q : tuple[queue.Queue, queue.Queue], event: Event):
    global sel
    try:
        while not event.isSet():
            if should_stop: break;
            events = sel.select(timeout=1)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask, *q)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()

def wrapper(q : tuple[queue.Queue, queue.Queue], event: Event):
    print(f"wrapper {id(q)=}")
    init_socket()
    main(q, event)


# if __name__ == "__main__":
#     init_socket()
#     main()

