# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink\\__init__.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink/addons', 'addons'), ('D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink/core', 'core'), ('D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink/gui', 'gui'), ('D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink/grammars', 'grammars'), ('D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink/tools', 'tools'), ('D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink/setup', 'setup'), ('D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink/icons', 'icons'), ('D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink/package_config.yaml', '.'), ('D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink/requirements.txt', '.'), ('D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink/build_natlink_dll.py', '.'), ('D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink/develop_with_fake_runtime.py', '.'), ('D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink/packages', 'packages')],
    hiddenimports=['wx', 'wx.adv', 'dragonfly', 'natlink', 'natlinkcore', 'dtactions', 'yaml', 'comtypes', 'subprocess', 'tempfile', 'platform', 'shutil', 'pathlib', 'os', 'sys'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'tkinter', 'IPython', 'jupyter'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FTNatlink',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\Projects\\TEST_INSTALLATION_NATLINK\\FTNatlink\\icons\\app_icon.ico'],
)
