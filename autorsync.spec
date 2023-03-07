Name:      autorsync
Version:   1.0.6
Release:   1%{?dist}
Summary:   Automate execution of various rsync commands

License:   LGPL
URL:       https://github.com/avibrazil/autorsync
Source0:   %{pypi_source auto_remote_sync}

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3dist(jinja2)
BuildRequires: python3dist(pyyaml)

%description
Command to automate execution of various rsync commands based on profiles
defined on a YAML configuration file.

%prep
%autosetup -n auto_remote_sync-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files autorsync


%check
%pyproject_check_import


%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/autorsync


%changelog
* Mon Mar  6 2023 Avi Alkalay <avi@unix.sh> - 1.0.6-1
- Upstream update
* Tue Dec  6 2022 Jonny Heggheim <hegjon@gmail.com> - 1.0.5-1
- Inital packaging
