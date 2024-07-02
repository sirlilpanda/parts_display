from tinydb import TinyDB, Query
import json
from gui import PartTable
from part import Part
import queue
import threading

temp_part = Part(
    "00796889",
    "test_part",
    "1THz, 56ohm",
    "air tag",
    "69420520",
    "www.github.com",
    ["www.github.com"],
)

no_part_to_screen = Part(
    "n/a",
    "add part to db",
    "n/a",
    "n/a",
    "n/a",
    "n/a",
    ["n/a"],
)

# db = pickledb.load('example.db', False)

# db.set('key', str(temp_part))

# print(json.loads(db.get('key')))

# db.dump()

def main(
        server_queue : tuple[queue.Queue, queue.Queue], 
        part_queue : queue.Queue, 
        part_table: PartTable,
        thread_event : threading.Event
):
    db : TinyDB = TinyDB('database.json')
    # print(f"{id(part_queue)=}")
    # print(f"{id(server_queue)=}")

    # print(db.all())
    # print("started")
    while not thread_event.isSet():
        if not server_queue[1].empty():
            UID = server_queue[1].get()
            part_query = Query()
            print(f"form server {UID=}")
            search = db.search(part_query.UID == UID)
            if search:
                part_table.title_content.set("part lookup")
                part_table.title.config(
                    foreground="#fef3c7"
                )
                print(f"[server] found part with {UID=} | ", search[0])
                part = Part(
                    search[0]["UID"],
                    search[0]["name"],
                    search[0]["specs"],
                    search[0]["footprint"],
                    search[0]["PN"],
                    search[0]["datasheet"],
                    search[0]["supplier_links"],
                )
                server_queue[0].put(part)
                part_table.update_field_vars(part)
            else:
                print(f"adding part with {UID=}")
                server_queue[0].put(no_part_to_screen)
                part_table.title_content.set("part not in data base")
                part_table.title.config(
                    foreground="#cd1d48"
                )
                no_part = Part(
                    UID,
                    "",
                    "",
                    "",
                    "",
                    "",
                    [],
                )
                part_table.update_field_vars(no_part)
  
        if not part_queue.empty():
            data : Part = part_queue.get()
            print(f"form gui {data}")
            part_query = Query()
            if db.search(part_query.UID == data.UID):
                print(f"fount part with {data.UID=}")
                db.update(data.__dict__, part_query.UID == data.UID)
            else:
                print(f"adding part with {data.UID=}")
                db.insert(data.__dict__) 
    
    print("ended") 
    
