# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/sasenyzhou/Documents/Development/Design/App_Design/20180314/BurninTools/0.1.9/MacOS/main.py'],
             pathex=['/Users/sasenyzhou/Documents/Development/Design/App_Design/20180314/BurninTools/0.1.9/MacOS/'],
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
             icon='/Users/sasenyzhou/Documents/Development/Design/App_Design/20180314/BurninTools/0.1.9/burnintools.icns',
             bundle_identifier=None,
             info_plist={
                'CFBundleName': 'BurninTools.app',
                'CFBundleDisplayName': 'BurninTools',
                'CFBundleVersion': "0.1.10b",
                'CFBundleShortVersionString': "0.1.10b",
                'NSHumanReadableCopyright': "Copyright © 2018, SasenyZhou, All Rights Reserved",
                'NSHighResolutionCapable': 'True',
                })
