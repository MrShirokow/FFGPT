from invoke import Collection

from provision import (
    celery,
    ci,
    data,
    django,
    docker,
    frontend,
    git,
    k8s,
    open_api,
    project,
    tests,
)

ns = Collection(
    celery,
    ci,
    django,
    docker,
    data,
    project,
    tests,
    git,
    open_api,
    k8s,
    frontend,
)

# Configurations for run command
ns.configure(
    {
        "run": {
            "pty": True,
            "echo": True,
        },
    },
)
