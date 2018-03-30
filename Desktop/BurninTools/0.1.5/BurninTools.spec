# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/cr/Desktop/0.0.1/MacOS/main.py'],
             pathex=['/Users/cr/Desktop/0.0.1/MacOS/'],
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
          name='BurninTools',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='BurninTools.app',
             icon='/Users/cr/Desktop/0.0.1/failcheck.icns',
             bundle_identifier=None,
             info_plist={
                'CFBundleName': 'BurninTools.app',
                'CFBundleDisplayName': 'BurninTools',
                'CFBundleVersion': "0.1.5",
                'CFBundleShortVersionString': "0.1.5",
                'NSHumanReadableCopyright': "Copyright © 2018, SasenyZhou, All Rights Reserved",
                'NSHighResolutionCapable': 'True',
                })
