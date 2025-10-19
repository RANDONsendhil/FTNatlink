"""
Addon Manager Module
Handles addon installation, packaging, and management
"""

from .addon_installer import install_addon
from .addon_packager import package_addon

__all__ = ['install_addon', 'package_addon']
