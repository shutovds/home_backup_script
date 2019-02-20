#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import time

start_time = time.time()

exclude = ["VirtualBox VMs",
           ".gnome2",
           ".gnome2_private",
           "mydatadir",
           "postgre_datadir",
           ".cache"
           ]

USERNAME = os.getlogin()
media_path = '/media/' + USERNAME + '/'
DISKNAME = os.path.dirname(os.path.dirname(__file__)).split(media_path)[1].split('/')[0]

current_time = time.strftime("%FT%H-%M-%S")
sorce = os.environ['HOME']+"/ "
backup_folder = "/media/" + USERNAME + "/" + DISKNAME + "/reserv/" + USERNAME + "/back-"+ current_time

link_dest = "/media/" + USERNAME + "/" + DISKNAME + "/reserv/" + USERNAME + "/current "
logpath = os.path.dirname(__file__)+"/logfile "
short_log_path = os.path.dirname(__file__)+"/shortlog "

excl = ""
for element in exclude:
    excl = excl + "--exclude '" + element + "' "

options = " -a --partial --stats " + excl + "--link-dest=" + link_dest + " --log-file=" + logpath
command = "rsync" + options  + sorce + backup_folder

#print(command)
result = os.system(command)
#print(result)

print(current_time, file=open(short_log_path, "a"))
if result == 0:
    end_time = time.time()
    print("Синхронизация выполнена Успешно!", file=open(short_log_path, "a"))
    print("Длительность синхронизации: ", end_time - start_time, " сек", file=open(short_log_path, "a"))
else:
    print("Ошибка синхронизации! Проверьте logfile! \n", file=open(short_log_path, "a"))
    
# -------------------- creating links

start_time = time.time()

command = "ln -nfs " + backup_folder + " " + link_dest
os.system(command)

end_time = time.time()
print("Длительность создания ссылок ", end_time - start_time, " сек", file=open(short_log_path, "a"))

# --------------------moveing links

result = os.system('mv ' + logpath + " " + backup_folder + "/")
if result == 0:
    print("Лог-файл синхронизации перемещен в папку: back-{time} \n".format(time=current_time), file=open(short_log_path, "a"))
else:
    print("Ошибка перемещения лог-файла в папку: back-{time} Проверьте logfile! \n".format(time=current_time),
          file=open(short_log_path, "a"))

