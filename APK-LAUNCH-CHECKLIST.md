# Ultron's Corner — APK Launch Checklist

A living checklist for taking the offline Android build from **"good personal
build"** to a **full, store-grade release**. Two columns:

- **Now** = state of the current build (`update-apk.ps1` → `apk/Ultrons-Corner-*.apk`).
- **Full launch** = what a real store submission (Google Play) additionally needs.

Audited 2026-09-17 against `Ultrons APK Game/apk-build/android/` (Capacitor project)
and `ultron-dashboard.html`. Status legend: ✅ done · 🟡 partial · ❌ gap · ⬜ needs a physical device.

---

## 📦 Production build settings
| Item | Now | Full launch | Where |
|---|---|---|---|
| Release build (not debug) | ✅ signed, no `debuggable` | keep | `app/build.gradle` buildTypes.release |
| R8 code shrink + obfuscation | ❌ `minifyEnabled false` | ✅ `minifyEnabled true` + `shrinkResources true` | `app/build.gradle` |
| targetSdk / compileSdk | 🟡 34 (Android 14) | ✅ 35 (Play mandate) — needs SDK 35 installed | `variables.gradle` |
| minSdk | ✅ 22 (Android 5.1) | keep or raise to 24 | `variables.gradle` |
| versionCode / versionName | ❌ static `1` / `1.0` | ✅ auto-increment per release (tie to date stamp) | `app/build.gradle` |
| APK signing scheme | 🟡 v1 (JAR) only | ✅ enable v2 + v3 (`v2SigningEnabled`, `v3SigningEnabled`) | signingConfigs.release |
| Output format | APK | ✅ also build `.aab` (App Bundle) for Play | `./gradlew bundleRelease` |
| Permissions audit | ✅ only `INTERNET` | keep minimal; declare nothing unused | `AndroidManifest.xml` |
| Asset optimization | 🟡 5.5 MB total | optional: pngcrush/oxipng the sprites | `pixel-assets/` |

## 🕹️ Core mechanics & save state
| Item | Now | Full launch | Notes |
|---|---|---|---|
| Save retention (close/force-quit/update) | ✅ localStorage + flush on `pagehide`/`beforeunload`/`visibilitychange` | keep | corrupt-save recovery keeps a `_corrupt` backup |
| Progression / economy loops | ✅ one shared `globalMult`; all systems synergise | keep | crypto now gated to Lv 100 |
| Win / loss + reward save | ✅ boss arena + adventure rewards persist | keep | |
| UI bounds on notch/curved screens | 🟡 responsive + collapsible HUD | ✅ add `viewport-fit=cover` + `env(safe-area-inset-*)` padding | one CSS pass |
| No text/HUD clipping | ✅ verified at 412px | re-verify on a real notched device | ⬜ |

## 📱 Lifecycle & interruptions
| Item | Now | Full launch |
|---|---|---|
| App switch / resume | ✅ rAF auto-pauses; re-sync on return; offline idle via timestamps | keep |
| Phone call / alarm / notification pause | ✅ handled by WebView backgrounding | verify on device ⬜ |
| Audio focus (stop when minimized) | 🟡 works via WebView suspend; no explicit `ctx.suspend()` | ✅ add explicit suspend on `visibilitychange` hidden |
| Screen off / lock mid-session | ✅ save flush on hide; single-write, no corruption | keep |

## ⚡ Performance & stability (need a device)
| Item | Now | Full launch |
|---|---|---|
| FPS on low/mid/flagship | ⬜ unmeasured | 30/60 fps target; profile canvas draws |
| Thermal & battery over 30–60 min | ⬜ | monitor; cap rAF if hot |
| Memory leaks | ⬜ | Android Studio Profiler over long session |
| Cold-boot load time | 🟡 SW-precached | keep < 3 s; splash already configured |

## 🌐 Network & backend
| Item | Now | Full launch |
|---|---|---|
| Offline / degraded network | ✅ SW precache; graceful cloud-sync degrade | keep |
| Sync conflict resolution | 🟡 "highest-level save wins" on load | ✅ explicit merge/version check if multi-device matters |
| Server-side validation | ⚠️ client-side idle game (all local) | ✅ required only if adding leaderboards / IAP / anti-cheat |

## 🎨 Store assets (only if publishing)
- [ ] Feature graphic (1024×500), phone screenshots (min 2), 512×512 hi-res icon
- [ ] Short + full description, content rating questionnaire (IARC)
- [ ] Privacy policy URL (required even with only INTERNET permission)
- [ ] **IP review** — the game uses Marvel-derived characters/names; a public
      store release would need original renaming/redesign or licensing. Fine for
      personal/sideload use.

---

## Priority order for the "full version" build
1. `minifyEnabled true` + `shrinkResources true` (R8) — **test on device** (R8 can strip WebView bridge classes).
2. `targetSdk`/`compileSdk` → 35 (install SDK 35 platform first).
3. Auto-increment `versionCode` from the build's date stamp.
4. `v2SigningEnabled true` + `v3SigningEnabled true`.
5. Safe-area insets CSS + explicit audio suspend on background.
6. Build `.aab` and gather store assets **only if** going to Play.

> Do 1–4 into a **release-candidate** APK kept separate from the current
> known-good build, sideload, smoke-test, then promote.
