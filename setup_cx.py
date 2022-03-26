from cx_Freeze import Executable, setup

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {
    "packages": ["npxcompress"],
    "excludes": ["tkinter"],
    "include_msvcr": True,
}

company_name = "KavliInstitute"
product_name = "npx"
msi_data = {
    "ProgId": [
        (
            "Prog.Id",
            None,
            None,
            "Compress/decompress large-scale electrophysiological recordings based on Neuropixels",
            None,
            None,
        ),
    ],
}
bdist_msi_options = {
    "upgrade_code": "{55101C5B-D716-4A32-9272-2B3D0D958F4F}",
    "add_to_path": True,
    "all_users": False,
    "initial_target_dir": rf"[ProgramFilesFolder]\{company_name}\{product_name}",
    "summary_data": {
        "author": "Vadim Frolov <fralik@gmail.com>",
    },
    "data": msi_data,
}

base = None

setup(
    name="npxompress",
    version="0.0.1",
    author=company_name,
    description="Compress/decompress large-scale electrophysiological recordings based on Neuropixels",
    options={
        "build": {"build_exe": "dist"},  # output directory
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=[
        Executable("npxcompress/cli.py", base=base, target_name="npxcompress"),
    ],
)
