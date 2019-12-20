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
%global pypi_name keystoneauth1

%global common_desc \
Keystoneauth provides a standard way to do authentication and service requests \
within the OpenStack ecosystem. It is designed for use in conjunction with \
the existing OpenStack clients and for simplifying the process of writing \
new clients.

%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-%{pypi_name}
Version:    3.17.1
Release:    2%{?_tis_dist}.%{tis_patch_ver}
Summary:    Authentication Library for OpenStack Clients
License:    ASL 2.0
URL:        https://pypi.io/pypi/%{pypi_name}
Source0:    https://tarballs.openstack.org/keystoneauth/keystoneauth1-%{upstream_version}.tar.gz

BuildArch:  noarch

%description
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}
Summary:        Authentication Libarary for OpenStack Identity
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}
%{?python_provide:%python_provide python%{pyver}-keystoneauth}

BuildRequires: git
BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-six
BuildRequires: python%{pyver}-pbr >= 2.0.0

# test requires
#BuildRequires: python%{pyver}-betamax >= 0.7.0
BuildRequires: python-betamax >= 0.7.0
BuildRequires: python%{pyver}-fixtures >= 1.3.1
BuildRequires: python%{pyver}-mock
BuildRequires: python%{pyver}-oslotest
BuildRequires: python%{pyver}-oslo-config
BuildRequires: python%{pyver}-oslo-utils
BuildRequires: python%{pyver}-stestr
BuildRequires: python%{pyver}-oauthlib
BuildRequires: python%{pyver}-requests
BuildRequires: python%{pyver}-os-service-types
BuildRequires: python%{pyver}-stevedore
BuildRequires: python%{pyver}-iso8601
BuildRequires: python%{pyver}-requests-mock >= 1.1

# Handle python2 exception
%if %{pyver} == 2
BuildRequires: PyYAML
BuildRequires: python-lxml
BuildRequires: python-requests-kerberos
BuildRequires: python-pep8
%else
BuildRequires: python%{pyver}-PyYAML
BuildRequires: python%{pyver}-lxml
BuildRequires: python%{pyver}-requests-kerberos
BuildRequires: python%{pyver}-pep8
%endif

Requires:      python%{pyver}-iso8601 >= 0.1.11
Requires:      python%{pyver}-os-service-types >= 1.2.0
Requires:      python%{pyver}-pbr >= 2.0.0
Requires:      python%{pyver}-requests >= 2.14.2
Requires:      python%{pyver}-six => 1.10.0
Requires:      python%{pyver}-stevedore >= 1.20.0

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:    Documentation for OpenStack Identity Authentication Library

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-sphinxcontrib-apidoc
BuildRequires: python%{pyver}-openstackdocstheme
BuildRequires: python%{pyver}-mox3

%description -n python-%{pypi_name}-doc
Documentation for OpenStack Identity Authentication Library
%endif


%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

sed -i '/sphinx.ext.intersphinx.*$/d'  doc/source/conf.py

# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{pyver_build}

%install
%{pyver_install}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
# Disabling warning-is-error because of issue with python2 giving a warning:
# "The config value `apidoc_module_dir' has type `unicode', expected to ['str']."
sphinx-build-%{pyver} -b html -d doc/build/doctrees doc/source doc/build/html
rm -rf doc/build/html/.buildinfo
%endif

%check
PYTHON=python%{pyver} stestr-%{pyver} run

%files -n python%{pyver}-%{pypi_name}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Thu Oct 03 2019 Joel Capitao <jcapitao@redhat.com> 3.17.1-2
- Removed python2 subpackages in no el7 distros

* Wed Sep 18 2019 RDO <dev@lists.rdoproject.org> 3.17.1-1
- Update to 3.17.1

