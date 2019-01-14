from .. import app
from json import load, dump


def get_downloads(id=None):
    with open(app.root_path + '/state.json', 'r') as file:
        downloads = load(file)
    if id:
        for index, download in enumerate(downloads):
            if download["id"] == id:
                break
        else:
            return None
        return download
    else:
        return downloads


def update_downloads(downloads):
    with open(app.root_path + '/state.json', 'w') as file:
        dump(downloads, file, indent="\t")


def update_download(updated_download):
    downloads = get_downloads()
    for index, download in enumerate(downloads):
        if download["id"] == updated_download["id"]:
            break
    else:
        return False
    downloads[index] = updated_download
    update_downloads(downloads)
    return True


def append_download(download):
    downloads = get_downloads()
    downloads.append(download)
    update_downloads(downloads)


def remove_download(id, ignore_status=False):
    downloads = get_downloads()
    for index, download in enumerate(downloads):
        if download["id"] == id:
            break
    else:
        return 404
    if download["progress"]["status"] != "finished" and not ignore_status:
        return 422
    downloads.pop(index)
    update_downloads(downloads)
    return 204


def remove_finished_downloads():
    downloads = get_downloads()
    for index, download in enumerate(downloads):
        if download["progress"]["status"] == "finished":
            downloads.pop(index)
    update_downloads(downloads)
