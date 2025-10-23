"""
Script to download pre-built natlink binary from GitHub releases
"""

import urllib.request
import os
import sys

# URLs for different Python versions
NATLINK_RELEASES = {
    "3.13": "https://github.com/dictation-toolbox/natlink/releases/download/v5.5.8/natlink-5.5.8-cp313-cp313-win32.whl",
    "3.12": "https://github.com/dictation-toolbox/natlink/releases/download/v5.5.8/natlink-5.5.8-cp312-cp312-win32.whl",
    "3.11": "https://github.com/dictation-toolbox/natlink/releases/download/v5.5.8/natlink-5.5.8-cp311-cp311-win32.whl",
}


def get_python_version():
    """Get Python version as string like '3.13'"""
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def download_natlink_wheel():
    """Download the appropriate natlink wheel for current Python version"""
    py_version = get_python_version()

    print(f"Python version: {py_version}")

    if py_version not in NATLINK_RELEASES:
        print(f"❌ No pre-built natlink binary available for Python {py_version}")
        print(f"Available versions: {', '.join(NATLINK_RELEASES.keys())}")
        return False

    url = NATLINK_RELEASES[py_version]
    filename = os.path.basename(url)

    print(f"Downloading from: {url}")
    print(f"Saving to: {filename}")

    try:
        urllib.request.urlretrieve(url, filename)
        print(f"✅ Downloaded {filename}")
        print(f"\nNow run:")
        print(f"  .venv\\Scripts\\pip.exe install {filename}")
        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print(
            "\nAlternative: Visit https://github.com/dictation-toolbox/natlink/releases"
        )
        print("and manually download the appropriate .whl file")
        return False


if __name__ == "__main__":
    download_natlink_wheel()
