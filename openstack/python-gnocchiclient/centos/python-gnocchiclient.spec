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

%global pypi_name gnocchiclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_doc 1

%global common_desc \
This is a client library for Gnocchi built on the Gnocchi API. It \
provides a Python API (the gnocchiclient module) and a command-line tool.

Name:             python-gnocchiclient
Version:          7.0.4
Release:          1%{?_tis_dist}.%{tis_patch_ver}
Summary:          Python API and CLI for OpenStack Gnocchi

License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://pypi.io/packages/source/g/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:        noarch

%description
%{common_desc}

%package -n python%{pyver}-%{pypi_name}
Summary:          Python API and CLI for OpenStack Gnocchi
%{?python_provide:%python_provide python%{pyver}-gnocchiclient}
%if %{pyver} == 3
Obsoletes: python2-%{pypi_name} < %{version}-%{release}
%endif


BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-tools
BuildRequires:    python%{pyver}-wheel

Requires:         python%{pyver}-cliff >= 2.10
Requires:         python%{pyver}-osc-lib >= 1.8.0
Requires:         python%{pyver}-keystoneauth1 >= 2.0.0
Requires:         python%{pyver}-six >= 1.10.0
Requires:         python%{pyver}-futurist
Requires:         python%{pyver}-ujson
Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-iso8601
Requires:         python%{pyver}-dateutil
Requires:         python%{pyver}-debtcollector
Requires:         python%{pyver}-monotonic

%description -n python%{pyver}-%{pypi_name}
%{common_desc}


%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:          Documentation for OpenStack Gnocchi API Client
Group:            Documentation

BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-cliff >= 2.10
BuildRequires:    python%{pyver}-keystoneauth1
BuildRequires:    python%{pyver}-six
BuildRequires:    python%{pyver}-futurist
BuildRequires:    python%{pyver}-ujson
BuildRequires:    python%{pyver}-sphinx_rtd_theme
# test
BuildRequires:    python%{pyver}-babel
# Runtime requirements needed during documentation build
BuildRequires:    python%{pyver}-osc-lib
BuildRequires:    python%{pyver}-dateutil
BuildRequires:    python%{pyver}-monotonic

%description      doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%package -n python%{pyver}-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Gnocchi Tests
Requires:         python%{pyver}-%{pypi_name} = %{version}-%{release}

%description -n python%{pyver}-%{pypi_name}-tests
%{common_desc}


%prep
%autosetup -n %{pypi_name}-%{upstream_version}

%if %{pyver} == 3
2to3 --write --nobackups .
%endif

# Remove bundled egg-info
rm -rf gnocchiclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
export PBR_VERSION=%{version}
%{pyver_build}
%{pyver_build_wheel}

%if 0%{?with_doc}
# Some env variables required to successfully build our doc
export PYTHONPATH=.
export LANG=en_US.utf8
%{pyver_bin} setup.py build_sphinx -b html

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
export PBR_VERSION=%{version}
%{pyver_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s gnocchi %{buildroot}%{_bindir}/gnocchi-%{pyver}

mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

%files -n python%{pyver}-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/gnocchi
%{_bindir}/gnocchi-%{pyver}
%{pyver_sitelib}/gnocchiclient
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/gnocchiclient/tests

%files -n python%{pyver}-%{pypi_name}-tests
%license LICENSE
%{pyver_sitelib}/gnocchiclient/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%endif

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Thu Sep 19 2019 RDO <dev@lists.rdoproject.org> 7.0.4-1
- Update to 7.0.4

