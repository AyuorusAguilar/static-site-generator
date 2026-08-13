import os
import shutil

def recursive_copy(static_path: str, public_path, debug = False, recursion_deb = 0):
    if debug: print(f"DEBUG: #{' #' * recursion_deb} Deleting: {public_path}")
    shutil.rmtree(public_path)
    if debug: print(f"DEBUG: #{' #' * recursion_deb} Creating: {public_path}")
    os.mkdir(public_path)

    listdir = os.listdir(static_path)
    if debug: print(f"DEBUG: # Scaning dir {listdir}")
    for direction in listdir:
        full_dir = f"{static_path}/{direction}"
        public_dir = f"{public_path}/{direction}"
        if os.path.isdir(full_dir):
            if debug: print(f"DEBUG: #{' #' * recursion_deb} {direction} is a directory. Calling recursively")
            os.mkdir(public_dir)
            recursive_copy(full_dir, public_dir, debug, recursion_deb + 1)
        else:
            shutil.copy(full_dir, public_dir)