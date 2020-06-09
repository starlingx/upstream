# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%global __python %{__python3}
%else
%global pyver 2
%global __python %{__python2}
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
%global pyver_build_wheel %{expand:%{py%{pyver}_build_wheel}}
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Command name
%global cname openstack

# library name
%global sname %{cname}client

%global with_doc 1

%global common_desc \
python-%{sname} is a unified command-line client for the OpenStack APIs. \
It is a thin wrapper to the stock python-*client modules that implement the \
actual REST API client actions.

Name:             python-%{sname}
Version:          4.0.0
Release:          1%{?_tis_dist}.%{tis_patch_ver}
Summary:          OpenStack Command-line Client

License:          ASL 2.0
URL:              http://launchpad.net/%{name}
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:    OpenStack Command-line Client
%{?python_provide:%python_provide python%{pyver}-%{sname}}
%if %{pyver} == 3
Obsoletes: python2-%{sname} < %{version}-%{release}
%endif

BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-six
BuildRequires:    python%{pyver}-oslo-i18n
BuildRequires:    python%{pyver}-oslo-utils
BuildRequires:    python%{pyver}-requests
BuildRequires:    python%{pyver}-glanceclient
BuildRequires:    python%{pyver}-keystoneclient
BuildRequires:    python%{pyver}-novaclient
BuildRequires:    python%{pyver}-cinderclient
BuildRequires:    python%{pyver}-mock
BuildRequires:    python%{pyver}-os-client-config
BuildRequires:    python%{pyver}-cliff
BuildRequires:    python%{pyver}-simplejson
BuildRequires:    python%{pyver}-wheel
%if %{pyver} == 2
BuildRequires:    python-requests-mock
%else
BuildRequires:    python%{pyver}-requests-mock
%endif

# Required to compile translation files
BuildRequires:    python%{pyver}-babel
# Required for unit tests
BuildRequires:    python%{pyver}-stestr
BuildRequires:    python%{pyver}-osc-lib-tests
BuildRequires:    python%{pyver}-fixtures
BuildRequires:    python%{pyver}-oslotest
BuildRequires:    python%{pyver}-reno
BuildRequires:    python%{pyver}-requestsexceptions
BuildRequires:    python%{pyver}-openstacksdk
BuildRequires:    python%{pyver}-osprofiler

Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-babel
Requires:         python%{pyver}-openstacksdk >= 0.17.0
Requires:         python%{pyver}-oslo-i18n >= 3.15.3
Requires:         python%{pyver}-oslo-utils >= 3.33.0
Requires:         python%{pyver}-glanceclient >= 1:2.8.0
Requires:         python%{pyver}-keystoneauth1 >= 3.6.2
Requires:         python%{pyver}-keystoneclient >= 1:3.17.0
Requires:         python%{pyver}-novaclient >= 1:15.0.0
Requires:         python%{pyver}-cinderclient >= 3.3.0
Requires:         python%{pyver}-neutronclient >= 6.7.0
Requires:         python%{pyver}-six >= 1.10.0
Requires:         python%{pyver}-osc-lib >= 1.14.0
Requires:         python%{pyver}-cliff

Requires:         python-%{sname}-lang = %{version}-%{release}


%description -n python%{pyver}-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary:          Documentation for OpenStack Command-line Client

BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-openstackdocstheme
BuildRequires:    python%{pyver}-sphinxcontrib-apidoc

Requires: python%{pyver}-%{sname} = %{version}-%{release}

%description -n python-%{sname}-doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%package  -n python-%{sname}-lang
Summary:   Translation files for Openstackclient

%description -n python-%{sname}-lang
Translation files for Openstackclient

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# We handle requirements ourselves, pkg_resources only bring pain
%py_req_cleanup

%build
%{pyver_build}
%{pyver_build_wheel}

# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/%{sname}/locale

%install
%{pyver_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{cname} %{buildroot}%{_bindir}/%{cname}-%{pyver}

%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build-%{pyver} -b html doc/source doc/build/html
sphinx-build-%{pyver} -b man doc/source doc/build/man
install -p -D -m 644 doc/build/man/%{cname}.1 %{buildroot}%{_mandir}/man1/%{cname}.1

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo doc/build/html/.htaccess
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/%{sname}/locale/*/LC_*/%{sname}*po
rm -f %{buildroot}%{pyver_sitelib}/%{sname}/locale/*pot
mv %{buildroot}%{pyver_sitelib}/%{sname}/locale %{buildroot}%{_datadir}/locale
rm -rf %{buildroot}%{pyver_sitelib}/%{sname}/locale

# Find language files
%find_lang %{sname} --all-name

# STX: stage wheels
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

%check
export PYTHON=%{__python}
stestr-%{pyver} run

%files -n python%{pyver}-%{sname}
%license LICENSE
%doc README.rst
%{_bindir}/%{cname}
%{_bindir}/%{cname}-%{pyver}
%{pyver_sitelib}/%{sname}
%{pyver_sitelib}/*.egg-info
%if 0%{?with_doc}
%{_mandir}/man1/%{cname}.1*

%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python-%{sname}-lang -f %{sname}.lang
%license LICENSE

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Mon Sep 23 2019 RDO <dev@lists.rdoproject.org> 4.0.0-1
- Update to 4.0.0

