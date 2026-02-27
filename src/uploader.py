import os
from pathlib import Path


def save_uploaded_file(uploaded_file, dest_dir="data"):
    """Write a Streamlit UploadedFile object to disk.

    The file is stored under ``dest_dir`` using its original name. The
    directory is created if necessary. Returns the path to the saved file.
    """
    Path(dest_dir).mkdir(parents=True, exist_ok=True)
    target = Path(dest_dir) / uploaded_file.name
    # `UploadedFile` provides a `getbuffer()` method which returns the
    # contents as a memoryview.
    with open(target, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(target)
