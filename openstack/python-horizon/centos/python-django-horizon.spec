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
%global rhosp 0

%if 0%{?rhosp} == 0
%global with_translation_extraction_support 1
%else
%global with_translation_extraction_support 0
%endif

%global with_doc 1

Name:       python-django-horizon
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:      1
Version:    15.1.0
Release:    1%{?_tis_dist}.%{tis_patch_ver}
Summary:    Django application for talking to Openstack

Group:      Development/Libraries
# Code in horizon/horizon/utils taken from django which is BSD
License:    ASL 2.0 and BSD
URL:        http://horizon.openstack.org/
Source0:    horizon-%{version}.tar.gz
Source2:    openstack-dashboard-httpd-2.4.conf
Source3:    python-django-horizon-systemd.conf

# demo config for separate logging
Source4:    openstack-dashboard-httpd-logging.conf

# logrotate config
Source5:    python-django-horizon-logrotate.conf

# STX 
Source7:    horizon.init
Source8:    horizon-clearsessions
Source11:   horizon-patching-restart
Source13:   guni_config.py
Source14:   horizon-assets-compress

# Patches
Patch1:   0001-Remove-the-hard-coded-internal-URL-for-keystone.patch

#
# BuildArch needs to be located below patches in the spec file. Don't ask!
#

BuildArch:  noarch

%description
Horizon is a Django application for providing Openstack UI components.
It allows performing site administrator (viewing account resource usage,
configuring users, accounts, quotas, flavors, etc.) and end user
operations (start/stop/delete instances, create/restore snapshots, view
instance VNC console, etc.)

%package -n     python%{pyver}-django-horizon
Summary:    Django application for talking to Openstack
%{?python_provide:%python_provide python%{pyver}-django-horizon}

BuildRequires:   python%{pyver}-django
Requires:   python%{pyver}-django

# STX 
Requires: cgts-client

Requires:   python%{pyver}-pytz
Requires:   python%{pyver}-six >= 1.10.0
Requires:   python%{pyver}-pbr

BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-wheel
BuildRequires: python%{pyver}-pbr >= 2.0.0
BuildRequires: git
BuildRequires: python%{pyver}-six >= 1.10.0
BuildRequires: gettext

# for checks:
BuildRequires:   python%{pyver}-django-nose
BuildRequires:   python%{pyver}-mox3
BuildRequires:   python%{pyver}-nose
BuildRequires:   python%{pyver}-osprofiler
BuildRequires:   python%{pyver}-iso8601
BuildRequires:   python%{pyver}-pycodestyle
BuildRequires:   python%{pyver}-mock

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:   python-nose-exclude
BuildRequires:   python-selenium
BuildRequires:   python-netaddr
BuildRequires:   python-anyjson
%else
BuildRequires:   python%{pyver}-nose-exclude
BuildRequires:   python%{pyver}-selenium
BuildRequires:   python%{pyver}-netaddr
BuildRequires:   python%{pyver}-anyjson
%endif


# additional provides to be consistent with other django packages
Provides: django-horizon = %{epoch}:%{version}-%{release}
Obsoletes: python-django-openstack-auth < 4.0.0-1
Obsoletes: python2-django-openstack-auth < 4.0.0-1
# (TODO) remove following provides once the requirements have been fixed
# in all dashboard plugins
Provides: python-django-openstack-auth = %{epoch}:%{version}-%{release}
Provides: python2-django-openstack-auth = %{epoch}:%{version}-%{release}

%description -n python%{pyver}-django-horizon
Horizon is a Django application for providing Openstack UI components.
It allows performing site administrator (viewing account resource usage,
configuring users, accounts, quotas, flavors, etc.) and end user
operations (start/stop/delete instances, create/restore snapshots, view
instance VNC console, etc.)


%package -n openstack-dashboard
Summary:    Openstack web user interface reference implementation
Group:      Applications/System

Requires:   httpd
Requires:   python%{pyver}-django-horizon = %{epoch}:%{version}-%{release}
Requires:   python%{pyver}-django-compressor >= 2.0

