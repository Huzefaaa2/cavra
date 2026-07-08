# cavra integration deliver

## Name

`cavra integration deliver` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra integration deliver --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli integration deliver [OPTIONS] EVENT                                                                             
                                                                                                                                            
 Send live connector requests and write redacted delivery evidence.                                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    event      PATH  [required]                                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config                 PATH     Connector config JSON/YAML path. [required]                                                         │
│    --output                 PATH     [default: .cavra/integrations/deliveries]                                                           │
│    --provider               TEXT     [default: all]                                                                                      │
│    --retries                INTEGER  [default: 2]                                                                                        │
│    --timeout-seconds        FLOAT    [default: 10.0]                                                                                     │
│    --help                            Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
