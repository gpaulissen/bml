#!/bin/sh
if [ -z "${UID}" ]; then
    echo exec "$@"
    exec "$@"
else
    GID=${GID:-${UID}}
    groupadd -g $GID -o host_user
    useradd --shell /bin/bash -u $UID -g $GID -o -c "" -Md /host_user host_user
    echo exec su-exec host_user "$@"
    exec su-exec host_user "$@"
fi
