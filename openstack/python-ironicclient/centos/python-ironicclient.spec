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

%global sname ironicclient

%global common_desc A python and command line client library for Ironic

Name:           python-ironicclient
Version:        3.1.0
Release:        1%{?_tis_dist}.%{tis_patch_ver}
Summary:        Python client for Ironic

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/python-%{sname}
Source0:        https://tarballs.openstack.org/python-%{sname}/python-%{sname}-%{version}%{?milestone}.tar.gz
BuildArch:      noarch


%description
%{common_desc}


%package -n python%{pyver}-%{sname}
Summary:        Python client for Ironic
%{?python_provide:%python_provide python%{pyver}-%{sname}}
%if %{pyver} == 3
Obsoletes: python2-%{sname} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr >= 2.0.0
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-wheel

Requires:       genisoimage
Requires:       python%{pyver}-appdirs >= 1.3.0
Requires:       python%{pyver}-keystoneauth1 >= 3.4.0
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-osc-lib >= 1.10.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-requests
# Handle python2 exception
%if %{pyver} == 2
Requires:       python-dogpile-cache >= 0.6.2
Requires:       python-jsonschema
Requires:       PyYAML
%else
Requires:       python%{pyver}-dogpile-cache >= 0.6.2
Requires:       python%{pyver}-jsonschema
Requires:       python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{sname}
%{common_desc}

%prep
%setup -q -n %{name}-%{upstream_version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
export PBR_VERSION=%{version}
%{pyver_build}
%{pyver_build_wheel}

%install
export PBR_VERSION=%{version}
%{pyver_install}

mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

%files -n python%{pyver}-%{sname}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/%{sname}*
%{pyver_sitelib}/python_%{sname}*

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Thu Jan 16 2020 RDO <dev@lists.rdoproject.org> 3.1.1-1
- Update to 3.1.1

* Thu Sep 26 2019 RDO <dev@lists.rdoproject.org> 3.1.0-1
- Update to 3.1.0

* Mon Sep 23 2019 RDO <dev@lists.rdoproject.org> 3.0.0-1
- Update to 3.0.0

