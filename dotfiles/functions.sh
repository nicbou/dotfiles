#!/bin/bash

PATH_TO_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Usage:
# `alert "Hello world"`
function alert {
    osascript -e 'display notification "'"$1"'"'
}

# Usage:
# `proxy on`
# `proxy off`
function proxy {
    is_proxy_on=$(networksetup -getsocksfirewallproxy wi-fi | grep "No")
    if [ -n "$is_proxy_on" ] | [ "$1" == "on" ]; then
        echo "Turning proxy on"
        sudo networksetup -setsocksfirewallproxystate wi-fi on
        ssh -D 9000 -p2200 root@home.nicolasbouliane.com
    else
        echo "Turning proxy off"
        sudo networksetup -setsocksfirewallproxystate wi-fi off
    fi
}

# Usage:
# `project HomeServer`
function project {
    python3 "$PATH_TO_SCRIPT_DIR/../scripts/project.py" "$@"
}

# Usage:
# `webclip screencap.mov output.mp4`
function webclip {
    ffmpeg -an -i "$1" -vf "scale='min(1200,iw)':-2" -vcodec libx264 -pix_fmt yuv420p -profile:v baseline -level 3 "$2"
}