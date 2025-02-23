# -*- mode: python -*-
import distutils
if distutils.distutils_path.endswith('__init__.py'):
  distutils.distutils_path = os.path.dirname(distutils.distutils_path)
block_cipher = None

added_files = [
  ( 'resource.zip', '.' )
]

a = Analysis(['piepme.py'],
             pathex=["D:\\QueenB\\PiepLive-Center\\viewer", "C:/Program Files (x86)/VideoLAN/VLC/"],
             binaries=[("C:/Program Files (x86)/VideoLAN/VLC/plugins/*", "plugins"),("C:/Program Files (x86)/VideoLAN/VLC/libvlc.dll", ".")],
             datas=added_files,
             hiddenimports=['packaging','packaging.version','python-vlc'],
             hookspath=["D:\\QueenB\\PiepLive-Center\\viewer\\hook"],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='piepmanager',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True, icon='..\\resource\\icons\\logo-viewer.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='piepmanager')
