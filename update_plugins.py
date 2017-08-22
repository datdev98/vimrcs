try:
    import concurrent.futures as futures
except ImportError:
    try:
        import futures
    except ImportError:
        futures = None

import zipfile
import shutil
import tempfile
import requests

from os import path


# --- Globals ----------------------------------------------
THEMES = """
lightline.vim https://github.com/itchyny/lightline.vim
mayansmoke https://github.com/vim-scripts/mayansmoke
peaksea https://github.com/vim-scripts/peaksea
vim-colors-solarized https://github.com/altercation/vim-colors-solarized
vim-irblack https://github.com/wesgibbs/vim-irblack
vim-pyte https://github.com/therubymug/vim-pyte
""".strip()
PLUGINS = """
ack.vim https://github.com/mileszs/ack.vim
ctrlp.vim https://github.com/ctrlpvim/ctrlp.vim
nerdtree https://github.com/scrooloose/nerdtree
open_file_under_cursor.vim https://github.com/amix/open_file_under_cursor.vim
syntastic https://github.com/vim-syntastic/syntastic
ultisnips https://github.com/SirVer/ultisnips
vim-commentary https://github.com/tpope/vim-commentary
vim-fugitive https://github.com/tpope/vim-fugitive
vim-gitgutter https://github.com/airblade/vim-gitgutter
vim-snippets https://github.com/honza/vim-snippets
vim-surround https://github.com/tpope/vim-surround
xmledit https://github.com/sukima/xmledit/
vim-yankstack https://github.com/maxbrunsfeld/vim-yankstack
""".strip()

GITHUB_ZIP = '%s/archive/master.zip'

PLUGINS_DIR = path.join(path.dirname(__file__), 'plugins')
THEMES_DIR = path.join(path.dirname(__file__), 'themes')
SOURCE_DIR = PLUGINS_DIR


def download_extract_replace(plugin_name, zip_path, temp_dir, source_dir):
    temp_zip_path = path.join(temp_dir, plugin_name)

    # Download and extract file in temp dir
    req = requests.get(zip_path)
    open(temp_zip_path, 'wb').write(req.content)

    zip_f = zipfile.ZipFile(temp_zip_path)
    zip_f.extractall(temp_dir)

    plugin_temp_path = path.join(temp_dir,
                                 path.join(temp_dir, '%s-master' % plugin_name))

    # Remove the current plugin and replace it with the extracted
    plugin_dest_path = path.join(source_dir, plugin_name)

    try:
        shutil.rmtree(plugin_dest_path)
    except OSError:
        pass

    shutil.move(plugin_temp_path, plugin_dest_path)

    print('Updated {0}'.format(plugin_name))


def update(plugin, source_dir=SOURCE_DIR):
    name, github_url = plugin.split(' ')
    zip_path = GITHUB_ZIP % github_url
    download_extract_replace(name, zip_path,
                             temp_directory, source_dir)


if __name__ == '__main__':
    temp_directory = tempfile.mkdtemp()

    try:
        if futures:
            with futures.ThreadPoolExecutor(16) as executor:
                SOURCE_DIR = PLUGINS_DIR
                executor.map(update, PLUGINS.splitlines())
                SOURCE_DIR = THEMES_DIR
                executor.map(update, THEMES.splitlines())
        else:
            [update(x, PLUGINS_DIR) for x in PLUGINS.splitlines()]
            [update(x, THEMES_DIR) for x in THEMES.splitlines()]
    finally:
        shutil.rmtree(temp_directory)
