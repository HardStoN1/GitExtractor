import zlib
import sys
import hashlib
import os

class Expander:
    def __init__(self, filename):
        self.filename = filename
        self.decompressed = None
        self.hash_code = None

        if self.__decompress():
            print(f"###########\nFilename: {self.filename}\nHash: {self.hash_code}")
            res = self.__get_data()
            if not res:
                print("Oops! Could not read.")
                return
            print("Blob: " + str(res))
            
        else:
            print(f"###########\nFilename: {self.filename}")
            print("Oops! Could not decompress.")
    
    def __decompress(self):
        try:
            with open(self.filename, "rb") as encoded:
                raw = encoded.read()
                data = zlib.decompress(raw)
                hash_code = hashlib.sha1(data).hexdigest()

            self.decompressed = data
            self.hash_code = hash_code
            return True
        except:
            return False

    def __get_data(self):
        try:
            blob_data = os.popen(f"git cat-file blob {self.hash_code}").read()
            if "fatal: git cat-file" in blob_data:
                return False
            return blob_data
        except:
            print("Could not fetch data!")
            return False

def main():
    # Should be root of objects
    objects_root_name = sys.argv[1]
    objects_root = os.listdir(objects_root_name)
    for obj_dir in objects_root:
        full_path_objects_dir = objects_root_name + "/" + obj_dir
        obj_dir_full = os.listdir(full_path_objects_dir)
        for obj in obj_dir_full:
            full_path_object = full_path_objects_dir + "/" + obj
            expander = Expander(full_path_object)

if __name__ == "__main__":
    main()