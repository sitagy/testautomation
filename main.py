import os
import subprocess
import time
import glob
import csv
import pandas as pd
import matplotlib.pyplot as plt

print("Enter the path of the server package")

exe_package = raw_input()
grsettings_location = os.path.join(exe_package, 'gr_settings.txt')
gr_settings = open(grsettings_location, "r")
server_conf_location = os.path.join(exe_package, 'GR-Server\config\server.event-driven.conf')
x264_param_loc = os.path.join(exe_package, 'GR-Server\config\common\\video-x264-param.conf')
exe = os.path.join(exe_package, 'GR-Server')
logserver = os.path.join(exe_package, 'GR-Server\log\logserver.txt')
#output_log_loc = os.path.join(exe_package, 'peer_Data\output_log.txt')
p_read = os.popen('echo %cd%').read()
m_split = p_read.split("\\")

o_2 = str(m_split[2])

c_users = 'C:\Users\\'
a_local = '\AppData\LocalLow\GridRaster\Gridrater Client v2017.3'

output_log_loc = c_users + o_2 + a_local


output_log_loc_join = os.path.join(output_log_loc, 'output_log.txt')

adb_loc = 'C:\client_adb_log\client-adb-log.txt'
##########################Server-Settings#######################################################
print("Server side Settings : " )
print(" ")
a =[]
for i in gr_settings:
    #i = i.split(" ")
    #print(i)
    i = i.strip()
    a.append(i)
print(a[1])
print(a[2])
print(a[3])
print(a[4])
print(a[5])
print(a[6])
print(a[10])
print(a[11])
print(a[12])
print(a[13])
#print(a[14])
#print(a[15])
#print(a[16])
#rint(a[17])

gr_settings.close()

server_conf = open(server_conf_location, "r")
b = []

for j in server_conf:
    j = j.strip()
    b.append(j)
print(b[36])

x264_param = open(x264_param_loc, "r")
c = []

for k in x264_param:
    k = k.strip()
    c.append(k)
print(c[5])
########################################Launching-Server###########################################################
print(" ")
print("If the settings are correct then press any key to continue else close the window...")
key1 = raw_input()
print("Deleting existing logserver.txt and client adb log")
if os.path.exists(adb_loc):
    os.remove(adb_loc)
if os.path.exists(logserver):
    os.remove(logserver)
if os.path.exists(output_log_loc):
    os.remove(output_log_loc)
start = 'start  "" /d '
space = " "
grserver = 'gr-server-event-driven.exe'
#cmd = 'start  "" /d "C:\\08-14-2017\GR-Server" "gr-server-event-driven.exe"'
cmd = start + exe + space + grserver
#print(cmd)
#subprocess.Popen("C:\Testing-Tools\\test.bat")
os.system(cmd)

#####################################Server-Status##########################################


while not os.path.exists(output_log_loc_join):
    time.sleep(1)
time.sleep(10)

output_log = open(output_log_loc_join, "r")

for k in output_log:
    if "[GR_Version]" in k:
        print(k)
    if "[GR]: ScreenResolution is set To:1920 x 1080 @ 75Hz,  ScreenWidth:1920, ScreenHeight:1080" in k:
        print("Server : " + k)


output_log.close()
'''
while not os.path.exists(output_log_loc):
    time.sleep(1)
time.sleep(10)
output_log = open(output_log_loc, "r")

for k in output_log:
    if "[GR_Version]" in k:
        print(k)
    if "[GR]: ScreenResolution is set To:1920 x 1080 @ 75Hz,  ScreenWidth:1280, ScreenHeight:720" in k:
        print("Server : " + k)
output_log.close()
'''
time.sleep(10)
print("Opening logserver.txt")
logserver_txt = open(logserver, "r")
for i in logserver_txt:
    i = i.strip()
    if "using 'tcp' for RTP flows" in i:
        print("Protocol Used - TCP")
    elif "using 'udp' for RTP flows" in i:
        print("Protocol Used - UDP")
    if "RTSP[config]: video specific option: b = " in i:
        f2 = i.split(' ')
        bit = f2[9]
        print("Bit rate - " +bit)
    if "detected resolution: " in i:
        f3 = i.split(' ')
        print("GA Detected resolution - " + f3[5])
logserver_txt.close()


logserver_txt = open(logserver, "r")
for j in logserver_txt:
    j.strip()

    if "audio encoder: initialized" in j:
        print("Audio Initialized")
    if "audio-source init failed" in j:
        print("Audio Initialization Failed")

    if "Use port 80 for optional RTSP-over-HTTP tunneling" in j:
        print("Server is ready")
logserver_txt.close()
##############################Launching-Client############################################
print("Press any key to launch client")
key2 = raw_input()

print("Starting adb-server and clearing the log buffer")

