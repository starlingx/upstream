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

%global sname glanceclient
%global with_doc 0

%global common_desc \
This is a client for the OpenStack Glance API. There's a Python API (the \
glanceclient module), and a command-line script (glance). Each implements \
100% of the OpenStack Glance API.

Name:             python-glanceclient
Epoch:            1
Version:          2.17.0
Release:          1%{?_tis_dist}.%{tis_patch_ver}
Summary:          Python API and CLI for OpenStack Glance

License:          ASL 2.0
URL:              https://launchpad.net/python-glanceclient
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:          Python API and CLI for OpenStack Glance
%{?python_provide:%python_provide python%{pyver}-glanceclient}
%if %{pyver} == 3
Obsoletes: python2-%{sname} < %{version}-%{release}
%endif

BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-wheel

Requires:         python%{pyver}-keystoneauth1 >= 3.6.2
Requires:         python%{pyver}-oslo-i18n >= 3.15.3
Requires:         python%{pyver}-oslo-utils >= 3.33.0
Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-prettytable
Requires:         python%{pyver}-pyOpenSSL >= 17.1.0
Requires:         python%{pyver}-requests
Requires:         python%{pyver}-six >= 1.10.0
# Handle python2 exception
%if %{pyver} == 2
Requires:         python-warlock
Requires:         python-wrapt
%else
Requires:         python%{pyver}-warlock
Requires:         python%{pyver}-wrapt
%endif


%description -n python%{pyver}-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Glance API Client

BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-openstackdocstheme
BuildRequires:    python%{pyver}-keystoneauth1
BuildRequires:    python%{pyver}-oslo-utils
BuildRequires:    python%{pyver}-prettytable
BuildRequires:    python%{pyver}-pyOpenSSL >= 17.1.0
BuildRequires:    python%{pyver}-sphinxcontrib-apidoc
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    python-warlock
%else
BuildRequires:    python%{pyver}-warlock
%endif

%description      doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

%py_req_cleanup

%build
%{pyver_build}
%{pyver_build_wheel}

%install
%{pyver_install}

# STX: stage wheels
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s glance %{buildroot}%{_bindir}/glance-%{pyver}

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/glance.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/glance

# Delete tests
rm -fr %{buildroot}%{pyver_sitelib}/glanceclient/tests

%if 0%{?with_doc}
# generate html docs
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
# generate man page
sphinx-build-%{pyver} -b man doc/source doc/build/man
install -p -D -m 644 doc/build/man/glance.1 %{buildroot}%{_mandir}/man1/glance.1
%endif

%files -n python%{pyver}-%{sname}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/glanceclient
%{pyver_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%if 0%{?with_doc}
%{_mandir}/man1/glance.1.gz
%endif
%{_bindir}/glance
%{_bindir}/glance-%{pyver}

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
* Wed Apr 22 2020 OSP Prod Chain <dev-null@redhat.com> 1:2.17.0-1
- Update patches

* Wed Apr 22 2020 Cyril Roelandt <cyril@redhat.com> 1:2.17.0-0.20200310160931.40c19aa
- Delete image from specific store (rhbz#1758424)
- Pass --all-stores, --allow-failure as bool to API (rhbz#1758416)
- Add support for copy-image import method (rhbz#1758416)
- Add support for multi-store import (rhbz#1758420)

* Tue Mar 10 2020 OSP Prod Chain <dev-null@redhat.com> 1:2.17.0-1
- Update patches

* Tue Feb 25 2020 OSP Prod Chain <dev-null@redhat.com> 1:2.17.0-1
- Cleanup session object (rhbz#1802636)

* Thu Sep 19 2019 OSP Prod Chain <dev-null@redhat.com> 1:2.17.0-1
- Update patches

* Thu Sep 19 2019 RDO <dev@lists.rdoproject.org> 1:2.17.0-1
- Update to 2.17.0

