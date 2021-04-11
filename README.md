# File Stealer PC 2 USB
This is a python program to search and copy selected files and folders of drives in the PC to your USB drive.
***
If you're not a developer, download and use the **FileStealerPC2USB.exe** in **Release(GitHub)** .

***

**/Main directory/**

FileStealerPC2USB.py: Script for both windows and Linux users

Type.txt: Tells program which file or folder it needs to copy and some more setting.

.Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d} : Folder that you can put in your USB.

## How to use:
First, you need to edit "Type.txt" and write at least one argument for "Type", "folder" or "file"

you can write whatever file types (extensions) for "type" , file names for "file" and folder names for folder.something like blow:

    type=txt,png
    file=csgo.exe,chrome.msi
    folder=ProgramFile,
    search_OS_drive=yes

Afterthat run the script, files and folders will go to ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" directory .

To access the copied files, rename ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" directory in your USB to something else (perhaps doesn't have Thumbs.ms)
, or it will open "Printer and Scanners" in Windows and it's a hidden directory in most Linux OSes.

### Advanced:

In types.txt you can have advanced part that allow you to set more things , unless you can remove it.

If you want to use it , add these to types.txt :
    
    [Advanced]
    exceptDrive=\root,D:
    message=This message will be shown to user.
    countNumberShow=no
    log=no

Type the drive you don't want to copy items from for "exceptDrive", 
type a message that will be shown when you run the program for "message",
type yes or no for "countNumberShow" to show or not the Numbers,
and type yes or no for "log" if you want or not having log file.

## Notice:
It doesn't search in os_installed_drive automatically because of a massive number of files and folders which take lots of time, and a weak chance of finding the special file (images, videos, and...). You can type "yes" for "search_OS_drive=" in "type.txt"

***

Your USB will recognize only by having the ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" directory but you can also change that with changing the "favorite" in the script. 

***
Based on Python 3.5+, so can't use them in Windows XP, 98, and...

***
Don't worry about missing and unarchived files, files will have the right name and path in your USB and a log.txt is in the main folder logs everything.

Any error of copying files can be because of the limited access level. Don't worry about Persian(Arabic) characters, it supports them.


# فارسی
<div dir="rtl">
این یک برنامه پایتون برای پیدا و کپی کردن فایل ها و فولدر های دلخواه از درایور های کامپیوتر و انتقال به یو اس بی شما است
***
اگر برنامه نویس نیستید ، در قسمت **ریلیز** در سایت گیت هاب **فایل اجرایی** رو دانلود و اجرا کنید 

***

## روش استفاده
ابتدا باید فایل متنی را تغییر دهید و حداقل یک مورد اضافه کنید

شما میتوانید برای "تایپ" پسوند فایل ، برای "فایل" اسم فایل و برای "فولدر" اسم فولدر مورد نظر را مثل زیر وارد کنید
</div>

    type=txt,png
    file=csgo.exe,chrome.msi
    folder=ProgramFile,
    search_OS_drive=yes
    
<div dir="rtl">
**مسیر**
</div>

        .Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}
        
<div dir="rtl">
بعد برنامه را اجرا کنید فایل ها و فولدر ها به صورت خودکار در مسیر بالا کپی میشوند

برای دسترسی به فایل های کپی شده ، اسم دایرکتوری بالا را عوض کنید ، البته ترجیحا از اسامی خودش مشتق نشده نباشد در غیر این صورت در ویندوز به صفحه ی پرینتر و اسکنر ها هدایت میشوید و در لینوکس هم دایرکتوری مخفی و غیرقابل دید است

### پیشرفته
در فایل متنی میتوانید قسمت پیشرفته را که به شما تنظیمات بیشتری میدهد را اضافه کنید یا آن را حذف کنید

اگر میخواهید از آن استفاده کنید ، این خطوط را به فایل متنی اضافه کنید
</div>

    [Advanced]
    exceptDrive=\root,D:
    message=This message will be shown to user.
    countNumberShow=no
    log=no
<div dir="rtl">
    
برای **"اکسپت درایو"** درایوی را که نمیخواهید فایل ها از آن کپی شوند را وارد کنید ، 
 برای **"مسیج"** پیغامی را که میتوانید اضافه کنید تا به کاربر نشان داده شود ، 
 برای **"نامبرشو"** میتوانید **"یس"** یا **"نو"** را به انگلیسی وارد کنید تا اعداد شمارش بشوند یا نشوند ،
 برای **"لاگ"** هم میتوانید **"یس"** یا **"نو"** به انگلیسی وارد کنید تا فایل لاگ برایتان بسازد یا نسازد .

## توجه

به طورخودکار ، درایوی که سیستم عامل در آن نصب شده ، به دلیل تعداد فایل و فولدر های زیاد و شانس بسیار کم برای پیدا کردن فایل ها (عکس،فیلم و ...) ، جستجو نمیشود . شما میتوانید برای غیرفعال کردن این ویژگی کلمه "یس" را به انگلیسی به متنی اضافه کنید  
***
</div>

    ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}"

<div dir="rtl">
یو اس بی شما با داشتن دایرکتوری بالا شناخته میشود و میتوانید آن را در کد عوض کنید
***
بر اساس پایتون 3.5 به بالا ، غیرقابل استفاده در ویندوز ایکس پی ، 98 و غیره 
***
نگران سردرگمی فایل ها نباشید ، همه ی فایل ها بر اساس اسم و مسیر درست کپی خواهند شد

ارور های کپی کردن فایل مینواند به دلیل محدودیت در سطح دسترسی  باشد . نگران کارکتر های فارسی فایل ها و پوشه ها نباشید ، کاملا با برنامه همخوانی دارد 

</div>
