from platform import system as syst
from shutil import copyfile, copytree
from time import localtime
from sys import stdout , exit
from os import walk, chdir, listdir, sep, path, makedirs
import threading

class MainWindows:
    def __init__(self):
        self.Log = []
        self.counter = 5
        filess = listdir('.')
        if "types.txt" in filess:
            self.message, self.countnumShow, self.have_log , OS_search = "","","",""
            listertype,listerfile,listerfolder,exceptdrive = [],[],[],[]
            file = open('types.txt')
            reader = file.readlines()

            # region Reader
            for read in reader:
                if "search_OS_drive=" in read:
                    OS_search = read.replace(" ", "").replace("\n", "").replace("search_OS_drive=", "").lower()
                if "types=" in read:
                    listertype = read.replace("types=", "").replace(" , ", '').replace("\n", "").replace(" ,",",").replace(", ", ",").lower().split(",")
                if "files=" in read:
                    listerfile = read.replace("files=", "").replace(" , ", '').replace("\n", "").replace(" ,",",").replace(", ", ",").lower().split(",")
                if "folders=" in read:
                    listerfolder = read.replace("folders=", "").replace(" , ", '').replace("\n", "").replace(" ,",",").replace(", ", ",").lower().split(",")
                if "exceptDrive=" in read:
                    exceptdrive = read.replace("exceptDrive=", "").replace(":","").replace(sep,"").replace(" , ", '').replace("\n", "").replace(" ,",",").replace(", ", ",").lower().split(",")
                if "message" in read:
                    self.message =read.replace("message=", "").replace("\n", "") + "\n"
                if "countNumberShow" in read:
                    self.countnumShow = read.replace("countNumberShow=", "").replace("\n", "").lower()
                if "log=" in read:
                    self.have_log = read.replace("log=", "").replace("\n", "").lower()
        # endregion

            self.folders = list(filter(None, listerfolder))
            self.types = list(filter(None, listertype))
            self.file = list(filter(None, listerfile))
            self.exceptdrive = list(filter(None, exceptdrive))
            self.oser = "NO-os"

            if OS_search == "yes":
                self.oser = "Yes-os"
                admin = ctypes.windll.shell32.IsUserAnAdmin()
                if admin != 1 :
                    print("May not work properly without Admin Permission . You can change "+ '\033[1m' + "search_OS_drive " + "in types.txt to" + "\033[1m"+ " no")

    def timer(self):
        if self.counter >= 0:
            stdout.write('\r' + str("Exiting in " + str(self.counter)))
            t = threading.Timer(1, self.timer)
            t.start()
            self.counter -= 1

    def usb_finder(self):
        self.usb_list = []
        self.dest = ""

        drivebits = GetLogicalDrives()
        for d in range(1, 26):
            mask = 1 << d
            if drivebits & mask:
                drname = '%c:\\' % chr(ord('A') + d)
                t = GetDriveType(drname)
                if t == DRIVE_REMOVABLE:
                    self.usb_list.append(drname)

        if self.usb_list.__len__() == 0 :
            print("No USB Connected!!!")
            self.timer()
            exit()

        favorite = ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}"

        for usb in self.usb_list:
            chdir(usb)
            if favorite in listdir('.'):
                self.dest = usb + sep + favorite + sep
        if self.dest == "":
            print("No F-USB!!!")
            self.timer()
            exit()

    def drives(self):
        win = environ['SYSTEMDRIVE'] + sep

        self.drive_list = []
        drivebits = GetLogicalDrives()
        for d in range(1, 26):
            mask = 1 << d
            if drivebits & mask:
                drname = '%c:\\' % chr(ord('A') + d)
                t = GetDriveType(drname)
                if t == DRIVE_FIXED:
                    self.drive_list.append(drname)

## region NOT OS:
        if self.oser == "NO-os":
            for i in self.drive_list:
                if i == win :
                    self.drive_list.remove(i)
## endregion

# region exceptdrive
        if self.exceptdrive != []:
            for ex in self.exceptdrive :
                if ex.upper()+":"+sep in self.drive_list:
                    self.drive_list.remove(ex.upper()+":"+sep)