%if 0%{rhosp} == 0
Requires:   openstack-dashboard-theme >= %{epoch}:%{version}-%{release}
%else
%{lua: ver = rpm.expand("%version"); x, y = string.find(ver, "%.");
maj = string.sub(ver, 1, x-1); rpm.define("version_major " .. maj .. ".0.0");}
Requires:   openstack-dashboard-theme >= %{epoch}:%{version_major}
%endif

Requires:   python%{pyver}-iso8601
Requires:   python%{pyver}-glanceclient >= 1:2.8.0
Requires:   python%{pyver}-keystoneclient >= 1:3.15.0
Requires:   python%{pyver}-keystoneauth1 >= 3.4.0
Requires:   python%{pyver}-novaclient >= 1:9.1.0
Requires:   python%{pyver}-neutronclient >= 6.7.0
Requires:   python%{pyver}-cinderclient >= 4.0.1
Requires:   python%{pyver}-swiftclient >= 3.2.0
Requires:   python%{pyver}-netaddr
Requires:   python%{pyver}-osprofiler >= 2.3.0
Requires:   python%{pyver}-django-pyscss >= 2.0.2
Requires:   python%{pyver}-XStatic
Requires:   python%{pyver}-XStatic-Angular >= 1:1.5.8.0
Requires:   python%{pyver}-XStatic-Angular-Bootstrap
Requires:   python%{pyver}-XStatic-Angular-Schema-Form
Requires:   python%{pyver}-XStatic-D3
Requires:   python%{pyver}-XStatic-Font-Awesome
Requires:   python%{pyver}-XStatic-JSEncrypt
Requires:   python%{pyver}-XStatic-Jasmine
Requires:   python%{pyver}-XStatic-Bootstrap-SCSS >= 3.3.7.1
Requires:   python%{pyver}-XStatic-termjs
Requires:   python%{pyver}-XStatic-smart-table
Requires:   python%{pyver}-XStatic-Angular-Gettext
Requires:   python%{pyver}-XStatic-Angular-FileUpload
Requires:   python%{pyver}-XStatic-bootswatch
Requires:   python%{pyver}-XStatic-roboto-fontface >= 0.5.0.0
Requires:   python%{pyver}-XStatic-mdi
Requires:   python%{pyver}-XStatic-objectpath
Requires:   python%{pyver}-XStatic-tv4
Requires:   python%{pyver}-django-debreach

Requires:   python%{pyver}-scss >= 1.3.4
Requires:   fontawesome-fonts-web >= 4.1.0

Requires:   python%{pyver}-oslo-concurrency >= 3.26.0
Requires:   python%{pyver}-oslo-config >= 2:5.2.0
Requires:   python%{pyver}-oslo-i18n >= 3.15.3
Requires:   python%{pyver}-oslo-serialization >= 2.18.0
Requires:   python%{pyver}-oslo-utils >= 3.33.0
Requires:   python%{pyver}-oslo-upgradecheck >= 0.1.1
Requires:   python%{pyver}-requests >= 2.14.2
Requires:   python%{pyver}-oslo-policy >= 1.30.0
Requires:   python%{pyver}-babel
Requires:   python%{pyver}-futurist

Requires:   openssl
Requires:   logrotate

