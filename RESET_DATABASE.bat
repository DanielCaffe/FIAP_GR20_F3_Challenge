@echo off
echo ======================================
echo  RESETANDO BANCO DE DADOS
echo ======================================
echo.

cd /d "%~dp0"

echo [1/4] Gerando novos dados...
python scripts\gerar_dados.py

echo.
echo [2/4] Deletando banco antigo...
del database\factory.db 2>nul

echo.
echo [3/4] Criando estrutura do banco...
B:\ENRICO\sql\sqlite-tools-win-x64-3500400\sqlite3.exe database\factory.db < database\script.sql

echo.
echo [4/4] Populando com novos dados...
B:\ENRICO\sql\sqlite-tools-win-x64-3500400\sqlite3.exe database\factory.db < database\load_from_staging.sql

echo.
echo ======================================
echo  CONCLUIDO! Banco resetado com sucesso
echo ======================================
pause
