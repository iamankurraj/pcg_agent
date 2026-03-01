# asset_pipeline/local_search.py

from pathlib import Path
from config import ASSET_ROOT, ALLOWED_EXTENSIONS


# Set this to True if you want only meshes returned
MESH_ONLY = False


def detect_asset_type(file_path: str, file_name: str):
    path = file_path.lower()
    name = file_name.lower()

    if "meshes" in path or name.startswith("sm_"):
        return "StaticMesh"
    elif "materials" in path or name.startswith("mi_") or name.startswith("m_"):
        return "Material"
    elif "textures" in path or name.startswith("t_"):
        return "Texture"
    else:
        return "Unknown"


def convert_to_unreal_path(file_path: Path):
    """
    Converts:
    C:\Project\Content\Meshes\Tree\SM_Tree.uasset

    Into:
    /Game/Meshes/Tree/SM_Tree
    """

    try:
        relative_path = file_path.relative_to(Path(ASSET_ROOT))
    except ValueError:
        return str(file_path)

    unreal_path = "/Game/" + str(relative_path).replace("\\", "/")

    if unreal_path.endswith(".uasset"):
        unreal_path = unreal_path[:-7]

    return unreal_path
def search_local_assets(keywords):
    root = Path(ASSET_ROOT)

    if not root.exists():
        raise FileNotFoundError(f"Asset root not found: {ASSET_ROOT}")

    ignored = {
        "texture", "mesh", "material",
        "ue5", "unreal", "engine",
        "asset", "download", "free"
    }

    # remove weak keywords
    filtered_keywords = [
        k.lower()
        for k in keywords
        if k.lower() not in ignored and len(k) > 3
    ]

    # If no meaningful keywords, skip local search
    if not filtered_keywords:
        return []

    matches = []

    for file in root.rglob("*"):
        if not file.is_file():
            continue

        if file.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        file_name = file.name.lower()
        full_path = str(file).lower()

        asset_type = detect_asset_type(str(file), file.name)

        relevance_hits = sum(
            1 for keyword in filtered_keywords
            if keyword in file_name or keyword in full_path
        )

        if relevance_hits > 0:
            matches.append({
                "name": file.name,
                "type": asset_type,
                "filesystem_path": str(file),
                "unreal_path": convert_to_unreal_path(file),
                "source": "local"
            })

    return matches[:20]   # hard cap