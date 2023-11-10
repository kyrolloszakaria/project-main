#!/usr/bin/env sh

git pull

if [ -z "$2" ]; then
	MAIN=project3
else
	MAIN=$1
	shift
fi

ARG="$1"
shift

pyb $MAIN -P inputfile="$ARG" "$@" 2>&1
