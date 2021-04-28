#!/bin/sh

if [ -z "${UID}" ]; then
    exec "$@"
else
    GID=${GID:-${UID}}
    groupadd -g $GID -o host_user
    useradd --shell /bin/bash -u $UID -g $GID -o -c "" -Md /host_user host_user
    exec gosu host_user "$@"
fi
