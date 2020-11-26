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
%global with_doc 1

%global cname neutron
%global sname %{cname}client

%global common_desc \
Client library and command line utility for interacting with OpenStack \
Neutron's API.

Name:       python-neutronclient
Version:    6.14.0
Release:    1%{?_tis_dist}.%{tis_patch_ver}
Summary:    Python API and CLI for OpenStack Neutron

License:    ASL 2.0
URL:        http://launchpad.net/%{name}/
Source0:    https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:  noarch

Obsoletes:  python-%{sname}-tests <= 4.1.1-3

%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:    Python API and CLI for OpenStack Neutron
%{?python_provide:%python_provide python%{pyver}-%{sname}}
%if %{pyver} == 3
Obsoletes: python2-%{sname} < %{version}-%{release}
%endif

BuildRequires: git
BuildRequires: openstack-macros
BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-pbr
BuildRequires: python%{pyver}-wheel
# Required for unit tests
BuildRequires: python%{pyver}-osc-lib-tests
BuildRequires: python%{pyver}-oslotest
BuildRequires: python%{pyver}-testtools
BuildRequires: python%{pyver}-testrepository
BuildRequires: python%{pyver}-testscenarios
BuildRequires: python%{pyver}-keystoneauth1
BuildRequires: python%{pyver}-keystoneclient
BuildRequires: python%{pyver}-os-client-config
BuildRequires: python%{pyver}-osc-lib
BuildRequires: python%{pyver}-oslo-log
BuildRequires: python%{pyver}-oslo-serialization
BuildRequires: python%{pyver}-oslo-utils
BuildRequires: python%{pyver}-cliff

Requires: python%{pyver}-babel >= 2.3.4
Requires: python%{pyver}-iso8601 >= 0.1.11
Requires: python%{pyver}-os-client-config >= 1.28.0
Requires: python%{pyver}-oslo-i18n >= 3.15.3
Requires: python%{pyver}-oslo-log >= 3.36.0
Requires: python%{pyver}-oslo-serialization >= 2.18.0
Requires: python%{pyver}-oslo-utils >= 3.33.0
Requires: python%{pyver}-pbr
Requires: python%{pyver}-requests >= 2.14.2
Requires: python%{pyver}-six >= 1.10.0
Requires: python%{pyver}-debtcollector >= 1.2.0
Requires: python%{pyver}-osc-lib >= 1.10.0
Requires: python%{pyver}-keystoneauth1 >= 3.4.0
Requires: python%{pyver}-keystoneclient >= 1:3.8.0
Requires: python%{pyver}-cliff >= 2.8.0
Requires: python%{pyver}-netaddr >= 0.7.18

# Handle python2 exception
%if %{pyver} == 2
Requires: python-simplejson >= 3.5.1
%else
Requires: python%{pyver}-simplejson >= 3.5.1
%endif

%description -n python%{pyver}-%{sname}
%{common_desc}

%package -n python%{pyver}-%{sname}-tests
Summary:    Python API and CLI for OpenStack Neutron - Unit tests
%{?python_provide:%python_provide python%{pyver}-%{sname}-tests}
Requires: python%{pyver}-%{sname} == %{version}-%{release}
Requires: python%{pyver}-osc-lib-tests
Requires: python%{pyver}-oslotest
Requires: python%{pyver}-testtools
Requires: python%{pyver}-testrepository
Requires: python%{pyver}-testscenarios

%description -n python%{pyver}-%{sname}-tests
%{common_desc}

This package containts the unit tests.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Neutron API Client

BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-openstackdocstheme
BuildRequires:    python%{pyver}-reno

%description      doc
%{common_desc}
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%{pyver_build}
%{pyver_build_wheel}

%if 0%{?with_doc}
# Build HTML docs
export PYTHONPATH=.
sphinx-build-%{pyver} -W -b html doc/source doc/build/html

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%{pyver_install}

# STX: stage wheels
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{cname} %{buildroot}%{_bindir}/%{cname}-%{pyver}

%check
# (TODO) Ignore unit tests results until https://bugs.launchpad.net/python-neutronclient/+bug/1783789
# is fixed.
%{pyver_bin} setup.py testr || true

%files -n python%{pyver}-%{sname}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/%{sname}
%{pyver_sitelib}/*.egg-info
%{_bindir}/%{cname}
%{_bindir}/%{cname}-%{pyver}
%exclude %{pyver_sitelib}/%{sname}/tests

%files -n python%{pyver}-%{sname}-tests
%{pyver_sitelib}/%{sname}/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Thu Sep 19 2019 RDO <dev@lists.rdoproject.org> 6.14.0-1
- Update to 6.14.0

