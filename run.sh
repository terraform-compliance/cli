#!/usr/bin/env bash

PARAMETERS="terraform-compliance "

if [[ -n $1 ]]; then
    PARAMETERS+=" -p \"$1\""
fi

if [[ -n $2 ]]; then
    PARAMETERS+=" -f \"git:$2\""
fi

if [[ -n $3 ]]; then
    PARAMETERS+=" -q"
fi

if [[ -n $4 ]]; then
    PARAMETERS+=" -n"
fi

if [[ -n $5 ]]; then
    PARAMETERS+=" -S"
fi

if [[ -n $6 ]]; then
    PARAMETERS+=" -i \"$6\""
fi

echo "Parameters: $PARAMETERS"

$PARAMETERS