subprocess.call("adb start-server")
subprocess.call("adb logcat -c")
#if os.path.exists('C:\\client_adb_log'):
#    os.remove('C:\\client_adb_log')
subprocess.call("mkdir C:\\client_adb_log")
if os.path.exists('C:\\client_adb_log\client-adb-log.txt'):
    os.remove('C:\\client_adb_log\client-adb-log.txt')

print("Starting adb logcat capture")
os.system("start cmd /k adb logcat ^> C:\client_adb_log\client-adb-log.txt")

print("Starting android client")

cmd1 = 'adb shell monkey -p com.gridraster.android.gles2sample -c android.intent.category.LAUNCHER 1'
s = subprocess.check_output(cmd1.split())

#################Client Status######################

while not os.path.exists(adb_loc):
    time.sleep(1)
adb_log = open(adb_loc, 'r')
time.sleep(10)
for a in adb_log:
    if '[GR]: Read ' in a:
        a = a.strip()
        c1 = a.split(':')

        print(c1[4] +" " + c1[5])
adb_log.close()
adb_log = open(adb_loc, 'r')
for a in adb_log:
    if '[GR]: Supported Resolutions list' in a:
        a = a.strip()
        d1 = a.split('.')
        print(d1[3])
adb_log.close()
time.sleep(10)
if '[OSVR Rendering Plugin] CreateRenderManagerFromUnity Success' in open(adb_loc).read():
    print("Render Manager Initialization Sucessful")
else:
    print("Render Manager Initialization Failed")

if '[GR]: Successfull created socket' in open(adb_loc).read():
    print("Input Initialization Sucessful")
else :
    print("Input Initialization Failed")

time.sleep(15)
if 'encoder client registered: total 1 clients' in open(logserver).read():
    print ("Connection between server and client sucessful")
else :
    print('Connection not successful')


#############Closing Server###############
print(" ")
print("Press any key to close server")
key3 = raw_input()
print("Killing Server")
subprocess.call('Taskkill /IM peer.exe /F')
time.sleep(2)
subprocess.call('Taskkill /IM osvr_server.exe /F')
############Closing Client################
print("press any key to close the client")
r = raw_input()

subprocess.call('adb shell am force-stop com.gridraster.android.gles2sample')

subprocess.call('adb.exe kill-server')

subprocess.call('Taskkill /IM cmd.exe /F')
####################################logs profiling#################################
print(" ")
print("Press any key to start profiling profiler logs")
key4 = raw_input()
log_folder = os.path.join(exe_package,'GR-Server\log')
grserver = os.path.join(log_folder, 'GRServer*.txt')

newest = max(glob.iglob(grserver), key=os.path.getctime)
#print(newest)

subprocess.call('adb.exe pull /sdcard/gridraster C:\\08-14-2017\GR-Server\log')
client_gr_log = os.path.join(log_folder, 'gridraster\gr_profile*.txt')
client_new = max(glob.iglob(client_gr_log), key=os.path.getctime)

#print(client_new)





#Input files
client_log = client_new
server_log = newest

#Files for intermediate conversion
client_csv_file = "client.csv"
server_csv_file = "server.csv"

#Output file
GeneratedFile = "output.xlsx"

#Convert from client TXT to CSV file
print("Reading client log file")
in_client_txt = csv.reader(open(client_log, "r"), delimiter = '|', skipinitialspace=True)
client_fp = open(client_csv_file, "w")
csv_writer = csv.writer(client_fp)
csv_writer.writerows(in_client_txt)

#Convert from server TXT to CSV file
print("Reading server log file")
in_server_txt = csv.reader(open(server_log, "r"), delimiter = '|', skipinitialspace=True)
server_fp = open(server_csv_file, "w")
csv_writer = csv.writer(server_fp)
csv_writer.writerows(in_server_txt)

#Drop first 2 rows & unwanted columns in client file
print("Dropping unwanted columns in client log")
file_client = pd.read_csv(open(client_csv_file,"r"),skiprows=2)

file_client = file_client.drop(['Unnamed: 0', 'Frame_Head ', 'C_FIS ', 'Frame_Time ', 'Delta_Time ', 'Status ', 'Status .1', 'Render_Wait ', 'Status .2', 'Frame_Entry ', 'Wait_MS ', 'Issue_Aft ', 'EOF_Entry ', 'EOF_Exit ', 'EOF_Time ', 'Render_Entry ', 'Render_Exit ', 'Dec_Entry ', 'Dec_Exit ', 'Warp_Entry ', 'Warp_Exit ', 'Frame_Avail ', 'Rend_Progress ', 'Deco_Progress ', 'Unnamed: 34'], axis=1)

#Drop first 3 rows & unwanted columns in server file