# Handle python2 exception
%if %{pyver} == 2
Requires:   mod_wsgi
Requires:   python-django-appconf
Requires:   python-lesscpy
Requires:   python-pymongo >= 3.0.2
Requires:   python-semantic_version
Requires:   python-XStatic-jQuery
Requires:   python-XStatic-Hogan
Requires:   python-XStatic-JQuery-Migrate
Requires:   python-XStatic-JQuery-TableSorter
Requires:   python-XStatic-JQuery-quicksearch
Requires:   python-XStatic-Rickshaw
Requires:   python-XStatic-Spin
Requires:   python-XStatic-jquery-ui
Requires:   python-XStatic-Bootstrap-Datepicker
Requires:   python-XStatic-Angular-lrdragndrop
Requires:   python-XStatic-Magic-Search
Requires:   python-pint
Requires:   PyYAML >= 3.10
Requires:   python-memcached
%else
Requires:   python%{pyver}-mod_wsgi
Requires:   python%{pyver}-django-appconf
Requires:   python%{pyver}-lesscpy
Requires:   python%{pyver}-pymongo >= 3.0.2
Requires:   python%{pyver}-semantic_version
Requires:   python%{pyver}-XStatic-jQuery
Requires:   python%{pyver}-XStatic-Hogan
Requires:   python%{pyver}-XStatic-JQuery-Migrate
Requires:   python%{pyver}-XStatic-JQuery-TableSorter
Requires:   python%{pyver}-XStatic-JQuery-quicksearch
Requires:   python%{pyver}-XStatic-Rickshaw
Requires:   python%{pyver}-XStatic-Spin
Requires:   python%{pyver}-XStatic-jquery-ui
Requires:   python%{pyver}-XStatic-Bootstrap-Datepicker
Requires:   python%{pyver}-XStatic-Angular-lrdragndrop
Requires:   python%{pyver}-XStatic-Magic-Search
Requires:   python%{pyver}-pint
Requires:   python%{pyver}-PyYAML >= 3.10
Requires:   python%{pyver}-memcached
%endif

%if 0%{?with_translation_extraction_support} == 1
Requires:   python%{pyver}-django-babel
%endif

BuildRequires: python%{pyver}-django-debreach
BuildRequires: python%{pyver}-django-compressor >= 2.0
BuildRequires: python%{pyver}-django-pyscss >= 2.0.2
BuildRequires: python%{pyver}-XStatic
BuildRequires: python%{pyver}-XStatic-Angular >= 1:1.5.8.0
BuildRequires: python%{pyver}-XStatic-Angular-Bootstrap
BuildRequires: python%{pyver}-XStatic-Angular-Schema-Form
BuildRequires: python%{pyver}-XStatic-D3
BuildRequires: python%{pyver}-XStatic-Font-Awesome
BuildRequires: python%{pyver}-XStatic-JSEncrypt
BuildRequires: python%{pyver}-XStatic-Jasmine
BuildRequires: python%{pyver}-XStatic-Bootstrap-SCSS
BuildRequires: python%{pyver}-XStatic-termjs
BuildRequires: python%{pyver}-XStatic-smart-table
BuildRequires: python%{pyver}-XStatic-Angular-FileUpload
BuildRequires: python%{pyver}-XStatic-Angular-Gettext
BuildRequires: python%{pyver}-XStatic-bootswatch
BuildRequires: python%{pyver}-XStatic-roboto-fontface
BuildRequires: python%{pyver}-XStatic-mdi
BuildRequires: python%{pyver}-XStatic-objectpath
BuildRequires: python%{pyver}-XStatic-tv4
# bootstrap-scss requires at least python-scss >= 1.2.1
BuildRequires: python%{pyver}-scss >= 1.3.4
BuildRequires: fontawesome-fonts-web >= 4.1.0
BuildRequires: python%{pyver}-oslo-concurrency
BuildRequires: python%{pyver}-oslo-config
BuildRequires: python%{pyver}-oslo-i18n
BuildRequires: python%{pyver}-oslo-serialization
BuildRequires: python%{pyver}-oslo-utils
BuildRequires: python%{pyver}-oslo-policy
BuildRequires: python%{pyver}-babel

BuildRequires: python%{pyver}-pytz
BuildRequires: systemd
# STX 
BuildRequires: systemd-devel

