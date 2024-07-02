

class Part:
    def __init__(self,
    UID : str, 
    name : str, 
    specs : str, 
    footprint : str, 
    PN : str, 
    datasheet : str, 
    supplier_links : list[str]
) -> None:
        self.UID : str = UID 
        self.name : str = name 
        self.specs : str = specs 
        self.footprint : str = footprint  
        self.PN : str = PN 
        self.datasheet : str = datasheet  
        self.supplier_links : list[str] = supplier_links 

    def __str__(self) -> str:
        return str(self.__dict__).replace("'", '"')

    def make_packet(self) -> bytes:
        total_len = 14 + 20 + 16 + 16
        #name
        name_arr = bytearray(self.name.ljust(14, " "), "utf-8")
        # print(f"{len(name_arr)=}")
        #spec
        spec_arr = bytearray(self.specs.ljust(20, " "), "utf-8")
        # print(f"{len(spec_arr)=}")
        #footprint
        footprint_arr = bytearray(self.footprint.ljust(16, " "), "utf-8")
        # print(f"{len(footprint_arr)=}")
        #part number
        part_arr = bytearray(self.PN.ljust(16, " "), "utf-8")
        # print(f"{len(part_arr)=}")
        
        packet_arr = name_arr+spec_arr+footprint_arr+part_arr
        assert len(packet_arr) == total_len
        return packet_arr