# endregion

        if self.message != "":
            print(self.message)

        #region AutoMinimize
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
        #endregion

        self.counter = 0
        for driver in self.drive_list:
            self.copier(driver)

    def structure(self):
        structure = "\n==========Search==========\nSearched for these folders    : "+str(self.folders) +"\nSearched for these file-types : "+str(self.types) +"\nSearched for these files      : "+ str(self.file)  + "\nExcept drives                 : " + str(self.exceptdrive) +  "\nAnd search os drive(folders)  : "+ self.oser.replace("-os","").lower()
        return structure.replace("\'","").replace("[","").replace("]","")

    def copier(self,driver):
        chdir(driver)

        files = self.file
        types = self.types
        folder = self.folders

        for (dirpath, dirname, filenames) in walk('.'):
                if types != []:
                    for filename in filenames:
                        for type in types:
                            if filename.lower().endswith(types[types.index(type)]):
                                main_location = sep.join([dirpath,filename])

                                timemin = str(localtime().tm_min)
                                timesec = str(localtime().tm_sec)

                                time = " (m" + timemin + "-s" + timesec + ")"

                                absulpath = path.abspath(main_location).replace(":","")
                                absulpath = absulpath[:absulpath.rfind(sep)] + sep
                                # print(absulpath)

                                if filename in listdir(self.dest):
                                    filename = filename.replace(types[types.index(type)],"")
                                    try:
                                        makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                        copyfile(main_location,self.dest + absulpath + filename + time + types[types.index(type)])
                                    except:
                                        self.Log.append(driver + main_location[2:])
                                    # print(main_location)
                                    self.counter += 1
                                    # print(counter)
                                    if self.countnumShow != "no":
                                        stdout.write('\r'+str(self.counter))

                                else:
                                    try:
                                        makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                        copyfile(main_location, self.dest +absulpath+ filename)
                                    except :
                                        self.Log.append(driver + main_location[2:])
                                    self.counter += 1
                                    # print(counter)
                                    if self.countnumShow != "no":
                                        stdout.write('\r' +str(self.counter))

                if files != [] :
                    for filename in filenames :
                        for file in files:
                            if files[files.index(file)] in filename.lower():
                                main_location = sep.join([dirpath, filename])

                                timemin = str(localtime().tm_min)
                                timesec = str(localtime().tm_sec)

                                time = " (m" + timemin + "-s" + timesec + ")"

                                absulpath = path.abspath(main_location).replace(":", "")
                                absulpath = absulpath[:absulpath.rfind(sep)] + sep
                                # print(absulpath)

                                if filename in listdir(self.dest):
                                    filename = filename.replace(files[files.index(file)], "")
                                    try:
                                        makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                        copyfile(main_location,self.dest + absulpath + filename + time + files[files.index(file)])
                                    except:
                                        self.Log.append(driver + main_location[2:])
                                    # print(main_location)
                                    self.counter += 1
                                    # print(counter)
                                    if self.countnumShow != "no":
                                        stdout.write('\r' + str(self.counter))

                                else:
                                    try:
                                        makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                        copyfile(main_location, self.dest + absulpath + filename)
                                    except :
                                        self.Log.append(driver + main_location[2:])
                                    self.counter += 1
                                    # print(counter)
                                    if self.countnumShow != "no":
                                        stdout.write('\r' + str(self.counter))

                if folder != [] :
                    for dir in dirname :
                        for fold in folder :
                            if folder[folder.index(fold)] in dir.lower():
                                main_location = sep.join([dirpath, dir])

                                timemin = str(localtime().tm_min)
                                timesec = str(localtime().tm_sec)

                                time = " (m" + timemin + "-s" + timesec + ")"

                                absulpath = path.abspath(main_location).replace(":", "")
                                absulpath = absulpath[:absulpath.rfind(sep)] + sep
                                # print(absulpath)

                                if dir in listdir(self.dest):
                                    dir = dir.replace(folder[folder.index(fold)], "")
                                    try:
                                        makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                        copytree(main_location,self.dest + absulpath + dir + time + folder[folder.index(fold)])
                                    except :
                                        self.Log.append(driver + main_location[2:])
                                    self.counter += 1
                                    if self.countnumShow != "no":
                                        stdout.write('\r' + str(self.counter))

                                else:
                                    try:
                                        makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                        copytree(main_location, self.dest + absulpath + dir)
                                    except :
                                        self.Log.append(driver + main_location[2:])
                                    self.counter += 1
                                    # print(counter)
                                    if self.countnumShow != "no":
                                        stdout.write('\r' + str(self.counter))


