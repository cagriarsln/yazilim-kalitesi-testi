@echo off
chcp 65001 > nul
title NovaStore Otomasyon Testi
echo ========================================================
echo       NOVASTORE E-TICARET OTOMASYON TESTI
echo ========================================================
echo.
echo Python ortamı kontrol ediliyor...
python test_otomasyon.py
echo.
echo ========================================================
echo Test tamamlandi. Kapatmak icin bir tusa basiniz.
echo ========================================================
pause > nul
