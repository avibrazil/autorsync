# Auto rsync

Command to automate execution of various rsync commands based on profiles
defined on a YAML configuration file.

* **Instead of doing:**
    ```shell
    rsync -avySH --delete --backup --backup-dir=../deleted/$timestamp/ "/media/Media/Photos" "user@host.com:/media/backup/filesets/$hostname.photos"
    ```

    **Just do:**
    ```shell
    autorsync -p photos
    ```
* **Instead of doing:**
    ```shell
    rsync -avySH --delete --backup --backup-dir=../deleted/$timestamp/ "/media/Media/Photos" "user@host.com:/media/backup/filesets/$hostname.photos"
    rsync -avySH --delete --backup --backup-dir=../deleted/$timestamp/ "/media/Media/Books" "user@host.com:/media/backup/filesets/$hostname.books"
    rsync -avySH --delete --backup --backup-dir=../deleted/$timestamp/ "/media/Media/Music" "user@host.com:/media/backup/filesets/$hostname.music"
    ```

    **Just do:**
    ```shell
    autorsync
    ```
Or, in more general terms, instead of doing long rsync commands for your
everyday backups, or putting them in adhoc scripts, write the clear
[`~/autorsync.yaml`](#yamlfile) file and let `autorsync` to the work for you.

## Installation

```shell
pip3 install auto-remote-sync --user
```
(Sorry for the long package name, ideally this would be simply **autorsync**,
but name `autosync` was already taken and PyPi would not allow similar names).

Check [PyPi](https://pypi.org/project/auto-remote-sync/) and
[GitHub](https://github.com/avibrazil/autorsync) for autorsync.

## Usage

### <a name="yamlfile"></a>Organize Profiles in `~/autorsync.yaml`
Here is an example with some defaults and a few profiles:

```yaml
DEFAULTS:
    source_part1: '{{home}}/Media'
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
      extra: --copy-links --no-atimes --itemize-changes
```

**Notes about this configuration**
- All profiles inherit parameters from `DEFAULTS`. If parameter isn’t set in
the profile, the value defined in `DEFAULTS` will be used.
- For each profile, the Source is defined by `source` parameter, or, if not
defined, by `source_part1/source_part2`
- Target follows same logic: `target` or `target_part1/target_part2`
- `delete` makes rsync delete files in target that are absent in source
- `backup` and `backup_dir` makes rsync save backups on target of deleted or
modified files on source. Value on `backup_dir` is a path relative to target
folder
- `extra` lets you add extra rsync switches and can be used in the `DEFAULTS`
section (to affect all profiles) or just into a specific profile.
- You can use Jinja logic in path parts, surrounded by `{{}}`. Currently these
are the available variables:
    - `time`, a Python `datetime.datetime` object which includes local timezone
    - `hostname`, such as “rocket”
    - `Hostname`, such as “rocket.mydomain.com” (FQDN)
    - `username`, UNIX user name as “joanbaez”
    - `home`, user’s home folder as “/home/joanbaez”
    - `userid`, user ID as “504”
    - `gecos`, user long name as “Joan Baez”

### Example usage
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
    autorsync -c /etc/autorsync.yaml -p "books, photos"
    ```
