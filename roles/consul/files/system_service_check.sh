#!/bin/bash

usage() {
    echo "usage: ${0##*/} [ service ]"
    exit 1
}

check() {
    res=$(service "$1" status)
    if [ $? -gt 1 ];
    then
        exit 2
    fi
    code=$(echo $res | grep running | wc -l)
    if [ $code == 1 ];
    then
        exit 0
    else
        exit 2
    fi
}

main() {
    [[ -z "$1" ]] && usage || check "$1"
}

main "$@"

# EOF
