# File Stealer PC 2 USB
This is a python program to search and copy selected files and folders of drives in PC to your USB drive.

این یک برنامه پایتون برای پیدا و کپی کردن فایل ها و فولدر های دلخواه از درایور های کامپیوتر و انتقال به یو اس بی شما است
***
If your not a developer just download and use the **FileStealerPC2USB.exe** in **Release(Github)** .

اگر برنامه نویس نیستید ، در قسمت **ریلیز** در سایت گیت هاب **فایل اجرایی** رو دانلود و اجرا کنید 
***

**/Main directory/**

Compiler_Windows.py: Script for windows users 

Compiler_Linux.py: Script for Linux users

Type.txt: Tells program which file or folder needs to be copied.

.Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d} : Folder that you can put in your USB .

## How to use:
First, you need to edit "Type.txt" and write at least one argument for "Type", "folder" or "file"

ابتدا باید فایل متنی را تغییر دهید و حداقل یک مورد اضافه کنید

you can write whatever file types (extensions) for "type" , file names for "file" and folder names for folder.
something like blow:

شما میتوانید برای "تایپ" پسوند فایل ، برای "فایل" اسم فایل و برای "فولدر" اسم فولدر مورد نظر را مثل زیر وارد کنید

    type=txt,png
    file=csgo.exe,chrome.msi
    folder=ProgramFile,
    search_OS_drive=yes

Then run the script , files and folders will go to  ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" directory .

بعد برنامه را اجرا کنید فایل ها و فولدر ها به صورت خودکار در مسیر بالا کپی میشوند

To access the copied files, just rename  ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" directory in your USB to something else (perhaps not having Thumbs.ms)
, elsewhere by opening the directory in Windows you will be headed to "Printer and Scanners" and it's also a Hidden directory in most Linux oses.

برای دسترسی به فایل های کپی شده ، اسم دایرکتوری بالا را عوض کنید ، البته ترجیحا از اسامی خودش مشتق نشده نباشد در غیر این صورت در ویندوز به صفحه ی پرینتر و اسکنر ها هدایت میشوید و در لینوکس هم دایرکتوری مخفی و غیرقابل دید است

## Notice:

It doesn't search in os_installed_drive automatically because of a massive number of files and folders which take lots of time, and a weak chance of finding the special file (images, videos, and ...). You can type "yes" for "search_OS_drive=" in "type.txt"

به طورخودکار ، درایوی که سیستم عامل در آن نصب شده ، به دلیل تعداد فایل و فولدر های زیاد و شانس بسیار کم برای پیدا کردن فایل ها (عکس،فیلم و ...) ، جستجو نمیشود . شما میتوانید برای غیرفعال کردن این ویژگی کلمه "یس" را به انگلیسی به متنی اضافه کنید  

***

Your USB will recognize just by having the  ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" directory but you can also change that with changing the "favorite" in the script.

.یو اس بی شما با داشتن دایرکتوری بالا شناخته میشود و میتوانید آن را در متغییر بالا عوض کنید 

***
Based on Python 3.5+, so can't be used in Windows XP, 98, and ...

بر اساس پایتون 3.5 به بالا ، غیرقابل استفاده در ویندوز ایکس پی ، 98 و غیره 

***
Don't worry about missing and unarchived files, files will behave the right name and path in your USB and a log.txt is in the main folder logs everything.

 .نگران سردرگمی فایل ها نباشید ، همه ی فایل ها بر اساس اسم و مسیر درست کپی خواهند شد ، و فایل لاگ هم آن ها را ثبت میکند

Any error of copying files can be because of the limited access level. Don't worry about Persian(Arabic) characters, they are also supported.

ارور های کپی کردن فایل مینواند به دلیل محدودیت در سطح دسترسی  باشد . نگران کارکتر های فارسی فایل ها و پوشه ها نباشید ، کاملا با 
برنامه همخوانی دارد .
