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
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Client library and command line utility for interacting with Openstack \
Identity API.

%global sname keystoneclient
%global with_doc 1

Name:       python-keystoneclient
Epoch:      1
Version:    3.21.0
Release:    2%{?_tis_dist}.%{tis_patch_ver}
Summary:    Client library for OpenStack Identity API
License:    ASL 2.0
URL:        https://launchpad.net/python-keystoneclient
Source0:    https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires: /usr/bin/openssl


%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:    Client library for OpenStack Identity API
%{?python_provide:%python_provide python%{pyver}-%{sname}}
%if %{pyver} == 3
Obsoletes: python2-%{sname} < %{version}-%{release}
%endif

BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-pbr >= 2.0.0
BuildRequires: git

Requires: python%{pyver}-oslo-config >= 2:5.2.0
Requires: python%{pyver}-oslo-i18n >= 3.15.3
Requires: python%{pyver}-oslo-serialization >= 2.18.0
Requires: python%{pyver}-oslo-utils >= 3.33.0
Requires: python%{pyver}-requests >= 2.14.2
Requires: python%{pyver}-six >= 1.10.0
Requires: python%{pyver}-stevedore >= 1.20.0
Requires: python%{pyver}-pbr >= 2.0.0
Requires: python%{pyver}-debtcollector >= 1.2.0
Requires: python%{pyver}-keystoneauth1 >= 3.4.0
# Handle python2 exception
%if %{pyver} == 2
Requires: python-keyring >= 5.5.1
%else
Requires: python%{pyver}-keyring >= 5.5.1
%endif

%description -n python%{pyver}-%{sname}
%{common_desc}

%package -n python%{pyver}-%{sname}-tests
Summary:  Python API and CLI for OpenStack Keystone (tests)
%{?python_provide:%python_provide python%{pyver}-%{sname}-tests}
Requires:  python%{pyver}-%{sname} = %{epoch}:%{version}-%{release}

BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oauthlib
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  python%{pyver}-oslo-serialization
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-testresources
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-requests-mock
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-keyring >= 5.5.1
BuildRequires:  python-lxml
%else
BuildRequires:  python%{pyver}-keyring >= 5.5.1
BuildRequires:  python%{pyver}-lxml
%endif

Requires:  python%{pyver}-hacking
Requires:  python%{pyver}-fixtures
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-oauthlib
Requires:  python%{pyver}-oslotest
Requires:  python%{pyver}-stestr
Requires:  python%{pyver}-testtools
Requires:  python%{pyver}-testresources
Requires:  python%{pyver}-testscenarios
Requires:  python%{pyver}-requests-mock
# Handle python2 exception
%if %{pyver} == 2
Requires:  python-lxml
%else
Requires:  python%{pyver}-lxml
%endif

%description -n python%{pyver}-%{sname}-tests
{common_desc}

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: Documentation for OpenStack Keystone API client

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description -n python-%{sname}-doc
{common_desc}
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# disable warning-is-error, this project has intersphinx in docs
# so some warnings are generated in network isolated build environment
# as koji
sed -i 's/^warning-is-error.*/warning-is-error = 0/g' setup.cfg

# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt

%build
%{pyver_build}

%install
%{pyver_install}

%if 0%{?with_doc}
# Build HTML docs
%{pyver_bin} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
%endif

#%check
#stestr --test-path=./keystoneclient/tests/unit run
#%if 0%{?with_python3}
#stestr-3 --test-path=./keystoneclient/tests/unit run
#%endif

%files -n python%{pyver}-%{sname}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{sname}
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/%{sname}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python%{pyver}-%{sname}-tests
%license LICENSE
%{pyver_sitelib}/%{sname}/tests

%changelog
* Thu Oct 03 2019 Joel Capitao <jcapitao@redhat.com> 1:3.21.0-2
- Removed python2 subpackages in no el7 distros

* Thu Sep 19 2019 RDO <dev@lists.rdoproject.org> 1:3.21.0-1
- Update to 3.21.0

