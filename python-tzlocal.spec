#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	tzlocal
Summary:	tzinfo object for the local timezone
Summary(pl.UTF-8):	Obiekt tzinfo dla lokalnej strefy czasowej
Name:		python-%{module}
# keep 2.x here for python2 support
Version:	2.1
Release:	7
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/tzlocal/
Source0:	https://files.pythonhosted.org/packages/source/t/tzlocal/%{module}-%{version}.tar.gz
# Source0-md5:	c0877603ff9de71cd8ca6ee2b50d2ebd
Patch0:		tzlocal-mock.patch
URL:		https://github.com/regebro/tzlocal
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-pytz
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytz
%endif
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This Python module returns a tzinfo object with the local timezone
information under Unix and Win-32. It requires pytz, and returns pytz
tzinfo objects.

This module attempts to fix a glaring hole in pytz, that there is no
way to get the local timezone information, unless you know the
zoneinfo name, and under several Linux distros that's hard or
impossible to figure out.

%description -l pl.UTF-8
Ten moduł Pythona zwraca obiekt tzinfo z informacjami o lokalnej
strefie czasowej pod Uniksem i Win-32. Wymaga pytz i zwraca obiekty
tzinfo z pytz.

Moduł próbuje naprawić dziurę świecącą w pytz, że nie ma sposobu
uzyskania informacji o lokalnej strefie czasowej, chyba że znamy jej
nazwą, a w niektórych dystrybucjach Linuksa jest to trudne lub
niemożliwe do uzyskania.

%package -n python3-%{module}
Summary:	tzinfo object for the local timezone
Summary(pl.UTF-8):	Obiekt tzinfo dla lokalnej strefy czasowej
Group:		Development/Languages/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-%{module}
This Python module returns a tzinfo object with the local timezone
information under Unix and Win-32. It requires pytz, and returns pytz
tzinfo objects.

This module attempts to fix a glaring hole in pytz, that there is no
way to get the local timezone information, unless you know the
zoneinfo name, and under several Linux distros that's hard or
impossible to figure out.

%description -n python3-%{module} -l pl.UTF-8
Ten moduł Pythona zwraca obiekt tzinfo z informacjami o lokalnej
strefie czasowej pod Uniksem i Win-32. Wymaga pytz i zwraca obiekty
tzinfo z pytz.

Moduł próbuje naprawić dziurę świecącą w pytz, że nie ma sposobu
uzyskania informacji o lokalnej strefie czasowej, chyba że znamy jej
nazwą, a w niektórych dystrybucjach Linuksa jest to trudne lub
niemożliwe do uzyskania.

%prep
%setup -q -n %{module}-%{version}
%patch -P0 -p1

# it was meant to be a symlink
ln -snf ../usr/share/zoneinfo/Africa/Harare tests/test_data/symlink_localtime/etc/localtime

%build
%if %{with python2}
%py_build

%if %{with tests}
# tz_from_env test expects absolute path to executable
PYTHONPATH=$(pwd) \
%{__python} $(pwd)/tests/tests.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} $(pwd)/tests/tests.py
%endif
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
%doc CHANGES.txt LICENSE.txt README.rst
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.rst
%dir %{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/__pycache__
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
