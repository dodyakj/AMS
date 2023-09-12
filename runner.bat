@echo off
color a
cls


:::   ____  ____  ____   ____   ___ 
:::  /    ||    ||    \ |    \ /   \ 
::: |   __| |  | |  _  ||  D  )     |
::: |  |  | |  | |  |  ||    /|  O  |
::: |  |_ | |  | |  |  ||    \|     |
::: |     | |  | |  |  ||  .  \     |
::: |___,_||____||__|__||__|\_|\___/ 
:::                                                                      
:::  ____  ______         __    ___  ____   ___     ____  ____    ____   
::: |    \|      |       /  ]  /  _]|    \ |   \   /    ||    \  /    |  
::: |  o  )      |      /  /  /  [_ |  _  ||    \ |  o  ||  _  ||  o  |  
::: |   _/|_|  |_|     /  /  |    _]|  |  ||  D  ||     ||  |  ||     |  
::: |  |    |  |      /   \_ |   [_ |  |  ||     ||  _  ||  |  ||  _  |  
::: |  |    |  |      \     ||     ||  |  ||     ||  |  ||  |  ||  |  |  
::: |__|    |__|       \____||_____||__|__||_____||__|__||__|__||__|__|  
                                                                     



for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A

if [%1]==[] goto usage
if exist "C:\Program Files (x86)\Odoo 10.0\server\odoo-bin.exe" (
    "C:\Program Files (x86)\Odoo 10.0\server\odoo-bin" -c odoo.conf --update %1
) else (
    "C:\Program Files\Odoo 10.0\server\odoo-bin" -c odoo.conf --update %1
)
goto :eof
:usage                                                                                   
if exist "C:\Program Files (x86)\Odoo 10.0\server\odoo-bin.exe" (
    "C:\Program Files (x86)\Odoo 10.0\server\odoo-bin" -c odoo.conf
) else (
    "C:\Program Files\Odoo 10.0\server\odoo-bin" -c odoo.conf
)