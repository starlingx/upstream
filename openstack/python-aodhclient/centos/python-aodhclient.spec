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
%global pypi_name aodhclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global common_desc \
This is a client library for Aodh built on the Aodh API. It \
provides a Python API (the aodhclient module) and a command-line tool.

Name:             python-aodhclient
Version:          1.3.0
Release:          1%{?_tis_dist}.%{tis_patch_ver}
Summary:          Python API and CLI for OpenStack Aodh

License:          ASL 2.0
URL:              https://launchpad.net/python-aodhclient
Source0:          https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:        noarch

%description
%{common_desc}

%package -n python%{pyver}-%{pypi_name}
Summary:          Python API and CLI for OpenStack Aodh
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-wheel
BuildRequires:    git

Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-cliff >= 1.14.0
Requires:         python%{pyver}-oslo-i18n >= 1.5.0
Requires:         python%{pyver}-oslo-serialization >= 1.4.0
Requires:         python%{pyver}-oslo-utils >= 2.0.0
Requires:         python%{pyver}-osprofiler >= 1.4.0
Requires:         python%{pyver}-keystoneauth1 >= 1.0.0
Requires:         python%{pyver}-six >= 1.9.0
Requires:         python%{pyver}-osc-lib >= 1.0.1
# Handle python2 exception
%if %{pyver} == 2
Requires:         pyparsing
%else
Requires:         python%{pyver}-pyparsing
%endif

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package  doc
Summary:          Documentation for OpenStack Aodh API Client

BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-openstackdocstheme
BuildRequires:    python%{pyver}-keystoneauth1
BuildRequires:    python%{pyver}-oslo-utils
BuildRequires:    python%{pyver}-oslo-serialization
BuildRequires:    python%{pyver}-cliff


%description doc
%{common_desc}
(aodh).

This package contains auto-generated documentation.
%endif

%package -n python%{pyver}-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Aodh Tests
Requires:         python%{pyver}-%{pypi_name} = %{version}-%{release}

%description -n python%{pyver}-%{pypi_name}-tests
%{common_desc}

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the requirements
rm -f {,test-}requirements.txt


%build
%{pyver_build}
%{pyver_build_wheel}

%install
%{pyver_install}

# STX: stage wheels
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s aodh %{buildroot}%{_bindir}/aodh-%{pyver}

%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%files -n python%{pyver}-%{pypi_name}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/aodhclient
%{pyver_sitelib}/*.egg-info
%{_bindir}/aodh
%{_bindir}/aodh-%{pyver}
%exclude %{pyver_sitelib}/aodhclient/tests

%files -n python%{pyver}-%{pypi_name}-tests
%license LICENSE
%{pyver_sitelib}/aodhclient/tests

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
* Mon Sep 23 2019 RDO <dev@lists.rdoproject.org> 1.3.0-1
- Update to 1.3.0

