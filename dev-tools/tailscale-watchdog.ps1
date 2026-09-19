$status = & "C:\Program Files\Tailscale\tailscale.exe" status --json | ConvertFrom-Json
if ($status.BackendState -ne "Running") {
    & "C:\Program Files\Tailscale\tailscale.exe" up
}
# ultron-backend publishes on the tailnet IP; if Docker came up before
# Tailscale at boot, that bind failed and the restart policy won't retry it.
if ((docker inspect -f '{{.State.Running}}' ultron-backend 2>$null) -eq 'false') {
    docker start ultron-backend | Out-Null
}
