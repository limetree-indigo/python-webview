# import multiprocessing as mp
# import time



# def worker():
#     proc = mp.current_process()
#     print(proc.name, proc.pid)
#     time.sleep(5)
#     print("Subprocess End")


# if __name__ == "__main__":
#     proc = mp.current_process()
#     print(proc.name, proc.pid)

#     p = mp.Process(name="SubProcess", target=worker)
#     p.start()

#     print("MainProcess End")

import asyncio
