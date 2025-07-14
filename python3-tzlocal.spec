#
# Conditional build:
%bcond_without	tests	# unit tests

%define 	module	tzlocal
Summary:	tzinfo object for the local timezone
Summary(pl.UTF-8):	Obiekt tzinfo dla lokalnej strefy czasowej
Name:		python3-%{module}
Version:	5.3.1
Release:	1
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/tzlocal/
Source0:	https://files.pythonhosted.org/packages/source/t/tzlocal/%{module}-%{version}.tar.gz
# Source0-md5:	f8eb4bf0eb262ba422741d032d6cfedf
URL:		https://github.com/regebro/tzlocal
BuildRequires:	python3 >= 1:3.9
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-setuptools >= 1:64
%if %{with tests}
BuildRequires:	python3-pytest >= 4.3
BuildRequires:	python3-pytest-mock >= 3.3
BuildRequires:	python3-pytz
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.9
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

%prep
%setup -q -n %{module}-%{version}

# it was meant to be a symlink
ln -snf ../usr/share/zoneinfo/Africa/Harare tests/test_data/symlink_localtime/etc/localtime
ln -snf ../usr/share/zoneinfo/Africa/Harare tests/test_data/conflicting/etc/localtime
ln -snf ../usr/share/zoneinfo/Etc/UTC tests/test_data/noconflict/etc/localtime

%build
%py3_build_pyproject

%if %{with tests}
# test_noconflict seems broken, even without /etc/localtime there are 3 different entries
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_mock.plugin \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests -k 'not test_noconflict'
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/tzlocal
%{py3_sitescriptdir}/tzlocal-%{version}.dist-info