# Handle python2 exception
%if %{pyver} == 2
BuildRequires: python-django-appconf
BuildRequires: python-lesscpy
BuildRequires: python-semantic_version
BuildRequires: python-XStatic-jQuery
BuildRequires: python-XStatic-Hogan
BuildRequires: python-XStatic-JQuery-Migrate
BuildRequires: python-XStatic-JQuery-TableSorter
BuildRequires: python-XStatic-JQuery-quicksearch
BuildRequires: python-XStatic-Rickshaw
BuildRequires: python-XStatic-Spin
BuildRequires: python-XStatic-jquery-ui
BuildRequires: python-XStatic-Bootstrap-Datepicker
BuildRequires: python-XStatic-Angular-lrdragndrop
BuildRequires: python-XStatic-Magic-Search
BuildRequires: python-pint
BuildRequires: python-memcached
%else
BuildRequires: python%{pyver}-django-appconf
BuildRequires: python%{pyver}-lesscpy
BuildRequires: python%{pyver}-semantic_version
BuildRequires: python%{pyver}-XStatic-jQuery
BuildRequires: python%{pyver}-XStatic-Hogan
BuildRequires: python%{pyver}-XStatic-JQuery-Migrate
BuildRequires: python%{pyver}-XStatic-JQuery-TableSorter
BuildRequires: python%{pyver}-XStatic-JQuery-quicksearch
BuildRequires: python%{pyver}-XStatic-Rickshaw
BuildRequires: python%{pyver}-XStatic-Spin
BuildRequires: python%{pyver}-XStatic-jquery-ui
BuildRequires: python%{pyver}-XStatic-Bootstrap-Datepicker
BuildRequires: python%{pyver}-XStatic-Angular-lrdragndrop
BuildRequires: python%{pyver}-XStatic-Magic-Search
BuildRequires: python%{pyver}-pint
BuildRequires: python%{pyver}-memcached
%endif
BuildRequires: python%{pyver}-glanceclient
BuildRequires: python%{pyver}-keystoneclient
BuildRequires: python%{pyver}-novaclient >= 1:9.1.0
BuildRequires: python%{pyver}-neutronclient
BuildRequires: python%{pyver}-cinderclient
BuildRequires: python%{pyver}-swiftclient

%description -n openstack-dashboard
Openstack Dashboard is a web user interface for Openstack. The package
provides a reference implementation using the Django Horizon project,
mostly consisting of JavaScript and CSS to tie it altogether as a standalone
site.

%if 0%{?with_doc}
%package doc
Summary:    Documentation for Django Horizon
Group:      Documentation

Requires:   python%{pyver}-django-horizon = %{epoch}:%{version}-%{release}
BuildRequires: python%{pyver}-sphinx >= 1.1.3

# Doc building basically means we have to mirror Requires:
BuildRequires: python%{pyver}-openstackdocstheme

%description doc
Documentation for the Django Horizon application for talking with Openstack
%endif

%if 0%{rhosp} == 0
%package -n openstack-dashboard-theme
Summary: OpenStack web user interface reference implementation theme module
Requires: openstack-dashboard = %{epoch}:%{version}-%{release}

%description -n openstack-dashboard-theme
Customization module for OpenStack Dashboard to provide a branded logo.
%endif

%prep
%autosetup -n horizon-%{upstream_version} -S git

# STX remove troublesome files introduced by tox
rm -f openstack_dashboard/test/.secret_key_store
rm -f openstack_dashboard/test/*.secret_key_store.lock
rm -f openstack_dashboard/local/.secret_key_store
rm -f openstack_dashboard/local/*.secret_key_store.lock
rm -rf horizon.egg-info

# drop config snippet
cp -p %{SOURCE4} .
cp -p %{SOURCE13} .

# customize default settings
# WAS [PATCH] disable debug, move web root
sed -i "/^DEBUG =.*/c\DEBUG = False" openstack_dashboard/local/local_settings.py.example
sed -i "/^WEBROOT =.*/c\WEBROOT = '/dashboard/'" openstack_dashboard/local/local_settings.py.example
sed -i "/^.*ALLOWED_HOSTS =.*/c\ALLOWED_HOSTS = ['horizon.example.com', 'localhost']" openstack_dashboard/local/local_settings.py.example
sed -i "/^.*LOCAL_PATH =.*/c\LOCAL_PATH = '/tmp'" openstack_dashboard/local/local_settings.py.example
sed -i "/^.*POLICY_FILES_PATH =.*/c\POLICY_FILES_PATH = '/etc/openstack-dashboard'" openstack_dashboard/local/local_settings.py.example

