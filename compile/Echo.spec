# -*- mode: python -*-

block_cipher = None


a = Analysis(['..\\source\\Echo.py'],
             pathex=[],
             binaries=[],
             datas=[					
					('..\\source\\qtdesigner\\icons\\*.*','icons\\'),
					('..\\source\\qtdesigner\\*.py','.'),					
			        ('..\\source\\*.py','.')		
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
          a.binaries,
          a.zipfiles,
          a.datas,
		  [],
          name='Echo',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
		  icon='..\\source\\qtdesigner\\icons\\Echo.ico')
		  