class MainLinux:
    def __init__(self):
        self.username = getuser()
        self.counter = 5

        self.Log = []
        filess = listdir('.')
        if "types.txt" in filess:
            self.message, self.countnumShow, self.have_log, OS_search = "", "", "", ""
            listertype, listerfile, listerfolder, exceptdrive = [], [], [], []
            file = open('types.txt')
            reader = file.readlines()

            # region Reader
            for read in reader:
                if "search_OS_drive=" in read:
                    OS_search = read.replace(" ", "").replace("\n", "").replace("search_OS_drive=", "").lower()
                if "types=" in read:
                    listertype = read.replace("types=", "").replace(" , ", '').replace("\n", "").replace(" ,",",").replace(", ", ",").lower().split(",")
                if "files=" in read:
                    listerfile = read.replace("files=", "").replace(" , ", '').replace("\n", "").replace(" ,",",").replace(", ", ",").lower().split(",")
                if "folders=" in read:
                    listerfolder = read.replace("folders=", "").replace(" , ", '').replace("\n", "").replace(" ,",",").replace(", ", ",").lower().split(",")
                if "exceptDrive=" in read:
                    exceptdrive = read.replace("exceptDrive=", "").replace(":", "").replace(sep, "").replace(" , ",'').replace("\n", "").replace(" ,", ",").replace(", ", ",").lower().split(",")
                if "message" in read:
                    self.message =read.replace("message=", "").replace("\n", "") + "\n"
                if "countNumberShow" in read:
                    self.countnumShow = read.replace("countNumberShow=", "").replace("\n", "").lower()
                if "log=" in read:
                    self.have_log = read.replace("log=", "").replace("\n", "").lower()
            # endregion

            self.folders = list(filter(None, listerfolder))
            self.types = list(filter(None, listertype))
            self.file = list(filter(None, listerfile))
            self.exceptdrive = list(filter(None, exceptdrive))


            if OS_search == "yes":
                self.oser = "Yes-os"
                if getuid() != 0:
                    print("====\nRun the script with root user , or change "+ '\033[1m' + "search_OS_drive " + "in types.txt to" + "\033[1m"+ " no")
                    print("====")
                    self.timer()
                    exit()
                else:
                    self.username = input("====\nEnter your non-root username > ").lower()
                    print("====\n")
            else:
                self.oser = "NO-os"
                if getuid() == 0:
                    self.username = input("====\nEnter your non-root username > ").lower()
                    print("====\n")

    def timer(self):
        if self.counter >= 0:
            stdout.write('\r' + str("Exiting in " + str(self.counter)))
            t = threading.Timer(1, self.timer)
            t.start()
            self.counter -= 1

    def usb_finder(self):
        chdir("/media/" + self.username + "/")
        self.usb_list = listdir('.')
        self.dest = ""

        if self.usb_list.__len__() == 0:
            print("No USB Connected!!!\n")
            self.timer()
            exit()

        favorite = ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}"

        for usb in self.usb_list:
            chdir("/media/" + self.username + sep + usb)
            if favorite in listdir('.'):
                self.dest = "/media/" + self.username + sep + usb + sep + favorite + sep
        if self.dest == "":
            print("No F-USB!!!\n")
            self.timer()
            exit()

    def drives(self):
        self.drive_list = ["/"]

## region NOT OS:
        if self.oser == "NO-os":
            self.drive_list = ["/media","/home","/mnt"]
## endregion

# region exceptdrive
        if self.exceptdrive != []:
            for ex in self.exceptdrive:
                if sep+ex.lower() in self.drive_list:
                    self.drive_list.remove(sep+ex.lower())
