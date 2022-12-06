# Created by pyp2rpm-3.3.8
%global pypi_name auto-remote-sync
%global pypi_version 1.0.5
%global pkg_name autorsync

Name:           python-%{pkg_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Automate execution of various rsync commands based on profiles defined on a YAML configuration file

License:        None
URL:            https://github.com/avibrazil/autorsync
Source0:        https://files.pythonhosted.org/packages/source/a/%{pypi_name}/auto_remote_sync-%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
Prepare your ~/autorsync.yaml file and do your everyday autorsyncs with short
commands instead of long rsync commands.

%package -n     python3-%{pkg_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkg_name}}

Requires:       python3dist(jinja2)
Requires:       python3dist(pyyaml)
%description -n python3-%{pkg_name}
Prepare your ~/autorsync.yaml file and do your everyday autorsyncs with short
commands instead of long rsync commands.


%prep
%autosetup -n auto_remote_sync-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pkg_name}
%license LICENSE
%doc README.md
%{_bindir}/autorsync
%{python3_sitelib}/autorsync
%{python3_sitelib}/auto_remote_sync-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Tue Dec 06 2022 Avi Alkalay <avibrazil@gmail.com> - 1.0.5-1
- Initial package.
