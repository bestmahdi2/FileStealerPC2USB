# File Stealer PC 2 USB
This is a python program to search and copy selected types of files of the drives in PC to your selected USB drive.

این یک برنامه پایتون برای پیدا و کپی کردن فرمت های دلخواه از درایور های کامپیوتر و انتقال به یو اس بی انتخابی است
***
If your not a developer just download and use the **FileStealerPC2USB.exe** in **Release(Github)** .

اگر برنامه نویس نیستید ، در قسمت **ریلیز** در سایت گیت هاب **فایل اجرایی** رو دانلود و اجرا کنید 
***

**/Main directory/**

Compiler_Windows.py : script for windows users 

## How to use:
Just run the script , files will go to  ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" directory .

فقط برنامه را اجرا کنید فایل ها در به صورت خودکار در مسیر بالا کپی میشوند

To access the copied files , just rename  ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" directory in your USB to something else (perhaps not having Thumbs.ms)
, elsewhere by opening the directory in Windows you will be headed to "Printer and Scanners" and it's also a Hidden directory in most Linux oses.

برای دسترسی به فایل های کپی شده ، اسم دایرکتوری بالا را عوض کنید ، البته ترجیحا از اسامی خودش مشتق نشده نباشد در غیر این صورت در ویندوز به صفحه ی پرینتر و اسکنر ها هدایت میشوید و در لینوکس هم دایرکتوری مخفی و غیرقابل دید است

## Notice:

It doesn't search in os_installed_drive because massive number of files and folders which take lots of time ,and weak chance of finding special file types (images , videos and ...) . for disabling you can remove "region OS" in the script .

به طور پیش فرض ، درایوی که سیستم عامل در آن نصب شده ، به دلیل تعداد فایل های زیاد و شانس بسیار کم برای پیدا کردن فایل های خاص(عکس،فیلم و ...) ، جستجو نمیشود  . برای غیر فعال کردن در بخش بالا آن را حذف کنید

***

Your USB will recognize just by having the  ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" directory  but you can also change that with changing the "favorite" in script .

.یو اس بی شما با داشتن دایرکتوری بالا شناخته میشود و میتوانید آن را در متغییر بالا عوض کنید 

***
Based on python 3.5+ , so can't be used in windows Xp , 98 and ...

بر اساس پایتون 3.5 به بالا ، غیرقابل استفاده در ویندوز ایکس پی ، 98 و غیره 

You may want to change file type ("filetype") in script to search for your favorite type of file.

.شاید دوست داشته باشید فرمت فایل ها (متغییر بالا) را جایگزین پسوند مورد نظرتان کنید 
***
Don't worry about missing and unarchived files . files will be have the right name and path in your USB .

.نگران سردرگمی فایل ها نباشید ، همه ی فایل ها بر اساس اسم و مسیر درست کپی شده اند