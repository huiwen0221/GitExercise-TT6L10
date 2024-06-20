# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['grid-main.py'],
    pathex=[],
    binaries=[],
    datas=[('pomodoro helper.png', '.'), ('user setting1.png', '.'), ('timer.png', '.'), ('short break.png', '.'), ('long break.png', '.'), ('tomato cycle.png', '.'), ('reset all.png', '.'), ('sounds setting.png', '.'), ('bg color.png', '.'), ('volume.png', '.'), ('vol lbl.png', '.'), ('preset 1.png', '.'), ('save preset1.png', '.'), ('load preset1.png', '.'), ('preset 2.png', '.'), ('save preset2.png', '.'), ('load preset2.png', '.'), ('preset 3.png', '.'), ('save preset3.png', '.'), ('load preset3.png', '.'), ('statistics.png', '.'), ('studylist.png', '.'), ('defaultmode.png', '.'), ('studymode.png', '.'), ('relaxmode.png', '.'), ('open settings.png', '.'), ('tomato cycle.png', '.'), ('start2.png', '.'), ('stop.png', '.'), ('repeat3.png', '.'), ('music on.png', '.'), ('music off.png', '.'), ('Default Timer Alarm.wav', '.'), ('Default SB.wav', '.'), ('Default Microwave LB.wav', '.'), ('Autumn Garden.mp3', '.'), ('Study Referee Alarm.wav', '.'), ('Study Churchbell SB.wav', '.'), ('Study Great Harp LB.wav', '.'), ('Relax Chime Alarm.wav', '.'), ('Relax WindChimes SB.wav', '.'), ('Relax Harp LB.wav', '.'), ('pomodorohelper.db', '.'), ('tasks.db', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='grid-main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
