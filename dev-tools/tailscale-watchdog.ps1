$status = & "C:\Program Files\Tailscale\tailscale.exe" status --json | ConvertFrom-Json
if ($status.BackendState -ne "Running") {
    & "C:\Program Files\Tailscale\tailscale.exe" up
}