# endregion

        if self.message != "":
            print(self.message)

        # region AutoMinimize
        # import ctypes
        # ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
        # endregion

        self.counter = 0
        for driver in self.drive_list:
            if driver != "/" :
                if driver.replace(sep,"") in listdir("/"):
                    self.copier(driver)
            else:
                self.copier(driver)

    def structure(self):
        structure = "\n==========Search==========\nSearched for these folders    : "+str(self.folders) +"\nSearched for these file-types : "+str(self.types) +"\nSearched for these files      : "+ str(self.file)  + "\nExcept drives                 : " + str(self.exceptdrive) +  "\nAnd search os drive(folders)  : "+ self.oser.replace("-os","").lower()
        return structure.replace("\'","").replace("[","").replace("]","")

    def copier(self,driver):
        chdir(driver)

        files = self.file
        types = self.types
        folder = self.folders

        for (dirpath, dirname, filenames) in walk('.'):
                if types != []:
                    for filename in filenames:
                        for type in types:
                            if filename.lower().endswith(types[types.index(type)]):
                                main_location = sep.join([dirpath,filename])

                                timemin = str(localtime().tm_min)
                                timesec = str(localtime().tm_sec)

                                time = " (m" + timemin + "-s" + timesec + ")"

                                absulpath = path.abspath(main_location).replace(":","")
                                absulpath = absulpath[:absulpath.rfind(sep)] + sep
                                # print(absulpath)

                                if filename in listdir(self.dest):
                                    filename = filename.replace(types[types.index(type)],"")
                                    try:
                                        makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                        copyfile(main_location,self.dest + absulpath + filename + time + types[types.index(type)])
                                    except:
                                        self.Log.append(driver + main_location[2:])
                                    # print(main_location)
                                    self.counter += 1
                                    # print(counter)
                                    if self.countnumShow != "no":
                                        stdout.write('\r'+str(self.counter))

                                else:
                                    try:
                                        makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                        copyfile(main_location, self.dest +absulpath+ filename)
                                    except :
                                        self.Log.append(driver + main_location[2:])
                                    self.counter += 1
                                    # print(counter)
                                    if self.countnumShow != "no":
                                        stdout.write('\r' +str(self.counter))

                if files != [] :
                    for filename in filenames :
                        for file in files:
                            if files[files.index(file)] in filename.lower():
                                main_location = sep.join([dirpath, filename])

                                timemin = str(localtime().tm_min)
                                timesec = str(localtime().tm_sec)

                                time = " (m" + timemin + "-s" + timesec + ")"

                                absulpath = path.abspath(main_location).replace(":", "")
                                absulpath = absulpath[:absulpath.rfind(sep)] + sep
                                # print(absulpath)

                                if filename in listdir(self.dest):
                                    filename = filename.replace(files[files.index(file)], "")
                                    try:
                                        makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                        copyfile(main_location,self.dest + absulpath + filename + time + files[files.index(file)])
                                    except:
                                        self.Log.append(driver + main_location[2:])
                                    # print(main_location)
                                    self.counter += 1
                                    # print(counter)
                                    if self.countnumShow != "no":
                                        stdout.write('\r' + str(self.counter))

                                else:
                                    try:
                                        makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                        copyfile(main_location, self.dest + absulpath + filename)
                                    except :
                                        self.Log.append(driver + main_location[2:])
                                    self.counter += 1
                                    # print(counter)
                                    if self.countnumShow != "no":
                                        stdout.write('\r' + str(self.counter))

                if folder != [] :
                    for dir in dirname :
                        for fold in folder :
                            if folder[folder.index(fold)] in dir.lower():
                                main_location = sep.join([dirpath, dir])

                                timemin = str(localtime().tm_min)
                                timesec = str(localtime().tm_sec)

                                time = " (m" + timemin + "-s" + timesec + ")"

                                absulpath = path.abspath(main_location).replace(":", "")
                                absulpath = absulpath[:absulpath.rfind(sep)] + sep
                                # print(absulpath)

                                if dir in listdir(self.dest):
                                    dir = dir.replace(folder[folder.index(fold)], "")
                                    try:
                                        makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                        copytree(main_location,self.dest + absulpath + dir + time + folder[folder.index(fold)])
                                    except :
                                        self.Log.append(driver + main_location[2:])
                                    self.counter += 1
                                    if self.countnumShow != "no":
                                        stdout.write('\r' + str(self.counter))

                                else:
                                    try:
                                        makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                        copytree(main_location, self.dest + absulpath + dir)
                                    except :
                                        self.Log.append(driver + main_location[2:])
                                    self.counter += 1
                                    # print(counter)
                                    if self.countnumShow != "no":
                                        stdout.write('\r' + str(self.counter))


