#!/bin/sh
set -e
cd ~/.vim_runtime



echo "Install settings vimrc to ~/.vimrc"

echo 'set runtimepath+=~/.vim_runtime

source ~/.vim_runtime/vimrcs/basic.vim
source ~/.vim_runtime/vimrcs/filetypes.vim
source ~/.vim_runtime/vimrcs/plugins_config.vim
source ~/.vim_runtime/vimrcs/extended.vim

try
source ~/.vim_runtime/my_configs.vim
catch
endtry' > ~/.vimrc

echo "Done"



echo "Update plugins"

python update_plugins.py

cd plugins/YouCompleteMe
git pull --rebase
git submodule update --init --recursive
echo "Updated YouCompleteMe"

echo "Install YouCompleteMe with semantic support for C-family language [y/N]: "
read a
if [ $a = 'y' ]; then
    python install.py --clang-complete;
else python install.py;
fi
echo "Done"



echo "Installed full version completed"
