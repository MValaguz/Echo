# -*- mode: python -*-


block_cipher = None


a = Analysis(['..\\source\\Echo.py'],
             pathex=[],
             binaries=[],
             datas=[					
		      ('..\\source\\qtdesigner\\*.py','.'),
			  ('..\\source\\qtdesigner\\icons\\*.*','icons\\'),			  
	           ],
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
          name='Echo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False, 
		  icon='..\\source\\qtdesigner\\icons\\Echo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Echo')
