#!/bin/bash

SRC=$(cd $(dirname $0)/..; pwd)

git config --global --add safe.directory $SRC
pre-commit install

# チェック用文字列
check_string="Git prompt settings"

# .bashrcを読み込んでチェック
if grep -q "$check_string" ~/.bashrc; then
    echo "Git prompt settings already exist in .bashrc"
else
    # git-prompt
    git clone https://github.com/magicmonty/bash-git-prompt.git ~/.bash-git-prompt --depth=1
    echo -e "\n\n# Git prompt settings" >> ~/.bashrc
    echo "export GIT_PROMPT_ONLY_IN_REPO=1" >> ~/.bashrc
    echo "source ~/.bash-git-prompt/gitprompt.sh" >> ~/.bashrc

    # git-completion
    curl https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -o ~/.git-completion.bash
    echo "source ~/.git-completion.bash" >> ~/.bashrc

    # 設定を反映
    source ~/.bashrc
fi
