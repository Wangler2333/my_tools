# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/cr/Desktop/TEST/0.0.3/MacOS/main.py'],
             pathex=['/Users/cr/Desktop/TEST'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='OverlayCheck',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='OverlayCheck.app',
             icon='/Users/cr/Desktop/TEST/OverlayCheck.icns',
             bundle_identifier=None,
             info_plist={
                'CFBundleName': 'OverlayCheck.app',
                'CFBundleDisplayName': 'OverlayCheck',
                'CFBundleVersion': "0.0.6",
                'CFBundleShortVersionString': "0.0.6",
                'NSHumanReadableCopyright': "Copyright © 2017, SasenyZhou, All Rights Reserved",
                'NSHighResolutionCapable': 'True',
                })
