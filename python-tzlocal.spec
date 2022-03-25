#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	tzlocal
Summary:	tzinfo object for the local timezone
Name:		python-%{module}
Version:	2.1
Release:	3
License:	MIT
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/source/t/tzlocal/%{module}-%{version}.tar.gz
# Source0-md5:	c0877603ff9de71cd8ca6ee2b50d2ebd
URL:		https://github.com/regebro/tzlocal
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules >= 1:2.7
Requires:	python-pytz
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This Python module returns a tzinfo object with the local timezone
information under Unix and Win-32. It requires pytz, and returns pytz
tzinfo objects.

This module attempts to fix a glaring hole in pytz, that there is no
way to get the local timezone information, unless you know the
zoneinfo name, and under several Linux distros that’s hard or
impossible to figure out.

%package -n python3-%{module}
Summary:	tzinfo object for the local timezone for Python 3
Group:		Development/Languages/Python
Requires:	python3-modules >= 1:3.6
Requires:	python3-pytz

%description -n python3-%{module}
This Python module returns a tzinfo object with the local timezone
information under Unix and Win-32. It requires pytz, and returns pytz
tzinfo objects.

This module attempts to fix a glaring hole in pytz, that there is no
way to get the local timezone information, unless you know the
zoneinfo name, and under several Linux distros that’s hard or
impossible to figure out.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.txt README.rst
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.txt README.rst
%dir %{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/__pycache__
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
