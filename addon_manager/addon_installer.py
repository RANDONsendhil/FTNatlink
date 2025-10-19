import zipfile
import shutil
from pathlib import Path
import json

GRAMMAR_DIR = Path(__file__).parent.parent / "grammars"
ADDON_DIR = Path(__file__).parent.parent / "installed_addons"

def install_addon(addon_path):
    addon_path = Path(addon_path)
    if not addon_path.exists():
        raise FileNotFoundError(f"Addon not found: {addon_path}")

    # Extract addon
    temp_extract = Path(__file__).parent.parent / "_tmp_extract"
    if temp_extract.exists():
        shutil.rmtree(temp_extract)
    with zipfile.ZipFile(addon_path, 'r') as zip_ref:
        zip_ref.extractall(temp_extract)

    # Read metadata
    metadata_file = temp_extract / "addon.json"
    if not metadata_file.exists():
        raise ValueError("Invalid addon: missing addon.json")
    metadata = json.loads(metadata_file.read_text())
    addon_id = metadata.get("id")

    # Move grammars to grammars/addon_id
    dest_dir = GRAMMAR_DIR / addon_id
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    shutil.move(str(temp_extract / "grammars"), dest_dir)

    # Store metadata
    ADDON_DIR.mkdir(exist_ok=True)
    shutil.copy2(metadata_file, ADDON_DIR / f"{addon_id}.json")

    shutil.rmtree(temp_extract)

    print(f"✅ Installed addon '{metadata['name']}' (v{metadata['version']})")
