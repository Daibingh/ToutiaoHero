#!/bin/bash
__conda_setup="$('/home/hdb/opt/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/hdb/opt/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/hdb/opt/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/hdb/opt/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
conda activate base
export LD_LIBRARY_PATH=''
python toutiao.py
