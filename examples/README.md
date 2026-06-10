# Example contracts

`reentrancy/Reentrancy.sol` contains a classic reentrancy vulnerability sample for Slither detection and MVP acceptance testing.

## Bundled ZIP (recommended)

The repository includes a ready-to-upload sample:

```
examples/reentrancy-example.zip
```

Use it for README quick start, demo recording (see [docs/demo-script.md](../docs/demo-script.md)), and CI integration tests.

## Rebuild from source

To regenerate the ZIP from source:

```bash
# Linux / macOS
cd examples/reentrancy && zip -r ../reentrancy-example.zip .

# Windows PowerShell
cd examples/reentrancy
Compress-Archive -Path * -DestinationPath ..\reentrancy-example.zip -Force
```

Upload `reentrancy-example.zip` in the web UI to complete end-to-end acceptance.
