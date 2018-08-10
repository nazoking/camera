import fcntl
import os

def lock_pid(name, lock=True):
    with open(name, "wt") as f:
        if lock:
            fcntl.flock(f, fcntl.LOCK_SH|fcntl.LOCK_NB)
        try:
            pid = os.getpid()
            f.write(str(pid))
            f.flush()
            yield pid
        finally:
            f.close()
            os.remove(name)
