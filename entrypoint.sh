#!/bin/sh

test -z "$DEBUG" || { id && set -x; }

# current user and group id
uid=`id -u`
gid=`id -g`

# wanted user and group id (default to current)
UID=${UID:-$uid}
GID=${GID:-$gid}

# user and group id of current user equal to wanted user?
if [ "$uid" -eq "$UID" -a "$gid" -eq "$GID" ]
then
    # just spawn the command
    exec "$@"   
else
    # must create a host user and group, add it to group bml (owner of software) and spawn if that succeeds
    addgroup --gid $GID host_user && \
        adduser --disabled-password --gecos "" --ingroup host_user --no-create-home --uid $UID host_user && \
        adduser host_user bml && \
        exec su-exec host_user "$@"
fi


