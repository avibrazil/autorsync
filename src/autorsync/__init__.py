import os
import pwd
import copy
import datetime
import platform
import shlex
import pathlib
import subprocess
import logging
import yaml
import jinja2


__version__="1.1.1"


__all__=['RSyncProfile', 'RSyncProfiles']


class RSyncProfile():
    # The barebone defaults
    delete=False
    backup=False
    background=False
    simulate=False

    # Databpool for Jinja as class variables to be available to all at once
    datapool=dict(
        time            = datetime.datetime.now(
                            tz=(
                                datetime.datetime.now(tz=datetime.timezone.utc)
                                .astimezone()
                                .tzinfo
                            )
        ),
        hostname        = platform.node().split('.',1)[0],
        Hostname        = platform.node(),
        username        = pwd.getpwuid(os.getuid()).pw_name,
        userid          = pwd.getpwuid(os.getuid()).pw_uid,
        gecos           = pwd.getpwuid(os.getuid()).pw_gecos,
        home            = pwd.getpwuid(os.getuid()).pw_dir,
    )

    as_str_template=(
        "{name}:\n" +
        "   source: {source}\n" +
        "   target: {target}\n" +
        "   command: {command}\n"
    )



    def __init__(self, data):
        # Setup logging
        self.logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)

        for name, value in data.items():
            setattr(self, name, self._wrap(value))

        multi_part_params='source target extra'.split()
        parts=[1,2]

        for param in multi_part_params:
            for part in parts:
                working_on=f"{param}_part{part}"
                if not hasattr(self,working_on):
                    setattr(self,working_on,'')



    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset, dict)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return value



    def get_source(self):
        """Process the 'source' and 'source_part1'+'source_part2' profile
        parameters"""

        # Can't use pathlib here because it strips down trailing slashes that
        # are soooo important to rsync
        if hasattr(self,'source'):
            path = self.source
        else:
            path = self.source_part1 + os.sep + self.source_part2

        # Resolve Jinja tags
        return self.render(path)



    def get_target(self):
        """Process the 'target' and 'target_part1'+'target_part2' profile
        parameters"""

        # Can't use pathlib here because it strips down trailing slashes that are soooo
        # important to rsync
        if hasattr(self,'target'):
            path = self.target
        else:
            path = self.target_part1 + os.sep + self.target_part2

        # Resolve Jinja tags
        return self.render(path)



    def get_extra(self):
        """Process the 'extra' and 'extra_part1'+'extra_part2' profile
        parameters"""

        # Can't use pathlib here because it strips down trailing slashes that are soooo
        # important to rsync
        if hasattr(self,'extra'):
            params = self.extra
        else:
            params = self.extra_part1 + ' ' + self.extra_part2

        # Resolve Jinja tags and split parameters in the Shell style
        return [p.strip() for p in shlex.split(self.render(params))]



    def __str__(self):
        return self.as_str_template.format(
            name=self.name,
            source=self.get_source(),
            target=self.get_target(),
            command=self.make_command()
        )



    def render(self,text):
        return jinja2.Template(text).render(self.datapool)



    def make_command(self,simulate=False):
        command=[
            'rsync',

            # The "rsync -a" suite in a verbose way:
            '--recursive',      '--links',   '--perms',    '--times',
            '--owner',          '--group',   '--devices',  '--specials',

            # More useful parameters
            '--human-readable', '--fuzzy',   '--sparse',   '--hard-links',
            '--executability',  '--atimes',  '--acls',     '--xattrs',
            '--open-noatime',   '--mkpath',  '--verbose',  '--compress',
            '--skip-compress=7z/apk/avi/bz2/cab/deb/dmg/gz/flac/heif/heic/jar/jpg/JPG/jpeg/JPEG/m4a/m4v/mkv/mov/mp3/mp4/mpeg/mpg/mpv/oga/ogg/ogv/opus/pack/png/qt/rar/rpm/sfx/svgz/tgz/tlz/txz/vob/webm/webp/wma/wmv/xz/z/zip'
        ]

        if self.simulate or simulate:
            command.append("--dry-run")

        if self.delete:
            command.append("--delete")

        if self.backup:
            if hasattr(self,'backup_dir'):
                command+=[
                    "--backup",
                    "--backup-dir={}".format(
                        self.render(self.backup_dir)
                    )
                ]
            else:
                raise NameError("undefined backup_dir")

        command+=self.get_extra()
        command.append(self.get_source())
        command.append(self.get_target())

        return command



    def run(self, simulate=False):
        self.logger.info('Execute sync profile {}'.format(str(self)))

        command_items=self.make_command(simulate=simulate)

        self.logger.debug('Command: ' + ' '.join([str(x) for x in command_items]))
        process = subprocess.run(
            command_items,
            universal_newlines=True,
        )



class RSyncProfiles():
    _profiles=dict()



    def append(self,profile):
        self._profiles[profile.name]=profile



    def __init__(self,config_or_config_file):
        # Setup logging
        self.logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)

        if isinstance(config_or_config_file,str) or isinstance(config_or_config_file,pathlib.Path):
            # Read the YAML file and into a dict
            self.logger.debug(f'Using configurations from «{config_or_config_file}»')
            try:
                with open(config_or_config_file) as f:
                    config=yaml.safe_load(f)
            except FileNotFoundError as e:
                msg=(
                    'Auto-rsync needs a YAML file with profiles but ' +
                    '«{}» doesn’t exist. Use ‘-c’ to pass a different file.'
                )
                raise FileNotFoundError(msg.format(config_or_config_file))

        if 'DEFAULTS' in config:
            defaults=config['DEFAULTS']
        else:
            defaults=dict()

        for p in config['profiles']:
            config=copy.deepcopy(defaults)
            config.update(p)
            self._profiles[p['name']]=RSyncProfile(config)



    @property
    def profiles(self):
        return self._profiles.keys()



    def get(self,name):
        return self._profiles[name]



    def run(self, selected_profiles=None, simulate=False):
        desired_profiles=None

        if isinstance(selected_profiles, str):
            desired_profiles=[x.strip() for x in selected_profiles.split(',')]
        elif isinstance(selected_profiles, list):
            desired_profiles=selected_profiles
        elif selected_profiles is None:
            desired_profiles=list(self._profiles.keys())

        for p in desired_profiles:
            if p in self._profiles:
                self._profiles[p].run(simulate=simulate)
            else:
                self.logger.warning(f'Can’t find profile “{p}” to execute.')



    def __str__(self):
        profs=""
        for p in self._profiles:
            if len(profs)>0:
                profs+="\n"
            profs+=str(self._profiles[p])

        return profs
