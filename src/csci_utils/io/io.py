from atomicwrites import atomic_write as _backend_writer, AtomicWriter
import os, io
from contextlib import contextmanager
import tempfile
from typing import ContextManager, Union

def split_file_extension(path: Union[str, os.PathLike]):
    """
    Returns the filename and extension separately

    Args:
        path: file path

    Returns:
        base, extension
    """

    filename = os.path.basename(path)
    try:
        extension = "." + str(filename).split(".", 1)[1]
        base = str(filename).split(".", 1)[0]
    except IndexError:
        # no dot in filename means there will be no extension
        extension = ""
        base = full_filename
    return base, extension

class SuffixWriter(AtomicWriter):
    def __init__(self, path: Union[str, os.PathLike], mode: str, overwrite: bool, new_default: str, **open_kwargs):
        super().__init__(path, mode, overwrite, **open_kwargs)
        self.new_default = new_default
        self.dir = os.path.normpath(os.path.dirname(self._path))

    def get_fileobject(self, prefix=tempfile.template, **kwargs):
        """ 
        Generates the temporary file, preserving the filename extension of the target file.

        Args:
            prefix: prefix to tempfile name
            **kwargs: other open kwargs

        Returns:
            file object

        """
        base, extension = split_file_extension(self._path)

        if base == "":
            base = self.new_default
            self._path = os.path.join(self.dir, base + extension)

        descriptor, name = tempfile.mkstemp(suffix=extension, prefix=prefix, dir=self.dir)
        os.close(descriptor)

        kwargs["mode"] = self._mode
        kwargs["file"] = name
        return io.open(**kwargs)

@contextmanager
def atomic_write(file, mode="w", new_default="asdf", as_file=True, **kwargs):
    """  
    Atomically writes a file as a context manager.  Will not write the file if it can't complete the operation

    Args:
        file: filepath
        mode: filemode - given atomicity expectation, I think this always wants to be 'w'
        new_default: filename if not given
        as_file: whether to yield actual file or just the name

    """
    with _backend_writer(writer_cls=SuffixWriter, path=str(file), mode=mode, overwrite=False, new_default=new_default, **kwargs) as f:
        if as_file:
            yield f
        else:
            yield f.name