print("Dropping unwanted columns in server log")
file_server = pd.read_csv(open(server_csv_file,"r"),skiprows=3)
file_server = file_server.drop(['Unnamed: 0', 'Frame_Capt ', 'Capt_diff ', 'Avl_for_enc ', 'Enc_Entry ', 'Enc_Exit ', 'Stream_Out ', 'Frame_header ', 'OSVR_RTN_W ', 'OSVR_RTN_X ', 'OSVR_RTN_Y ', 'OSVR_RTN_Z ', 'Unnamed: 17'], axis=1)

#Generate the output excel file
print("Dumping output file")
file = pd.concat([file_server, file_client], axis=1)
file.to_excel(GeneratedFile)


#Close opened files & delete intermediate files
client_fp.close()
server_fp.close()
os.remove(client_csv_file)
os.remove(server_csv_file)
print("DONE: Output data available in file",GeneratedFile)

time.sleep(5)


f = pd.read_excel('output.xlsx')
nonzero_pkt = []
proc_time = f['Frame_ProcTime ']
enc_time = f['Enc_Time ']
ga_fps = f['FPS ']
n_fps = f['FPS_N ']
u_fps = f['FPS_U ']
dec_time = f['Dec_Time ']
ren_time = f['Render_Time ']
mtpl = f['MTPL  ']
f = pd.read_excel('output.xlsx')
ie_list=[]
ie = f['I_E_FROM ']
for ie1 in range(len(ie)-1):
    if ie[ie1] == 'ANDROID_JNI':
        ie_list.append(ie1)

ie_list_first = ie_list[0]
ie_list_last = ie_list[-1]







#m#tpl10 = f['MTPL  '].iloc[n:8272]
#print("mtpl min ",max(mtpl10))

#Average

enc_time_avg = str(enc_time.mean())
enc_time_max = str(max(enc_time))
print("Average Encoding time = " +enc_time_avg+ " and highest value = " +enc_time_max)

ga_fps_avg = str(ga_fps.mean())
ga_fps_min = str(min(ga_fps))
print("Average GA fps = " +ga_fps_avg+ " and lowest value is = " +ga_fps_min)

n_fps_avg = str(n_fps.iloc[ie_list_first:ie_list_last].mean())
n_fps_max = str(max(n_fps.iloc[ie_list_first:ie_list_last]))
print("Average Client Native FPS = " +n_fps_avg+ " and highest value is = " +n_fps_max)

u_fps_avg = str(u_fps.iloc[ie_list_first:ie_list_last].mean())
u_fps_max = str(max(u_fps.iloc[ie_list_first:ie_list_last]))
print("Average Client Unity cycle FPS = " +u_fps_avg+ " and highest value is = " +u_fps_max)

dec_time_avg = str(dec_time.iloc[ie_list_first:ie_list_last].mean())
dec_time_max = str(max(dec_time.iloc[ie_list_first:ie_list_last]))
print("Average Decoding time = " +dec_time_avg+ " and highest value is = " +dec_time_max)

ren_time_avg = str(ren_time.iloc[ie_list_first:ie_list_last].mean())
ren_time_max = str(max(ren_time.iloc[ie_list_first:ie_list_last]))
print("Average Rendering time = " +ren_time_avg+ " and highest value is = " +ren_time_max)

#mtpl = f['MTPL  ']
mtpl_avg = str(mtpl.iloc[ie_list_first:ie_list_last].mean())

mtpl_max = str(max(mtpl.iloc[ie_list_first:ie_list_last]))
print('Average MTPL = ' +mtpl_avg+ " and highest value is = " +mtpl_max)
#, mtpl.mean(), "and highest value is : " , max(mtpl)

###################Plots###################################
plt.figure(1)    #proc time
plt.plot(proc_time)
plt.title("Proc Time")

plt.ylabel("Proc time")
plt.xlim(0,)
plt.figure(2)    #encoding time
plt.plot(enc_time.iloc[ie_list_first:ie_list_last])
plt.title("Encoding Time")

plt.ylabel("Encoding time")
plt.xlim(0,)
#plt.show()

plt.figure(3)    #decoding time
plt.plot(dec_time.iloc[ie_list_first:ie_list_last])
plt.title("Decoding Time")

plt.ylabel("Decoding time")
plt.xlim(0,)
plt.ylim(0,20)
#plt.show()



plt.figure(4)    #rendering time
plt.plot(ren_time.iloc[ie_list_first:ie_list_last])
plt.title("Rendering Time")

plt.ylabel("Rendering time")
plt.xlim(0,)
plt.ylim(0,)
#plt.show()
mtpl_graph = f['MTPL  '].iloc[ie_list_first:ie_list_last]
plt.figure(5)    #mtpl
plt.plot(mtpl_graph)
plt.title("MTPL")

plt.ylabel("MTPL")
plt.xlim(0,)
plt.ylim(0,500)
#plt.show()

plt.figure(6)    #fps
plt.plot(n_fps.iloc[ie_list_first:ie_list_last])
plt.title("FPS")

plt.ylabel("FPS")
plt.xlim(0,)
plt.ylim(0,)
plt.show()
