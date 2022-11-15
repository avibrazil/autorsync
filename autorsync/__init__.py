import copy
import datetime
import yaml
import jinja2
import subprocess


__version__=0.1.5


class RSyncProfile:
    # The barebone defaults
    delete=False
    backup=False
    background=False
    simulate=False

    current_time=datetime.datetime.now()

    as_str_template=(
        "{name}:\n" +
        "   source: {source}\n" +
        "   target: {target}\n" +
        "   command: {command}\n"
    )

    def __init__(self, data):
        for name, value in data.items():
            setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset, dict)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return value

    def get_source(self):
        if hasattr(self,'source'):
            return pathlib.Path(self.source)
        else:
            return pathlib.Path(self.source_part1) / pathlib.Path(self.source_part2)

    def get_target(self):
        if hasattr(self,'target'):
            return pathlib.Path(self.target)
        else:
            return pathlib.Path(self.target_part1) / pathlib.Path(self.target_part2)

    def __str__(self):
        return self.as_str_template.format(
            name=self.name,
            source=self.get_source(),
            target=self.get_target(),
            command=self.make_command()
        )

    def render(self,text):
        datapool=dict(
            time=self.current_time
        )

        return jinja2.Template(text).render(datapool)

    def make_command(self):
        command=[
            'rsync','--fuzzy','--sparse','--human-readable','--hard-links',
            '--perms','--recursive','--times','--atimes','--open-noatime',
            '--devices','--specials','--links','--mkpath','--verbose'
        ]

        if self.simulate:
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

        command.append(self.get_source())
        command.append(self.get_target())

        return command

    def run(self):
        logger.info('Execute sync profile {}'.format(str(self)))
        process = subprocess.run(
            self.make_command(),
            universal_newlines=True,
        )



class RSyncProfiles:
    _profiles=dict()

    def append(self,profile):
        self._profiles[profile.name]=profile

    def __init__(self,config_or_config_file):
        if isinstance(config_or_config_file,str) or isinstance(config_or_config_file,pathlib.Path):
            # Read the YAML file and into a dict
            try:
                with open(config_or_config_file) as f:
                    config=RSyncProfiles(yaml.safe_load(f))
            except FileNotFoundError as e:
                raise FileNotFoundError(f'Auto-rsync needs a YAML file with profiles but {args.config_file} doesn’t exist. Use ‘-c’ to pass a different file.')

        if 'DEFAULTS' in config:
            defaults=config['DEFAULTS']
        else:
            defaults=dict()

        for p in config['profiles']:
            prof=copy.deepcopy(defaults)
            prof.update(p)
            self.append(RSyncProfile(prof))



    @property
    def profiles(self):
        return self._profiles.keys()



    def get(self,name):
        return self._profiles[name]



    def run(self,selected_profiles=None):
        desired_profiles=None

        if isinstance(selected_profiles, str):
            desired_profiles=[x.strip() for x in selected_profiles.split(',')]
        elif isinstance(selected_profiles, list):
            desired_profiles=selected_profiles
        elif args.profiles is None:
            desired_profiles=list(self._profiles.keys())

        for p in desired_profiles:
            if p in self._profiles:
                self._profiles[p].run()
            else:
                logger.warning(f'Can’t find profile “{p}” to execute.')



    def __str__(self):
        profs=""
        for p in self._profiles:
            if len(profs)>0:
                profs+="\n"
            profs+=str(self._profiles[p])

        return profs
