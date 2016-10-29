#!/usr/bin/env sh

BASEDIR="/home/le/git-acme-inwx-python"

dns_inwx_add() {
    fulldomain=$1
    txtvalue=$2
    $BASEDIR/acme-inwx.py "$fulldomain" "$txtvalue"
}

dns_inwx_rm() {
    fulldomain=$1
    $BASEDIR/acme-inwx.py "$fulldomain"
}

