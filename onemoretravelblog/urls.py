import subprocess
import pandas as pd
import sqlite3
password = "micron"


class myfio():
    def __init__(self, jobs):
        self.jobs = jobs
        self.run_fio()
        self.write_to_db()

    def run_fio(self):

        # Deleting Old Files
        for x in range(0,self.jobs):
            cmd = "sudo rm bw_write_"+str(x+1)+".log"
            p = subprocess.call('echo {} | sudo -S {}'.format(password, cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            cmd = "sudo rm iops_write_"+str(x+1)+".log"
            p = subprocess.call('echo {} | sudo -S {}'.format(password, cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            cmd = "sudo rm lat_write_"+str(x+1)+".log"
            p = subprocess.call('echo {} | sudo -S {}'.format(password, cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        # Run command
        # --filename=/dev/mapper/Gen9NVDIMM
        cmd = "sudo fio --name=first-run --direct=0 --rw=randwrite --sync=1 --numjobs="+str(self.jobs)+" --bs=4k --time_based --runtime=20 --thinktime=0 --size=512M --ioengine=psync --norandommap --group_reporting --write_bw_log=write_bw_log --write_iops_log=write_iops_log --write_lat_log=write_lat_log --log_avg_msec=900"
        p = subprocess.call('echo {} | sudo -S {}'.format(password, cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)


        # Moving Files To New Name
        for x in range(0, self.jobs):
            cmd = "mv write_bw_log_bw."+str(x+1)+".log bw_write_"+str(x+1)+".log"
            p = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            cmd = "mv write_iops_log_iops."+str(x+1)+".log iops_write_"+str(x+1)+".log"
            p = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            cmd = "mv write_lat_log_lat."+str(x+1)+".log lat_write_"+str(x+1)+".log"
            p = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            #Deleting Old Files
            cmd = "sudo rm write_bw_log_bw."+str(x+1)+".log"
            p = subprocess.call('echo {} | sudo -S {}'.format(password, cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            cmd = "sudo rm write_iops_log_iops."+str(x+1)+".log"
            p = subprocess.call('echo {} | sudo -S {}'.format(password, cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            cmd = "sudo rm write_lat_log_lat."+str(x+1)+".log"
            p = subprocess.call('echo {} | sudo -S {}'.format(password, cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            cmd = "sudo rm write_lat_log_clat."+str(x+1)+".log"
            p = subprocess.call('echo {} | sudo -S {}'.format(password, cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            cmd = "sudo rm write_lat_log_slat."+str(x+1)+".log"
            p = subprocess.call('echo {} | sudo -S {}'.format(password, cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

    def write_to_db(self):
        df_bw = pd.DataFrame()
        df_lat = pd.DataFrame()
        df_iops = pd.DataFrame()
        for x in range(0, self.jobs):
            df1 = pd.read_csv("bw_write_"+str(x+1)+".log", header=None, usecols=[1, 1])
            df2 = pd.read_csv("lat_write_"+str(x+1)+".log", header=None, usecols=[1, 1])
            df3 = pd.read_csv("iops_write_"+str(x+1)+".log", header=None, usecols=[1, 1])
            if x == 0:
                df_bw = df1
                df_lat = df2
                df_iops = df3
            else:
                df_bw = df_bw + df1
                df_lat = df_lat + df2
                df_iops = df_iops + df3


        result = pd.concat([df_bw, df_lat, df_iops], axis=1, join_axes=[df1.index])
        result.columns = ["bw", "lat", "iops"]

        # Write to DB
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        for index, row in result.iterrows():
            cursor.execute("insert into sc_demo_2017_nvdimm (bw, lat, iops) values (?, ?, ?)",(int(row["bw"]), int(row["lat"]), int(row["iops"])))
        conn.commit()

        # Deleting Old Files
        for x in range(0,self.jobs):
            cmd = "sudo rm bw_write_"+str(x+1)+".log"
            p = subprocess.call('echo {} | sudo -S {}'.format(password, cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            cmd = "sudo rm iops_write_"+str(x+1)+".log"
            p = subprocess.call('echo {} | sudo -S {}'.format(password, cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            cmd = "sudo rm lat_write_"+str(x+1)+".log"
            p = subprocess.call('echo {} | sudo -S {}'.format(password, cmd), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)


for x in range(0,100):
    print(x)
    myfio(1)


# --readwrite=randrw --rwmixread=50%
