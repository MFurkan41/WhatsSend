# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:/Users/mfurk/Desktop/WP&Flask Projesi/app.py'],
             pathex=['C:\\Users\\mfurk\\Desktop\\WP&Flask Projesi'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          [],
          exclude_binaries=True,
          name='app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='C:\\Users\\mfurk\\Desktop\\WP&Flask Projesi\\iconfinder_092-robot-face-1_3099460.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app')
