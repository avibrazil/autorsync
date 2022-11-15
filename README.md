# Auto rsync

Command to automate execution of various rsync commands based on profiles defined on a YAML configuration file.

## Installation

```shell
pip3 install autorsync --user
```

## Usage

### Organize Profiles in `~/autorsync.yaml`
Here is an example with some defaults and a few profiles:

```yaml
DEFAULTS:
    source_part1: /media/Media
    target_part1: user@remote.host.com:/media/backup/filesets
    delete: True
    backup: True
    backup_dir: ../deleted/{{time.strftime('%Y.%m.%d-%H.%M.%S')}}/
    background: False

profiles:
    - name: books
      source_part2: Books/
      target_part2: '{{hostname}}.books/files'
      background: True

    - name: nextcloud.data
      source: /var/lib/nextcloud/data
      target_part2: '{{hostname}}.nextcloud_files'
```

**Notes about this configuration**
- All profiles inherit parameters from `DEFAULTS`. If parameter isn’t set in the profile,
the value defined in `DEFAULTS` will be used.
- For each profile, the Source is defined by `source` parameter, or, if not defined, by `source_part1/source_part2`
- Target follows same logic: `target` or `target_part1/target_part2`
- `delete` makes rsync delete files in target that are absent in source
- `backup` and `backup_dir` makes rsync save backups on target of deleted or modified
files. Value on `backup_dir` is a path relative to target folder
- You can use Jinja logic in path parts, surrounded by `{{}}`. Currently these are the available variables:
    - `time`, a Python `datetime.datetime` object which includes local timezone
    - `hostname`, such as “rocket”
    - `username`, as “joanbaez”
    - `home`, as “/home/joanbaez”
    - `userid`, as “504”
    - `gecos`, as “Joan Baez”

### Execution
- Show all profiles:
```shell
autorsync -l
```
- Run rsync for all profiles:
```shell
autorsync
```
- Run rsync only for profile `books`
```shell
autorsync -p books
```

- Simulate rsync only for profile `books` (force rsync’s `--dry-run`)
```shell
autorsync -n -p books
```
or
```shell
autorsync --dry-run -p books
```

- Run rsync for 2 profiles from a non-default configuration file:
```shell
autorsync -c /etc/autorsync.yaml -p "books, music, photos"
```
