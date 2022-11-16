Name:           autorsync
Version:        1.0.1
Release:        %autorelease
Summary:        Automate execution of various rsync commands based on profiles defined on a YAML configuration file

License:        GPL
URL:            https://github.com/avibrazil/autorsync
Source0:        https://github.com/avibrazil/autorsync/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Avoids the need to run autogen.sh during setup (which requires the complete
# git repository). Recreate by running './autogen.sh' in a local git checkout
Patch0:         %{name}.autogen.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  %{py3_dist jinja2}
BuildRequires:  %{py3_dist pyyaml}

%description
Command to automate execution of various rsync commands based on profiles defined on a YAML configuration file.

%prep
%autosetup -p1 -n %{name}-%{version}


%build
%py3_build


%install
%py3_install


%files
%license LICENSE
%doc README.md
%{python3_sitelib}/*
%{_bindir}/autorsync


%changelog
%autochangelog
