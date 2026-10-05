# Homepage dashboard config (odin-docker: /opt/stacks/homepage/config)

Copy of the live files, no secrets (the Proxmox token is read from the env, not stored here).
`custom.css` = the cyber/future theme. Deploy: scp these to odin-docker and `sudo docker compose -f /opt/stacks/homepage/compose.yaml restart`.
Validate YAML before restarting: a `: ` inside a description breaks the whole dashboard.
