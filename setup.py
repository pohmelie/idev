from cx_Freeze import setup, Executable


options = {
    "build_exe": {
        "includes": [],
        "create_shared_zip": False,
        "packages": [],
        "include_msvcr": True,
        "include_files": [
            "favicon.ico",
        ]
    }
}

executables = [
    Executable(
        script="idev.pyw",
        base="Win32GUI",
        targetName="idev.exe",
        compress=True,
        copyDependentFiles=True,
        appendScriptToExe=True,
        appendScriptToLibrary=False,
        icon="favicon.ico"
    )
]

setup(
    name="idev",
    version="0.0.1",
    description="",
    options=options,
    executables=executables,
)
