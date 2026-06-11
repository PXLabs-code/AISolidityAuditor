# Sandbox and execution boundaries

## Current isolation model

AISolidityAuditor treats uploaded projects as untrusted input.

The current Docker Compose deployment uses:

- A read-only container root filesystem.
- A writable `/data/jobs` volume for per-task working directories.
- A temporary `/tmp` tmpfs with `noexec` and `nosuid`.
- `no-new-privileges`.
- Dropped Linux capabilities.
- Process, memory, CPU, upload-size, file-count, extracted-size, and Slither timeout limits.
- ZIP path traversal, absolute path, symlink, unsupported-file, and ZIP-bomb checks.

Each audit is stored under its own task directory and removed by retention cleanup.

## Residual risks

- Slither and crytic-compile still execute inside the application container.
- Complex build systems may invoke compiler or dependency-resolution behavior that is hard to fully constrain.
- Docker Compose resource limits depend on the host Docker engine and deployment environment.
- The current web app does not yet create a fresh container per uploaded job.

## Recommended production posture

For public deployments, run the app behind HTTPS and an authentication/rate-limit layer, and prefer a worker model where each analysis job runs in a short-lived restricted container:

- Network disabled for uploaded project analysis by default.
- Read-only project input mount.
- Dedicated writable output directory.
- CPU, memory, pids, and wall-clock limits.
- Non-root user.
- No Docker socket mount.
- Strict cleanup after job completion.

## Grant hardening milestone

The next hardening milestone is to move from in-container subprocess execution to per-job worker isolation. The intended design is:

1. API accepts and validates ZIP upload.
2. API writes a sanitized project directory.
3. Worker starts a short-lived container with network disabled.
4. Worker mounts input read-only and output read-write.
5. Slither writes raw JSON to output.
6. API parses output, generates report/SARIF, and deletes temporary files after retention.
