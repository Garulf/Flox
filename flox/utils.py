from tempfile import gettempdir
from urllib import request
from pathlib import Path
from functools import wraps


def cache(file_name:str, max_age=30, dir=gettempdir()):
    """
    Cache decorator
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_file = Path(dir, file_name)
            if not cache_file.exists() or time() - cache_file.stat().st_mtime > max_age or cache_file.stat().st_size == 0:
                data = func(*args, **kwargs)
                if len(data) != 0 and data is not None:
                    with open(cache_file, 'w') as f:
                        json.dump(data, f)
                return data
            else:
                with open(cache_file, 'r') as f:
                    return json.load(f)
        return wrapper
    return decorator

def download_image(self, url:str, dir:str=gettempdir(), file_name:str=None, **kwargs):
    """
    Download image from url and save it to dir

    Args:
        url (str): image url.
        dir (str): directory to save image.
        file_name (str): file name to save image.

    Keyword Args:
        force_download (bool): Force download image even if it exists.
    """
    force_download = kwargs.pop('force_download', False)
    if not file_name:
        file_name = url.split('/')[-1]
    full_path = Path(dir).joinpath(file_name)
    if not Path(full_path).exists() or force_download:
        with open(full_path, 'wb') as f:
            f.write(request.urlopen(url).read())
    return Path(full_path)