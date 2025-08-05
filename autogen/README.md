# Autogen Studio

Install by `pip install -U autogenstudio`
- bin path
  - linux `$HOME/.local/bin`
  - Windows (powershell) `(Split-Path (Get-Command python).Source) + '\Scripts'`

Run by `autogenstudio ui --host 0.0.0.0`
- `--appdir` defaults to
  - Windows: `$env:USERPROFILE\.autogenstudio`
  - Linux: `$HOME/.autogenstudio`
- global configs (e.g. Gallery:Models) stored in `--appdir`
- `--port` defaults to 8081