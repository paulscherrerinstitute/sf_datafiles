import json
import time
from pathlib import Path

from .utils import print_skip_warning, json_load, adjust_shape
from .ign import remove_ignored_filetypes_scan
from . import SFDataFiles, SFScanInfo

from partialjson.json_parser import JSONParser


class SFUnfinishedScanInfo(SFScanInfo):
    """
    Represents an unfinished scan from SwissFEL data, mimicking a finished SFScanInfo. It allows to iterate 
    over already available scan steps and waits for new data if the scan is still ongoing.

    If the scan is already finished, it behaves like a regular SFScanInfo.

    Args:
        fname (str): The filepath of the JSON file to be processed for scan information (e.g. scan.json).
        refresh_interval (int): Time in seconds to wait before checking for new data again. Default is 10 seconds.
    """

    def __init__(self, fname, refresh_interval=10):
        self.fname = fname
        self.finished = False
        self.refresh_interval = refresh_interval

        if is_finished_scan(fname):
            # simple case, it is a finished scan and our parent can handle it
            super().__init__(fname)
            self.finished = True
        else:
            # try to parse it as a partial JSON file
            self._parse_partial_json(fname)

    def _parse_partial_json(self, fname):
        with open(fname) as f:
            content = f.read()
        
        parser = JSONParser()
        self.info = info = parser.parse(content)

        # we try to extract as much information as possible,
        # leaving missing parts out if not available
        fnames = info.get("scan_files", [])
        self.files = remove_ignored_filetypes_scan(fnames)

        self.parameters = info.get("scan_parameters", [])

        values = info.get("scan_values", [])
        readbacks = info.get("scan_readbacks", [])

        # filter for empty values which can occur in the partial json parsing
        values = [vals for vals in values if vals]
        readbacks = [rb for rb in readbacks if rb]
        
        self.values = adjust_shape(values)
        self.readbacks = adjust_shape(readbacks)

    def __iter__(self):
        if self.finished:
            return super().__iter__()
        
        return self._generate_data()

    def _generate_data(self):
        """Generator that yields scan data as it becomes available during the scan."""
        yielded_count = 0
        
        while True:
            self._parse_partial_json(self.fname) 

            # Check if we have new files to yield
            while self.files and len(self.files) > yielded_count:
                fns = self.files[yielded_count]
                
                if not files_available_on_disk(fns):
                    time.sleep(self.refresh_interval)
                    continue  # Wait and recheck

                yielded_count += 1

                try:
                    with SFDataFiles(*fns) as data:
                        yield data
                except Exception as exc:
                    # TODO: Think about what could go wrong here and deal with it more specifically
                    sn = f"step {yielded_count - 1} {fns}"
                    print_skip_warning(exc, sn)
                    continue  # Try next file

            if is_finished_scan(self.fname) and (yielded_count >= len(self.files)):
                return  # Scan is finished, and we yielded all available files, stop iteration
            
            # Wait before checking again
            time.sleep(self.refresh_interval)


def is_finished_scan(fname):
    """ If the scan.json file is complete and valid the scan is finished."""
    try:
        json_load(fname)
    except json.JSONDecodeError:
        return False
    return True


def files_available_on_disk(fnames):
    """Check if all files for this step are available on disk and contain some data."""
    if all(Path(fn).exists() for fn in fnames):
       return all(Path(fn).stat().st_size > 0 for fn in fnames)
    return False