import uuid
from pathlib import Path
from fastapi import UploadFile

ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def save_file(
    file: UploadFile,
    subfolder: str,
    allowed_exts: set = ALLOWED_IMAGE_EXTS,
    max_size: int = MAX_FILE_SIZE,
):
    """
    Saves file inside app/static/uploads/<subfolder>
    Returns path usable by frontend: /static/uploads/<subfolder>/<filename>
    """

    if not file or not file.filename:
        return None

    ext = Path(file.filename).suffix.lower()

    if ext not in allowed_exts:
        raise ValueError("Invalid file type")

    contents = file.file.read()
    size = len(contents)

    if size > max_size:
        raise ValueError("Max file size exceeded")

    # Locate project root
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent  # -> RUNAMARGACRM

    upload_dir = project_root / "app" / "static" / "uploads" / subfolder
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4()}{ext}"
    save_path = upload_dir / filename

    with open(save_path, "wb") as f:
        f.write(contents)

    # 🔑 RETURN WEB PATH (NOT FILESYSTEM PATH)
    return f"/static/uploads/{subfolder}/{filename}"

def delete_static_file(web_path: str) -> bool:
    if not web_path or not web_path.startswith("/static/"):
        return False

    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent

    fs_path = project_root / "app" / web_path.lstrip("/")

    if fs_path.exists():
        fs_path.unlink()
        return True

    return False
