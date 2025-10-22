import zipfile
import shutil
from pathlib import Path
import json
import sys
import os

# Add core module to path for logging
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from core.logHandler import log

GRAMMAR_DIR = Path(__file__).parent.parent / "grammars"
ADDON_DIR = Path(__file__).parent.parent / "installed_addons"


def install_addon(addon_path):
    """
    Install an addon from a .natlink-addon file

    Args:
        addon_path: Path to the .natlink-addon file    Raises:
        FileNotFoundError: If addon file doesn't exist
        ValueError: If addon structure is invalid
        Exception: For other installation errors
    """
    addon_path = Path(addon_path)
    log.info(f"Starting addon installation: {addon_path.name}")

    # Validate addon file exists
    if not addon_path.exists():
        error_msg = f"Addon file not found: {addon_path}"
        log.error(error_msg)
        raise FileNotFoundError(error_msg)

    # Validate file extension
    if not addon_path.suffix == ".natlink-addon":
        error_msg = f"Invalid addon file type. Expected .natlink-addon, got: {addon_path.suffix}"
        log.error(error_msg)
        raise ValueError(error_msg)

    # Validate it's a zip file
    if not zipfile.is_zipfile(addon_path):
        error_msg = f"Addon file is not a valid zip archive: {addon_path.name}"
        log.error(error_msg)
        raise ValueError(error_msg)

    # Setup temp extraction directory
    temp_extract = Path(__file__).parent.parent / "_tmp_extract"
    log.debug(f"Using temp directory: {temp_extract}")

    try:
        # Clean up any existing temp directory
        if temp_extract.exists():
            log.debug("Cleaning up existing temp directory")
            shutil.rmtree(temp_extract)

        # Extract addon
        log.info("Extracting addon archive...")
        with zipfile.ZipFile(addon_path, "r") as zip_ref:
            zip_ref.extractall(temp_extract)

        # Validate addon structure
        metadata_file = temp_extract / "addon.json"
        if not metadata_file.exists():
            error_msg = "Invalid addon: missing addon.json metadata file"
            log.error(error_msg)
            raise ValueError(error_msg)

        # Read and validate metadata
        log.info("Reading addon metadata...")
        try:
            metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            error_msg = f"Invalid addon.json format: {e}"
            log.error(error_msg)
            raise ValueError(error_msg)

        # Validate required metadata fields
        required_fields = ["id", "name", "version"]
        for field in required_fields:
            if field not in metadata:
                error_msg = f"Invalid addon.json: missing required field '{field}'"
                log.error(error_msg)
                raise ValueError(error_msg)

        addon_id = metadata["id"]
        addon_name = metadata["name"]
        addon_version = metadata["version"]

        log.info(f"📝 Installing: {addon_name} v{addon_version} (ID: {addon_id})")

        # Ensure required directories exist
        GRAMMAR_DIR.mkdir(exist_ok=True)
        ADDON_DIR.mkdir(exist_ok=True)

        # Check if addon already exists
        dest_dir = GRAMMAR_DIR / addon_id
        if dest_dir.exists():
            log.warning(f"Addon already exists, removing old version: {dest_dir}")
            shutil.rmtree(dest_dir)

        # Validate that the addon contains grammar files or python files
        grammar_source = (
            temp_extract / "grammars"
            if (temp_extract / "grammars").exists()
            else temp_extract
        )

        # Look for Python files
        python_files = list(grammar_source.glob("*.py"))
        if not python_files:
            log.warning(
                f"⚠️  No Python files found in addon, checking subdirectories..."
            )
            # Check subdirectories for Python files
            for subdir in grammar_source.iterdir():
                if subdir.is_dir():
                    python_files.extend(subdir.glob("*.py"))

        if not python_files:
            error_msg = f"No Python grammar files found in addon: {addon_path.name}"
            log.error(error_msg)
            raise ValueError(error_msg)

        log.info(f"Found {len(python_files)} Python files to install")

        # Move addon files to destination
        log.info(f"📁 Installing to: {dest_dir}")
        if (temp_extract / "grammars").exists():
            shutil.move(str(temp_extract / "grammars"), str(dest_dir))
        else:
            # If no grammars folder, move the entire content
            dest_dir.mkdir(exist_ok=True)
            for item in temp_extract.iterdir():
                if item.name != "addon.json":  # Don't move metadata to grammars
                    if item.is_dir():
                        shutil.move(str(item), str(dest_dir / item.name))
                    else:
                        shutil.copy2(str(item), str(dest_dir / item.name))

        # Store metadata
        metadata_dest = ADDON_DIR / f"{addon_id}.json"
        shutil.copy2(str(metadata_file), str(metadata_dest))
        log.info(f"💾 Saved metadata to: {metadata_dest}")

        # Cleanup
        shutil.rmtree(temp_extract)
        log.info("🧹 Cleaned up temporary files")

        log.info(f"Successfully installed addon '{addon_name}' v{addon_version}")
        return {
            "id": addon_id,
            "name": addon_name,
            "version": addon_version,
            "files_installed": len(python_files),
        }

    except Exception as e:
        # Cleanup on error
        if temp_extract.exists():
            try:
                shutil.rmtree(temp_extract)
                log.debug("Cleaned up temp directory after error")
            except Exception as cleanup_error:
                log.warning(f"Failed to cleanup temp directory: {cleanup_error}")

        # Re-raise the original exception
        log.error(f"Addon installation failed: {e}")
        raise
