import threading
import queue
import server
import gui
import database


# def main() -> None:
in_server_queue : queue.Queue = queue.Queue()
out_server_queue : queue.Queue = queue.Queue()
database_queue : queue.Queue = queue.Queue()
server_event : threading.Event = threading.Event()
database_event : threading.Event = threading.Event()


app = gui.App(database_queue)
server_thread = threading.Thread(target=server.wrapper, args=((in_server_queue, out_server_queue), server_event))    
database_thread = threading.Thread(target=database.main, args=((in_server_queue, out_server_queue), database_queue, app.table, database_event))
try:
    database_thread.start()
    server_thread.start()
    app.run()
except KeyboardInterrupt:
    print("stopped")
finally:
    database_event.set()
    server_event.set()
    database_thread.join()
    server_thread.join()

# if __name__ == "__main__":
#     main()