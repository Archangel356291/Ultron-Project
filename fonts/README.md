# fonts

Self-hosted copies of the dashboard's typefaces, served by `app.py` at
`/fonts/<file>` and declared with `@font-face` at the top of
`ultron-dashboard.html`. Latin subset only, `.woff2`, fetched once from
Google Fonts' CDN (2026-09-16) so the dashboard makes no third-party
request and renders identically with no internet connection.

All four are licensed under the SIL Open Font License 1.1, which permits
bundling and redistribution like this:

| File(s) | Family | Source |
|---|---|---|
| `barlow-condensed-{500,600,700}.woff2` | Barlow Condensed (Jeremy Tribby) | https://github.com/jpt/barlow |
| `inter.woff2` (variable) | Inter (Rasmus Andersson) | https://github.com/rsms/inter |
| `jetbrains-mono.woff2` (variable) | JetBrains Mono (JetBrains) | https://github.com/JetBrains/JetBrainsMono |
| `orbitron.woff2` (variable) | Orbitron (Matt McInerney) | https://github.com/theleagueof/orbitron |

License text: https://openfontlicense.org/open-font-license-official-text/
