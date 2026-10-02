@echo off
rem odin-portfix.cmd -- runs at logon from shell:startup.
rem Docker Desktop can start before Tailscale has its IP, then silently drops
rem odin-backend's port 5000 forward (bound to the tailnet IP in docker-compose.yml).
rem Wait for Docker, the container and Tailscale, then restart only if the forward is missing.
set tries=0
:wait
set /a tries+=1
if %tries% gtr 90 echo odin-portfix: gave up waiting & exit /b 1
docker inspect -f "{{.State.Running}}" odin-backend 2>nul | findstr true >nul || (timeout /t 10 /nobreak >nul & goto wait)
tailscale ip -4 >nul 2>&1 || (timeout /t 10 /nobreak >nul & goto wait)
docker port odin-backend | findstr 5000 >nul && (echo odin-portfix: forward present, nothing to do & exit /b 0)
echo odin-portfix: port forward missing, restarting odin-backend
docker restart odin-backend
