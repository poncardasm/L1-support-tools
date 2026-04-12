# log-parse (Windows)

Windows-specific implementation of the log-parse CLI tool.

> **Status:** Planned - Not yet implemented

## Platform-Specific Features (Planned)

### Windows Event Logs

Parse Windows Event Log exports:

```powershell
# Export Event Logs to JSON (planned)
Get-WinEvent -FilterHashtable @{LogName='Application'; Level=1,2,3} | 
    Export-Clixml events.xml
log-parse events.xml
```

### IIS Logs

```powershell
log-parse "C:\inetpub\logs\LogFiles\W3SVC1\u_ex240101.log"
```

### Windows Update Logs

```powershell
log-parse "C:\Windows\Logs\WindowsUpdate\WindowsUpdate.log"
```

## Installation (Planned)

### Chocolatey

```powershell
choco install log-parse
```

### Winget

```powershell
winget install log-parse
```

### From Source

```powershell
cd 02-log-dump-parser\windows
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## Windows-Specific Log Sources

| Source | Path | Format | Status |
|--------|------|--------|--------|
| Application Event Log | `Get-WinEvent` | EVTX | Planned |
| System Event Log | `Get-WinEvent` | EVTX | Planned |
| IIS Logs | `C:\inetpub\logs\` | W3C | Planned |
| Windows Update | `C:\Windows\Logs\` | plain | Planned |
| Setup Logs | `C:\$Windows.~BT\Sources\Panther\` | plain | Planned |

## Differences from macOS Version

The Windows version will include:

- EVTX (Windows Event Log) parser
- Windows-optimized path handling
- PowerShell pipeline support
- Windows-specific error pattern detection

## Configuration

Config directory: `%APPDATA%\log-parse\`

## See Also

- [Main Project README](../../README.md)
- [macOS Implementation](../macos/)
- [PRD](docs/PRD.md) - Product Requirements
- [Implementation](docs/IMPLEMENTATION.md) - Technical Plan
- [Tasks](docs/TASKS.md) - Development Checklist