sed -i "/^BIN_DIR = .*/c\BIN_DIR = '/usr/bin'" openstack_dashboard/settings.py
sed -i "/^COMPRESS_PARSER = .*/a COMPRESS_OFFLINE = True" openstack_dashboard/settings.py

# set COMPRESS_OFFLINE=True
sed -i 's:COMPRESS_OFFLINE.=.False:COMPRESS_OFFLINE = True:' openstack_dashboard/settings.py

# STX: MANIFEST needs .eslintrc files for angular
echo "include .eslintrc"   >> MANIFEST.in
# MANIFEST needs to include json and pot files under openstack_dashboard 
echo "recursive-include openstack_dashboard *.json *.pot .eslintrc"   >> MANIFEST.in
# MANIFEST needs to include pot files  under horizon
echo "recursive-include horizon *.pot .eslintrc"   >> MANIFEST.in

# Fix manage.py shebang
sed -i 's/\/usr\/bin\/env python/\/usr\/bin\/env python%{pyver}/' manage.py

# Fix python executable depending on python version
sed -i 's/\/usr\/bin\/python /\/usr\/bin\/python%{pyver} /g' %{SOURCE3}

%build
# compile message strings
cd horizon && django-admin compilemessages && cd ..
cd openstack_dashboard && django-admin compilemessages && cd ..
# Dist tarball is missing .mo files so they're not listed in distributed egg metadata.
# Removing egg-info and letting PBR regenerate it was working around that issue
# but PBR cannot regenerate complete SOURCES.txt so some other files wont't get installed.
# Further reading why not remove upstream egg metadata:
# https://github.com/emonty/python-oslo-messaging/commit/f632684eb2d582253601e8da7ffdb8e55396e924
# https://fedorahosted.org/fpc/ticket/488
# STX: 2 problems.  1  we dont have an egg yet.  2 there are no .mo files
#echo >> horizon.egg-info/SOURCES.txt
#ls */locale/*/LC_MESSAGES/django*mo >> horizon.egg-info/SOURCES.txt
export PBR_VERSION=%{version}
%{pyver_build}

# compress css, js etc.
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py
# get it ready for compressing later in puppet-horizon
# STX: run compression on the controller
# STX: turn off compression because /dev/log does not exist in mock
#%{pyver_bin} manage.py collectstatic --noinput --clear
#%{pyver_bin} manage.py compress --force

%if 0%{?with_doc}
# build docs
export PYTHONPATH=.
sphinx-build-%{pyver} -b html doc/source html
# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo
%endif

# undo hack
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py

%{pyver_build_wheel}

%install
%{pyver_install}

# drop httpd-conf snippet
install -m 0644 -D -p %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
install -d -m 755 %{buildroot}%{_datadir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sharedstatedir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sysconfdir}/openstack-dashboard
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# STX
install -d -m 755 %{buildroot}/opt/branding
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 755 -D -p  %{SOURCE7} %{buildroot}%{_sysconfdir}/rc.d/init.d/horizon
install -m 755 -D -p %{SOURCE8} %{buildroot}/%{_bindir}/horizon-clearsessions
install -m 755 -D -p %{SOURCE11} %{buildroot}/%{_bindir}/horizon-patching-restart
install -m 755 -D -p %{SOURCE14} %{buildroot}/%{_bindir}/horizon-assets-compress

# drop config snippet
install -m 0644 -D -p %{SOURCE4} .

# create directory for systemd snippet
mkdir -p %{buildroot}%{_unitdir}/httpd.service.d/
cp %{SOURCE3} %{buildroot}%{_unitdir}/httpd.service.d/openstack-dashboard.conf


