import zipfile
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.config import settings


def _is_safe_path(base: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def validate_zip_file(file: UploadFile) -> None:
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip project archives are supported")


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
            for info in zf.infolist():
                if info.is_dir():
                    continue

                name = info.filename.replace("\\", "/")
                if name.startswith("/") or ".." in Path(name).parts:
                    raise HTTPException(status_code=400, detail="ZIP contains invalid paths")

                if name.startswith("__MACOSX/") or name.endswith("/.DS_Store"):
                    continue

                target = project_dir / name
                if not _is_safe_path(project_dir, target):
                    raise HTTPException(status_code=400, detail="ZIP contains invalid paths")

                target.parent.mkdir(parents=True, exist_ok=True)

                is_symlink = (info.external_attr >> 16) & 0o120000 == 0o120000
                if is_symlink:
                    raise HTTPException(status_code=400, detail="ZIP must not contain symbolic links")

                with zf.open(info) as src, open(target, "wb") as dst:
                    dst.write(src.read())

                if name.lower().endswith(".sol"):
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
