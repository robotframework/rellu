from .repo import get_repository


LABELS = '''
bug             ee0701
enhancement     84b6eb
task            ededed

alpha 1         ffffff
alpha 2         ffffff
alpha 3         ffffff
beta 1          ffffff
beta 2          ffffff
beta 3          ffffff
rc 1            ffffff
rc 2            ffffff
rc 3            ffffff

bwic            fbca04
depr            fef2c0

duplicate       000000
wont fix        000000
invalid         000000
in progress     ededed
pending         ededed
help wanted     ededed
needs review    ededed

prio-critical   00441b
prio-high       006d2c
prio-medium     238b45
prio-low        41ae76
'''


def initialize_labels(repository, username=None, password=None):
    repository = get_repository(repository, username, password)
    labels = [label.rsplit(None, 1) for label in LABELS.splitlines() if label]
    existing_labels = {label.name.lower(): label.name
                       for label in repository.get_labels()}
    for name, color in labels:
        normalized = name.lower()
        if normalized in existing_labels:
            label = repository.get_label(existing_labels[normalized])
            label.edit(name, color)
        else:
            repository.create_label(name, color)
