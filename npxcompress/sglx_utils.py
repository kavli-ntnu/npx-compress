"""
This module contains functions that were origianlly taken from SpikeGLX_Datafile_Tools found
at http://billkarsh.github.io/SpikeGLX/#post-processing-tools
"""
from pathlib import Path
from typing import Dict


def read_meta(meta_full_path: Path) -> Dict[str, str]:
    # Parse ini file returning a dictionary whose keys are the metadata
    # left-hand-side-tags, and values are string versions of the right-hand-side
    # metadata values. We remove any leading '~' characters in the tags to match
    # the MATLAB version of readMeta.
    #
    # The string values are converted to numbers using the "int" and "float"
    # functions. Note that python 3 has no size limit for integers.
    #
    #

    meta_dict: Dict[str, str] = {}
    if not meta_full_path.exists():
        return meta_dict

    # print("meta file present")
    with meta_full_path.open() as f:
        mdat_list = f.read().splitlines()
        # convert the list entries into key value pairs
        for m in mdat_list:
            cs_list = m.split(sep="=")
            if cs_list[0][0] == "~":
                curr_key = cs_list[0][1 : len(cs_list[0])]
            else:
                curr_key = cs_list[0]
            meta_dict.update({curr_key: cs_list[1]})
    return meta_dict


def get_sample_rate(meta: Dict[str, str]) -> float:
    # Return sample rate as python float.
    # On most systems, this will be implemented as C++ double.
    # Use python command sys.float_info to get properties of float on your system.
    #
    if meta["typeThis"] == "imec":
        rate = float(meta["imSampRate"])
    else:
        rate = float(meta["niSampRate"])
    return rate


def get_num_saved_channels(meta: Dict[str, str]) -> int:
    return int(meta["nSavedChans"])
