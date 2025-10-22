#!/usr/bin/env python
"""
Build script to create FTNatlink.exe
Creates a standalone executable from the FTNatlink project
"""

import PyInstaller.__main__
import os
import sys
from pathlib import Path

try:
    from PIL import Image

    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


def create_icon_from_image(project_root):
    """Convert JPEG images to ICO format for use with PyInstaller"""
    icons_dir = project_root / "icons"
    ico_file = icons_dir / "app_icon.ico"

    # If ICO already exists, use it
    if ico_file.exists():
        print(f"Found existing ICO file: {ico_file}")
        return ico_file

    # Look for JPEG files to convert
    jpeg_files = [
        icons_dir / "FTNatlink_BLUE.jpg",
        icons_dir / "FTNATLINK_DARK_BLUE.jpg",
    ]

    if not PILLOW_AVAILABLE:
        print("Pillow not available for image conversion")
        return None

    for jpeg_file in jpeg_files:
        if jpeg_file.exists():
            print(f"Converting {jpeg_file.name} to ICO format...")
            try:
                # Open and convert image
                with Image.open(jpeg_file) as img:
                    # Convert to RGBA if not already
                    if img.mode != "RGBA":
                        img = img.convert("RGBA")

                    # Resize to common icon sizes and save
                    # Create multiple sizes for better Windows compatibility
                    sizes = [
                        (16, 16),
                        (32, 32),
                        (48, 48),
                        (64, 64),
                        (128, 128),
                        (256, 256),
                    ]

                    # Save as ICO with multiple sizes
                    img.save(ico_file, format="ICO", sizes=sizes)
                    print(f"Created icon file: {ico_file}")
                    return ico_file

            except Exception as e:
                print(f"Failed to convert {jpeg_file.name}: {e}")
                continue

    print("No suitable image files found for icon conversion")
    return None


def build_exe():
    """Build FTNatlink executable using PyInstaller"""

    # Get project root
    project_root = Path(__file__).parent

    # Define paths
    main_script = project_root / "__init__.py"

    # Create or find icon file
    icon_file = create_icon_from_image(project_root)

    # Build arguments for PyInstaller
    args = [
        str(main_script),
        "--name=FTNatlink",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (GUI app)
        "--clean",
        f"--workpath={project_root}/build",
        f"--distpath={project_root}/dist",
        f"--specpath={project_root}",
        # Include necessary modules
        "--hidden-import=wx",
        "--hidden-import=wx.adv",
        "--hidden-import=dragonfly",
        "--hidden-import=natlink",
        "--hidden-import=natlinkcore",
        "--hidden-import=dtactions",
        "--hidden-import=yaml",
        "--hidden-import=comtypes",
        "--hidden-import=subprocess",
        "--hidden-import=tempfile",
        "--hidden-import=platform",
        "--hidden-import=shutil",
        # Additional imports for build functionality
        "--hidden-import=pathlib",
        "--hidden-import=os",
        "--hidden-import=sys",
        # Include data files and directories
        f"--add-data={project_root}/addons;addons",
        f"--add-data={project_root}/core;core",
        f"--add-data={project_root}/gui;gui",
        f"--add-data={project_root}/grammars;grammars",
        f"--add-data={project_root}/tools;tools",
        f"--add-data={project_root}/setup;setup",
        f"--add-data={project_root}/icons;icons",
        f"--add-data={project_root}/package_config.yaml;.",
        f"--add-data={project_root}/requirements.txt;.",
        # Include important Python scripts
        f"--add-data={project_root}/build_tools/build_natlink_dll.py;build_tools",
        f"--add-data={project_root}/development/develop_with_fake_runtime.py;development",
        # Include packages directory
        f"--add-data={project_root}/packages;packages",
        # Exclude unnecessary modules to reduce size
        "--exclude-module=matplotlib",
        "--exclude-module=tkinter",
        "--exclude-module=IPython",
        "--exclude-module=jupyter",
    ]

    # Add icon if available
    if icon_file and icon_file.exists():
        args.append(f"--icon={icon_file}")
        print(f"Using icon: {icon_file}")
    else:
        print("No icon found, building without icon")

    # Add version info if available
    version_args = [
        "--version-file=version_info.txt",  # We'll create this
    ]

    print("Building FTNatlink.exe...")
    print(f"Main script: {main_script}")
    print(f"Project root: {project_root}")

    # Run PyInstaller
    try:
        PyInstaller.__main__.run(args)
        print("Build completed successfully!")
        print(f"Executable created: {project_root}/dist/FTNatlink.exe")

        # Show file size
        exe_path = project_root / "dist" / "FTNatlink.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"File size: {size_mb:.1f} MB")

    except Exception as e:
        print(f"Build failed: {e}")
        return False

    return True


def create_version_info():
    """Create version info file for Windows executable"""
    version_content = """
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Sendhil RANDON'),
        StringStruct(u'FileDescription', u'FTNatlink - Dragon NaturallySpeaking Integration'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'FTNatlink'),
        StringStruct(u'LegalCopyright', u'Copyright © 2025 Sendhil RANDON'),
        StringStruct(u'OriginalFilename', u'FTNatlink.exe'),
        StringStruct(u'ProductName', u'FTNatlink'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""

    with open("version_info.txt", "w") as f:
        f.write(version_content)
    print("Created version_info.txt")


if __name__ == "__main__":
    print("FTNatlink Executable Builder")
    print("=" * 50)

    # Create version info
    create_version_info()

    # Build executable
    if build_exe():
        print("\nSuccess! Your FTNatlink.exe is ready!")
        print("Location: dist/FTNatlink.exe")
        print("\nUsage:")
        print("   - Double-click FTNatlink.exe to run")
        print("   - No Python installation needed on target machine")
        print("   - Includes all dependencies")
    else:
        print("\nBuild failed. Check error messages above.")
