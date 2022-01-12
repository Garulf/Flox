from tempfile import gettempdir
from urllib import request
from pathlib import Path
from functools import wraps
import json
from time import time
from concurrent.futures import ThreadPoolExecutor


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

def refresh_cache(file_name:str, dir:str=gettempdir()):
    """
    Touch cache file
    """
    cache_file = Path(dir, file_name)
    if cache_file.exists():
        cache_file.touch()

def cache_path(file_name:str, dir:str=gettempdir()):
    """
    Return path to cache file
    """
    return Path(dir, file_name)

def remove_cache(file_name:str, dir:str=gettempdir()):
    """
    Remove cache file
    """
    cache_file = Path(dir, file_name)
    if cache_file.exists():
        cache_file.unlink()

def download_image(url:str, dir:str=gettempdir(), file_name:str=None, **kwargs):
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

def download_images(urls:list, dir:str=gettempdir(), max_workers=5, **kwargs):
    """
    Download images from urls and save them to dir using threads.

    Args:
        urls (list): list of image urls.
        dir (str): directory to save images.
        max_workers (int): number of workers to download images.

    Keyword Args:
        force_download (bool): Force download images even if they exists.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for url in urls:
            executor.submit(download_image, url, dir, **kwargs)