import zipfile
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.config import settings

ALLOWED_FILE_EXTENSIONS = {
    ".sol",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".js",
    ".ts",
    ".lock",
    ".txt",
    ".md",
}

ALLOWED_FILE_NAMES = {
    ".gitignore",
    ".solhint.json",
    ".solhintignore",
    ".prettierrc",
    ".prettierignore",
    "foundry.toml",
    "hardhat.config.js",
    "hardhat.config.ts",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "remappings.txt",
    "truffle-config.js",
    "yarn.lock",
}


def _is_safe_path(base: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def validate_zip_file(file: UploadFile) -> None:
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip project archives are supported")


def _is_allowed_project_file(name: str) -> bool:
    path = Path(name)
    lower_name = path.name.lower()
    return lower_name in ALLOWED_FILE_NAMES or path.suffix.lower() in ALLOWED_FILE_EXTENSIONS


def _validate_zip_member(info: zipfile.ZipInfo, project_dir: Path) -> Path | None:
    if info.is_dir():
        return None

    name = info.filename.replace("\\", "/")
    if name.startswith("/") or ".." in Path(name).parts:
        raise HTTPException(status_code=400, detail="ZIP contains invalid paths")

    if name.startswith("__MACOSX/") or name.endswith("/.DS_Store"):
        return None

    if not _is_allowed_project_file(name):
        raise HTTPException(
            status_code=400,
            detail=f"ZIP contains unsupported file type: {Path(name).name}",
        )

    max_file_bytes = settings.max_zip_file_mb * 1024 * 1024
    if info.file_size > max_file_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"ZIP member exceeds size limit (max {settings.max_zip_file_mb} MB): {Path(name).name}",
        )

    is_symlink = (info.external_attr >> 16) & 0o120000 == 0o120000
    if is_symlink:
        raise HTTPException(status_code=400, detail="ZIP must not contain symbolic links")

    target = project_dir / name
    if not _is_safe_path(project_dir, target):
        raise HTTPException(status_code=400, detail="ZIP contains invalid paths")

    return target


async def save_and_extract_zip(file: UploadFile, job_dir: Path) -> Path:
    validate_zip_file(file)

    content = await file.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds size limit (max {settings.max_upload_mb} MB)",
        )
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    zip_path = job_dir / "upload.zip"
    zip_path.write_bytes(content)

    project_dir = job_dir / "project"
    project_dir.mkdir(parents=True, exist_ok=True)

    sol_files: list[Path] = []

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            members: list[tuple[zipfile.ZipInfo, Path]] = []
            total_uncompressed = 0

            for info in zf.infolist():
                target = _validate_zip_member(info, project_dir)
                if target is None:
                    continue

                members.append((info, target))
                total_uncompressed += info.file_size

            if len(members) > settings.max_zip_files:
                raise HTTPException(
                    status_code=400,
                    detail=f"ZIP contains too many files (max {settings.max_zip_files})",
                )

            max_extracted_bytes = settings.max_extracted_mb * 1024 * 1024
            if total_uncompressed > max_extracted_bytes:
                raise HTTPException(
                    status_code=400,
                    detail=f"ZIP extracted size exceeds limit (max {settings.max_extracted_mb} MB)",
                )

            for info, target in members:
                target.parent.mkdir(parents=True, exist_ok=True)

                with zf.open(info) as src, open(target, "wb") as dst:
                    dst.write(src.read())

                if target.name.lower().endswith(".sol"):
                    sol_files.append(target)

    except zipfile.BadZipFile as exc:
        raise HTTPException(status_code=400, detail="Invalid ZIP file") from exc

    if not sol_files:
        raise HTTPException(status_code=400, detail="ZIP contains no .sol files")

    return _resolve_project_root(project_dir)


def _resolve_project_root(project_dir: Path) -> Path:
    """If ZIP has a single top-level folder, use it as project root."""
    children = [p for p in project_dir.iterdir() if p.name != "__MACOSX"]
    if len(children) == 1 and children[0].is_dir():
        return children[0]
    return project_dir
