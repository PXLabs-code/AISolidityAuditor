# Threat model (ZIP upload)

## Attack surface

| Vector | Risk | Mitigation |
|--------|------|------------|
| ZIP path traversal (`../`) | Write outside job dir | Path validation; reject `..` and absolute paths |
| ZIP symbolic links | Read/write arbitrary files | Detect Unix symlink attributes and reject |
| ZIP bomb | Disk/memory exhaustion | 10 MB upload limit; post-extract size monitoring (post-MVP) |
| Malicious binaries | Code execution | Only `.sol` analysis; no execution of extracted binaries |
| API key leakage | Cost/abuse | Keys not persisted or logged; HTTPS recommended in production |
| Denial of service | Resource exhaustion | Slither 120s timeout; Semaphore(3); rate limiting |

## Trust boundaries

- **Untrusted**: user-uploaded ZIP contents
- **Trusted**: Slither, solc (preinstalled in Docker image)
- **Semi-trusted**: OpenAI API (user-provided key)

## Data retention

- Task directories retained for 24 hours by default, then auto-cleaned
- No user accounts; no long-term PII storage
