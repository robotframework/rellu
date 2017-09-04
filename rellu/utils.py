import invoke


def run(command, dry_run=False, **config):
    if dry_run:
        print(command)
    else:
        invoke.run(command, echo=True, **config)