if __name__ == "__main__":
    if syst() == "Windows":
        # region libs
        from os import environ
        import ctypes
        from win32api import GetLogicalDrives
        from win32file import GetDriveType, DRIVE_FIXED, DRIVE_REMOVABLE
        #endregion

        filess = listdir('.')
        if "types.txt" not in filess:
            print("====\nThere is no [type.txt] file in this directory, copy it here and re-open the program.\nAlso you can answer these questions(hit Enter without anything typed to skip a question. Seperate items with :  ,  )\n====")
            OS_search = input("Do you want program to search in os drive/folder(s) ? (yes\\no)\n > ").replace(" ", "")
            listertype = input("Which type-file do you want to be copied ? (hit Enter for nothing)\n > ").replace(" ",
                                                                                                                  "")
            listerfile = input("What files do you want to be copied ? (hit Enter for nothing)\n > ")
            listerfolder = input("What folders do you want to be copied ? (hit Enter for nothing)\n > ")
            exceptdrive = input("What drives don't you want to be copied ? (hit Enter for nothing)\n > ").replace(" ",
                                                                                                                  "")
            message = input("What message do you want to be shown ? (hit Enter for nothing)\n > ")
            countnumShow = input("Do you want numbers of files to be counted ? (yes\\no)\n > ").replace(" ", "")
            have_log = input("Do you want to have log-file ? (yes\\no)\n > ").replace(" ", "")

            print("\nAll done. Let's go for real challenge...\n==========================\n")

            txt = open("types.txt", "w")
            txt.write("[Basic]\ntypes=" + listertype + "\nfiles=" + listerfile + "\nfolders=" + listerfolder +
                      "\nsearch_OS_drive=" + OS_search + "\n\n[Advanced]\nexceptDrive=" + exceptdrive +
                      "\nmessage=" + message + "\ncountNumberShow=" + countnumShow + "\nlog=" + have_log +
                      "\n\n\nNote:\nyou can seperate items with	                 : ,\nSearch_OS_drive,CountnumShow, and Log should be	 : yes\\no")
            txt.close()

        M = MainWindows()
        M.usb_finder()
        M.drives()

        #region log
        if M.have_log != "no":
            if M.Log == []:
                log1 = open(M.dest+"Log.txt","w",encoding="utf-8")
                log1.write("#####All files(folders) copied#####\n")
                log1.close()
                log = open(M.dest+"Log.txt","a",encoding="utf-8")
                log.write(M.structure())
                log.close()
            if len(M.Log) > 0:
                log1 = open(M.dest+"Log.txt","w",encoding="utf-8")
                log1.write("=====Couldn't copy these files or folders=====\n\n")
                log1.close()
                log = open(M.dest+"Log.txt","a",encoding="utf-8")
                for Log in M.Log:
                    log.write(Log + "\n")
                log.write(M.structure())
                log.close()
        #endregion
        print(".")


    if syst() == "Linux":
        # region libs
        from getpass import getuser
        from os import getuid
        #endregion

        filess = listdir('.')
        if "types.txt" not in filess:
            print("\nThere is no [type.txt] file in this directory, copy it here and re-open the program.\nAlso you can answer these questions(hit Enter without anything typed to skip a question. Seperate items with :  ,  )\n")
            OS_search = input("Do you want program to search in os drive/folder(s) ? (yes\\no)\n > ").replace(" ", "")
            listertype = input("Which type-file do you want to be copied ? (hit Enter for nothing)\n > ").replace(" ",
                                                                                                                  "")
            listerfile = input("What files do you want to be copied ? (hit Enter for nothing)\n > ")
            listerfolder = input("What folders do you want to be copied ? (hit Enter for nothing)\n > ")
            exceptdrive = input("What drives don't you want to be copied ? (hit Enter for nothing)\n > ").replace(" ",
                                                                                                                  "")
            message = input("What message do you want to be shown ? (hit Enter for nothing)\n > ")
            countnumShow = input("Do you want numbers of files to be counted ? (yes\\no)\n > ").replace(" ", "")
            have_log = input("Do you want to have log-file ? (yes\\no)\n > ").replace(" ", "")

            print("\nAll done. Let's go for real challenge...\n==========================\n")

            txt = open("types.txt", "w")
            txt.write("[Basic]\ntypes=" + listertype + "\nfiles=" + listerfile + "\nfolders=" + listerfolder +
                      "\nsearch_OS_drive=" + OS_search + "\n\n[Advanced]\nexceptDrive=" + exceptdrive +
                      "\nmessage=" + message + "\ncountNumberShow=" + countnumShow + "\nlog=" + have_log +
                      "\n\n\nNote:\nyou can seperate items with	                 : ,\nSearch_OS_drive,CountnumShow, and Log should be	 : yes\\no")
            txt.close()

        M = MainLinux()
        M.usb_finder()
        M.drives()

        # region log
        if M.have_log != "no":
            if M.Log == []:
                log1 = open(M.dest + "Log.txt", "w", encoding="utf-8")
                log1.write("#####All files(folders) copied#####\n")
                log1.close()
                log = open(M.dest + "Log.txt", "a", encoding="utf-8")
                log.write(M.structure())
                log.close()
            if len(M.Log) > 0:
                log1 = open(M.dest + "Log.txt", "w", encoding="utf-8")
                log1.write("=====Couldn't copy these files or folders=====\n\n")
                log1.close()
                log = open(M.dest + "Log.txt", "a", encoding="utf-8")
                for Log in M.Log:
                    log.write(Log + "\n")
                log.write(M.structure())
                log.close()
        # endregion
        print(".")
