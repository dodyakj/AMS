@echo off
color a
cls


:::           ___     ___   ___    __ __ 
:::          |   \   /   \ |   \  |  |  |
::: 		 |    \ |     ||    \ |  |  |
:::          |  D  ||  O  ||  D  ||  ~  |
:::          |     ||     ||     ||___, |
:::          |     ||     ||     ||     |
:::          |_____| \___/ |_____||____/ 

                                                                     

for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A

if exist %cd%\%1 (

cls
color c 
echo ERROR!!!!! MODUL UDAH ADA........

) else (

if exist "C:\Program Files (x86)\Odoo 10.0\server\odoo-bin.exe" (
	"C:\Program Files (x86)\Odoo 10.0\server\odoo-bin" scaffold -t cendana %1 %cd%
) else (
	"C:\Program Files\Odoo 10.0\server\odoo-bin" scaffold -t cendana %1 %cd%
)

)
	