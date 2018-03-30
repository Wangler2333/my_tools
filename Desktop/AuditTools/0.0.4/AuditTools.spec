# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Volumes/Seven-陈/_tools/Tools_For_Audit/0.0.4/MacOS/main.py'],
             pathex=['/Volumes/Seven-陈/_tools/Tools_For_Audit/0.0.4/MacOS/'],
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
          name='AuditTools',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='AuditTools.app',
             icon='/Volumes/Seven-陈/_tools/Tools_For_Audit/0.0.4/icns/homer.icns',
             bundle_identifier=None,
             info_plist={
                'CFBundleName': 'AuditTools.app',
                'CFBundleDisplayName': 'AuditTools',
                'CFBundleVersion': "0.0.4",
                'CFBundleShortVersionString': "0.0.4",
                'NSHumanReadableCopyright': "Copyright © 2018, Create By TE, All Rights Reserved",
                'NSHighResolutionCapable': 'True',
                })
