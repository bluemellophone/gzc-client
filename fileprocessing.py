import sys
from os import makedirs, getcwd
from os.path import isfile, join, exists
import shutil

# as far as i'm aware, we should use multiprocessing to
# allow concurrency in file copying and gui operation?

# the function right now will do the copying but will not
# deal with parallelism.

def copy_files(filepaths, destinations, callback=None):
    for f in filepaths:
        # if we encounter a string that doesn't lead
        #  to a file, skip it
        if not isfile(f):
            continue
        for outdir in destinations:
            # if our destination director doesn't exist
            #  create it
            if not exists(outdir):
                makedirs(outdir)
            shutil.copy2(f, outdir) # we copy the file here
            if callback:
                # send back the name of the file
                #  that was completed
                callback(f)


# TEST MAIN
# =========

def main(argv):
    outdir = argv[0]
    files = ["test.txt", "test2"]
    copy_files(files, [outdir])

if __name__ == "__main__":
    main(sys.argv[1:])
