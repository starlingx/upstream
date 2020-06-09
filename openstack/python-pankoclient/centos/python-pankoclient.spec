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
%global pypi_name pankoclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

Name:             python-pankoclient
Version:          0.7.0
Release:          1%{?_tis_dist}.%{tis_patch_ver}
Summary:          Python API and CLI for OpenStack Panko

License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:        noarch


%package -n python%{pyver}-%{pypi_name}
Summary:          Python API and CLI for OpenStack Panko
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}
%if %{pyver} == 3
Obsoletes: python2-%{pypi_name} < %{version}-%{release}
%endif


BuildRequires:    git
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-tools
BuildRequires:    python%{pyver}-wheel

Requires:         python%{pyver}-keystoneauth1 >= 3.4.0
Requires:         python%{pyver}-osc-lib >= 1.8.0
Requires:         python%{pyver}-oslo-i18n >= 2.1.0
Requires:         python%{pyver}-oslo-serialization >= 1.10.0
Requires:         python%{pyver}-oslo-utils >= 3.18.0
Requires:         python%{pyver}-osprofiler >= 1.4.0
Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-requests
Requires:         python%{pyver}-six >= 1.9.0


%description -n python%{pyver}-%{pypi_name}
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool.

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:          Documentation for OpenStack Panko API Client
Group:            Documentation

BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-openstackdocstheme
BuildRequires:    python%{pyver}-osc-lib
# test
BuildRequires:    python%{pyver}-babel

%description      doc
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool
(panko).

This package contains auto-generated documentation.
%endif

%package -n python%{pyver}-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Panko Tests
Requires:         python%{pyver}-%{pypi_name} = %{version}-%{release}

%description -n python%{pyver}-%{pypi_name}-tests
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool.

%description
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool.


%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf pankoclient.egg-info

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
ln -s panko %{buildroot}%{_bindir}/panko-%{pyver}

%if 0%{?with_doc}
# Some env variables required to successfully build our doc
export PATH=$PATH:%{buildroot}%{_bindir}
export LANG=en_US.utf8
%{pyver_bin} setup.py build_sphinx -b html

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%files -n python%{pyver}-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/panko
%{_bindir}/panko-%{pyver}
# XXX: man page build is broken
#%{_mandir}/man1/panko.1*
%{pyver_sitelib}/pankoclient
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/pankoclient/tests

%files -n python%{pyver}-%{pypi_name}-tests
%license LICENSE
%{pyver_sitelib}/pankoclient/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
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
* Thu Oct 10 2019 RDO <dev@lists.rdoproject.org> 0.7.0-1
- Update to 0.7.0


