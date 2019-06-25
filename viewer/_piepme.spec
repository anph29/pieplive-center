# -*- mode: python -*-

block_cipher = None

added_files = [
  ( 'src', 'src' )
]

a = Analysis(['piepme.py'],
             pathex=["D:\\QueenB\\PiepLive-Center\\viewer", "C:/Program Files (x86)/VideoLAN/VLC/"],
             binaries=[("C:/Program Files (x86)/VideoLAN/VLC/plugins/*", "plugins"),("C:/Program Files (x86)/VideoLAN/VLC/libvlc.dll", ".")],
             datas=added_files,
             hiddenimports=['packaging','packaging.version','python-vlc'],
             hookspath=[],
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
          name='piepview',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False, icon='src\\icons\\logo-viewer.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='piepview')
