#!/bin/sh
if [ -z "${UID}" ]; then
    exec "$@"
else
    GID=${GID:-${UID}}
    addgroup --gid $GID host_user
    adduser --disabled-password --gecos "" --ingroup host_user --no-create-home --uid $UID host_user
    exec su-exec host_user "$@"
fi
