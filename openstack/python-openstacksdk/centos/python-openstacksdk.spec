# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
%global pyver_build_wheel %{expand:%{py%{pyver}_build_wheel}}
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Disable docs until bs4 package is available
%global with_doc 0

# STX: Disable unit tests as part of build
%global do_check 0

%global pypi_name openstacksdk

%global common_desc \
A collection of libraries for building applications to work with OpenStack \
clouds.

%global common_desc_tests \
A collection of libraries for building applications to work with OpenStack \
clouds - test files

Name:           python-%{pypi_name}
Version:        0.36.0
Release:        1%{?_tis_dist}.%{tis_patch_ver}
Summary:        An SDK for building applications to work with OpenStack

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://pypi.io/packages/source/o/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git

%description
%{common_desc}

%package -n python%{pyver}-%{pypi_name}
Summary:        An SDK for building applications to work with OpenStack
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr >= 2.0.0
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-appdirs
BuildRequires:  python%{pyver}-requestsexceptions
BuildRequires:  python%{pyver}-munch
BuildRequires:  python%{pyver}-jmespath
BuildRequires:  python%{pyver}-jsonschema
BuildRequires:  python%{pyver}-os-service-types
BuildRequires:  python%{pyver}-wheel
# Test requirements
BuildRequires:  python%{pyver}-iso8601 >= 0.1.11
BuildRequires:  python%{pyver}-jsonpatch >= 1.16
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-requests-mock
BuildRequires:  python%{pyver}-dogpile-cache
BuildRequires:  python%{pyver}-ddt
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-decorator
BuildRequires:  python-ipaddress
BuildRequires:  python-netifaces
BuildRequires:  python-futures
%else
BuildRequires:  python%{pyver}-decorator
BuildRequires:  python%{pyver}-netifaces
%endif

Requires:       python%{pyver}-cryptography >= 2.1
Requires:       python%{pyver}-jsonpatch >= 1.16
Requires:       python%{pyver}-keystoneauth1 >= 3.16.0
Requires:       python%{pyver}-six
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-appdirs
Requires:       python%{pyver}-requestsexceptions >= 1.2.0
Requires:       python%{pyver}-munch
Requires:       python%{pyver}-jmespath
Requires:       python%{pyver}-iso8601
Requires:       python%{pyver}-os-service-types >= 1.7.0
Requires:       python%{pyver}-dogpile-cache
# Handle python2 exception
%if %{pyver} == 2
Requires:       python-decorator
Requires:       python-ipaddress
Requires:       python-netifaces
Requires:       python-futures
Requires:       PyYAML
%else
Requires:       python%{pyver}-decorator
Requires:       python%{pyver}-netifaces
Requires:       python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%package -n python%{pyver}-%{pypi_name}-tests
Summary:        An SDK for building applications to work with OpenStack - test files

Requires: python%{pyver}-%{pypi_name} = %{version}-%{release}

%description -n python%{pyver}-%{pypi_name}-tests
%{common_desc_tests}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        An SDK for building applications to work with OpenStack - documentation
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinx

%description -n python-%{pypi_name}-doc
A collection of libraries for building applications to work with OpenStack
clouds - documentation.
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the requirements
rm -rf {,test-}requirements.txt
# This unit test requires python-prometheus, which is optional and not needed
rm -f openstack/tests/unit/test_stats.py

%build
%{pyver_build}
%{pyver_build_wheel}

%if 0%{?with_doc}
# generate html docs
sphinx-build-%{pyver} -b html doc/source html
# remove the sphinx-build-%{pyver} leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# STX: stage wheels
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

%check
export OS_STDOUT_CAPTURE=true
export OS_STDERR_CAPTURE=true
export OS_TEST_TIMEOUT=20
# FIXME(jpena) we are skipping some unit tests due to
# https://storyboard.openstack.org/#!/story/2005677
PYTHON=python%{pyver} stestr-%{pyver} --test-path ./openstack/tests/unit run --black-regex 'test_wait_for_task_'

%files -n python%{pyver}-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/openstack-inventory
%{pyver_sitelib}/openstack
%{pyver_sitelib}/%{pypi_name}-*.egg-info
%exclude %{pyver_sitelib}/openstack/tests

%files -n python%{pyver}-%{pypi_name}-tests
%{pyver_sitelib}/openstack/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE
%endif

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Fri Oct 04 2019 OSP Prod Chain <dev-null@redhat.com> 0.36.0-2
- Update patches

* Wed Oct 02 2019 Joel Capitao <jcapitao@redhat.com> 0.36.0-2
- Removed python2 subpackages in no el7 distros

* Thu Sep 19 2019 RDO <dev@lists.rdoproject.org> 0.36.0-1
- Update to 0.36.0