# Copy everything to /usr/share
mv %{buildroot}%{pyver_sitelib}/openstack_dashboard \
   %{buildroot}%{_datadir}/openstack-dashboard
# STX
cp guni_config.py %{buildroot}%{_datadir}/openstack-dashboard
cp manage.py %{buildroot}%{_datadir}/openstack-dashboard
rm -rf %{buildroot}%{pyver_sitelib}/openstack_dashboard

# remove unnecessary .po files
find %{buildroot} -name django.po -exec rm '{}' \;
find %{buildroot} -name djangojs.po -exec rm '{}' \;

# Move config to /etc, symlink it back to /usr/share
mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py.example %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings
# STX: we do not want to have this symlink, puppet will overwrite the content of local_settings
#ln -s ../../../../..%{_sysconfdir}/openstack-dashboard/local_settings %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py

%if 0%{?rhosp}
mkdir -p %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings.d
mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d/* %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings.d
rmdir %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d
ln -s ../../../../..%{_sysconfdir}/openstack-dashboard/local_settings.d %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d
%endif

mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/conf/*.json %{buildroot}%{_sysconfdir}/openstack-dashboard
mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/conf/nova_policy.d %{buildroot}%{_sysconfdir}/openstack-dashboard

%find_lang django --all-name

grep "\/usr\/share\/openstack-dashboard" django.lang > dashboard.lang
grep "\/site-packages\/horizon" django.lang > horizon.lang

# copy static files to %{_datadir}/openstack-dashboard/static
mkdir -p %{buildroot}%{_datadir}/openstack-dashboard/static
cp -a openstack_dashboard/static/* %{buildroot}%{_datadir}/openstack-dashboard/static
cp -a horizon/static/* %{buildroot}%{_datadir}/openstack-dashboard/static
# STX: there is no static folder, since compress step was skipped
#cp -a static/* %{buildroot}%{_datadir}/openstack-dashboard/static

# create /var/run/openstack-dashboard/ and own it
mkdir -p %{buildroot}%{_sharedstatedir}/openstack-dashboard

# create /var/log/horizon and own it
mkdir -p %{buildroot}%{_var}/log/horizon

# place logrotate config:
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cp -a %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-dashboard

%check
%{pyver_bin} manage.py test horizon --settings=horizon.test.settings

%post -n openstack-dashboard
# ugly hack to set a unique SECRET_KEY
sed -i "/^from horizon.utils import secret_key$/d" /etc/openstack-dashboard/local_settings
sed -i "/^SECRET_KEY.*$/{N;s/^.*$/SECRET_KEY='`openssl rand -hex 10`'/}" /etc/openstack-dashboard/local_settings
# reload systemd unit files
systemctl daemon-reload >/dev/null 2>&1 || :

%postun
# update systemd unit files
%{systemd_postun}

%files -n python%{pyver}-django-horizon -f horizon.lang
%doc README.rst openstack-dashboard-httpd-logging.conf
%license LICENSE
%dir %{pyver_sitelib}/horizon
%{pyver_sitelib}/horizon/*.py*
%{pyver_sitelib}/horizon/browsers
%{pyver_sitelib}/horizon/conf
%{pyver_sitelib}/horizon/contrib
%{pyver_sitelib}/horizon/forms
%{pyver_sitelib}/horizon/hacking
%{pyver_sitelib}/horizon/management
%{pyver_sitelib}/horizon/static
%{pyver_sitelib}/horizon/tables
%{pyver_sitelib}/horizon/tabs
%{pyver_sitelib}/horizon/templates
%{pyver_sitelib}/horizon/templatetags
%{pyver_sitelib}/horizon/test
%{pyver_sitelib}/horizon/utils
%{pyver_sitelib}/horizon/workflows
%{pyver_sitelib}/horizon/karma.conf.js
%{pyver_sitelib}/horizon/middleware
%{pyver_sitelib}/openstack_auth
%{pyver_sitelib}/*.egg-info
%if %{pyver} == 3
%{pyver_sitelib}/horizon/__pycache__
%endif

%files -n openstack-dashboard -f dashboard.lang
%license LICENSE
%dir %{_datadir}/openstack-dashboard/
%{_datadir}/openstack-dashboard/*.py*
%{_datadir}/openstack-dashboard/static
%{_datadir}/openstack-dashboard/openstack_dashboard/*.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/api
%{_datadir}/openstack-dashboard/openstack_dashboard/contrib
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/admin
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/identity
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/project
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/settings
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/__init__.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/django_pyscss_fix
%{_datadir}/openstack-dashboard/openstack_dashboard/enabled
%{_datadir}/openstack-dashboard/openstack_dashboard/karma.conf.js
%{_datadir}/openstack-dashboard/openstack_dashboard/local
%{_datadir}/openstack-dashboard/openstack_dashboard/management
%{_datadir}/openstack-dashboard/openstack_dashboard/static
%{_datadir}/openstack-dashboard/openstack_dashboard/templates
%{_datadir}/openstack-dashboard/openstack_dashboard/templatetags
%{_datadir}/openstack-dashboard/openstack_dashboard/themes
%{_datadir}/openstack-dashboard/openstack_dashboard/test
%{_datadir}/openstack-dashboard/openstack_dashboard/usage
%{_datadir}/openstack-dashboard/openstack_dashboard/utils
%{_datadir}/openstack-dashboard/openstack_dashboard/wsgi
%dir %{_datadir}/openstack-dashboard/openstack_dashboard
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??_??
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??/LC_MESSAGES
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??_??/LC_MESSAGES

%if 0%{?rhosp}
%dir %attr(0750, root, apache) %{_sysconfdir}/openstack-dashboard/local_settings.d/
%{_sysconfdir}/openstack-dashboard/local_settings.d/*.example
%endif

%{_datadir}/openstack-dashboard/openstack_dashboard/.eslintrc
# fix installed (but unpackaged) files
%{_datadir}/openstack-dashboard/openstack_dashboard/__pycache__
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/__pycache__

%if %{pyver} == 3
%{_datadir}/openstack-dashboard/openstack_dashboard/__pycache__
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/__pycache__
%endif

%dir %attr(0750, root, apache) %{_sysconfdir}/openstack-dashboard
%dir %attr(0750, apache, apache) %{_sharedstatedir}/openstack-dashboard
%dir %attr(0750, apache, apache) %{_var}/log/horizon
%config(noreplace) %{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/local_settings
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/cinder_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/keystone_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/nova_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/glance_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/neutron_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/nova_policy.d/api-extensions.yaml
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/logrotate.d/openstack-dashboard
%attr(755,root,root) %dir %{_unitdir}/httpd.service.d
%config(noreplace) %{_unitdir}/httpd.service.d/openstack-dashboard.conf

# STX
%dir /opt/branding
%{_sysconfdir}/rc.d/init.d/horizon
%{_bindir}/horizon-clearsessions
%{_bindir}/horizon-patching-restart
%{_bindir}/horizon-assets-compress


%if 0%{?with_doc}
%files doc
%doc html
%license LICENSE
%endif

%if 0%{rhosp} == 0
%files -n openstack-dashboard-theme
#%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/theme
#%{_datadir}/openstack-dashboard/openstack_dashboard/enabled/_99_customization.*
%endif

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Thu Jan 23 2020 RDO <dev@lists.rdoproject.org> 1:16.1.0-1
- Update to 16.1.0

* Wed Oct 16 2019 RDO <dev@lists.rdoproject.org> 1:16.0.0-1
- Update to 16.0.0

* Fri Oct 11 2019 RDO <dev@lists.rdoproject.org> 1:16.0.0-0.2.0rc1
- Update to 16.0.0.0rc2

* Mon Sep 30 2019 RDO <dev@lists.rdoproject.org> 1:16.0.0-0.1.0rc1
- Update to 16.0.0.0rc1

