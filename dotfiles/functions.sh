#!/bin/bash
function alert {
    osascript -e 'display notification "'"$1"'"'
}

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