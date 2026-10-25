@echo off
chcp 65001 > nul
echo NovaStore Web Sitesi Aciliyor...
start "" "%~dp0website\index.html"
exit
