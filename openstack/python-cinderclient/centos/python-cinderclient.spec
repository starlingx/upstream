# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
%global pyver_build_wheel %{expand:%{py%{pyver}_build_wheel}}
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname cinderclient

%global with_doc 1

%global common_desc \
Client library (cinderclient python module) and command line utility \
(cinder) for interacting with OpenStack Cinder (Block Storage) API.

Name:             python-cinderclient
Version:          5.0.0
Release:          1%{?_tis_dist}.%{tis_patch_ver}
Summary:          Python API and CLI for OpenStack Cinder

License:          ASL 2.0
URL:              http://github.com/openstack/python-cinderclient
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    git

%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:          Python API and CLI for OpenStack Cinder
%{?python_provide:%python_provide python%{pyver}-%{sname}}

BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-wheel

Requires:         python%{pyver}-babel
Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-prettytable
Requires:         python%{pyver}-requests
Requires:         python%{pyver}-six
Requires:         python%{pyver}-keystoneauth1 >= 3.4.0
Requires:         python%{pyver}-oslo-i18n >= 3.15.3
Requires:         python%{pyver}-oslo-utils >= 3.33.0
Requires:         python%{pyver}-simplejson

%description -n python%{pyver}-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Cinder API Client
Group:            Documentation

BuildRequires:    python%{pyver}-reno
BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-openstackdocstheme

%description      doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf python_cinderclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%{pyver_build}
%{pyver_build_wheel}

%if 0%{?with_doc}
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
sphinx-build-%{pyver} -W -b man doc/source doc/build/man

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%{pyver_install}
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s cinder %{buildroot}%{_bindir}/cinder-%{pyver}

mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# Delete tests
rm -fr %{buildroot}%{pyver_sitelib}/cinderclient/tests

install -p -D -m 644 tools/cinder.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/cinder.bash_completion

%if 0%{?with_doc}
install -p -D -m 644 doc/build/man/cinder.1 %{buildroot}%{_mandir}/man1/cinder.1
%endif

%files -n python%{pyver}-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/cinder
%{_bindir}/cinder-%{pyver}
%{pyver_sitelib}/cinderclient
%{pyver_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d/cinder.bash_completion
%if 0%{?with_doc}
%{_mandir}/man1/cinder.1*
%endif

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Thu Sep 19 2019 RDO <dev@lists.rdoproject.org> 5.0.0-1
- Update to 5.0.0

