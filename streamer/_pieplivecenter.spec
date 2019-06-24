# -*- mode: python -*-
from kivy_deps import sdl2, glew
block_cipher = None

added_files = [
  ( 'src\\ui', 'src\\' ),
  ( 'src\\cfg', 'src\\' ),
  ( 'src\\musics', 'src\\' ),
  ( 'src\\images', 'src\\' ),
  ( 'src\\fonts', 'src\\' ),
  ( 'pieplivecenter.kv', '.' ),
  ('Lib\\site-packages\\cv2\\opencv_ffmpeg410.dll', 'cv2'),
  ('Lib\\site-packages\\_sounddevice_data\\portaudio-binaries\\libportaudio32bit.dll', '_sounddevice_data\\portaudio-binaries')
]

a = Analysis(['pieplivecenter.py'],
             pathex=['D:\\QueenB\\PiepLive-Center\\streamer'],
             binaries=[],
             datas=added_files,
             hiddenimports=['six','packaging','packaging.version','backend_kivy','win32timezone'],
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
          name='pieplivecenter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False, icon='src\\images\\logo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='pieplivecenter')
