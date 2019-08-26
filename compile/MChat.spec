# -*- mode: python -*-

block_cipher = None


a = Analysis(['..\\MChat.py'],
             pathex=['N:\\smi_job\\It&c\\mvalaguz\\17 - Python\\MChat'],
             binaries=[],
             datas=[
					('..\\icons\\*.*','icons'),
					('..\\help\\*.*','help'),
					('..\\computer_list.txt','.')
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
          name='MChat',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
		  icon='..\\icons\MChat.ico')
		  
