import sys
import os
from cloudmesh.common.util import banner


class Provider:

    def list(self):
        banner("list")
        os.system("multipass find")

    def shell(self):
        print("shell")
        #os.system("multipass shell")

    def run(self, command):
        print(f"run {command}")
        #os.system(f"multipass exec {command}")


if __name__ == "__main__":
    p = Provider()
    p.run("hallo")
    p.list()


opsys_name = os.name
oplat = sys.platform
curr_dir = os.getcwd()
print("Op name, platform, current dir:", opsys_name, oplat, curr_dir)

filesize = sys.getsizeof("cm")
filesize2 = sys.getsizeof("/")
print("Filesize:", filesize, filesize2)

x = Provider()
x.list()

#list = os.listdir('/')
#result=os.statvfs('/')
#result=os.fstat('/')
#block_size=result.f_frsize
#total_blocks=result.f_blocks
#free_blocks=result.f_bfree
#print(list)
#print(result)
#block_size, total_blocks, free_blocks

