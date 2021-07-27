#!/bin/bash
function alert {
    osascript -e 'display notification "'"$1"'"'
}

function proxy {
    ssh -D 9000 -p2200 root@home.nicolasbouliane.com
}