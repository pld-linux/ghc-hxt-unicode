#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	hxt-unicode
Summary:	Unicode en-/decoding functions for utf-8, iso-latin-* and other encodings
Summary(pl.UTF-8):	Funcje kodujące/dekodujące Unicode dla utf-8, iso-latin-* i innych kodowań
Name:		ghc-%{pkgname}
Version:	9.0.2.4
Release:	2
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/hxt-unicode
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	e4f61cef60736dca5778641e791f66c8
URL:		http://hackage.haskell.org/package/hxt-unicode
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-hxt-charproperties >= 9
BuildRequires:	ghc-hxt-charproperties < 10
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-hxt-charproperties-prof >= 9
BuildRequires:	ghc-hxt-charproperties-prof < 10
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 4
Requires:	ghc-hxt-charproperties >= 9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Unicode encoding and decoding functions for utf-8, iso-latin-* and
somes other encodings, used in the Haskell XML Toolbox.
ISO Latin 1-16, UTF-8, UTF-16, ASCII are supported. Decoding is done
with lazy functions, errors may be detected or ignored.

%description -l pl.UTF-8
Funkcje kodujące i dekodujące dla utf-8, iso-latin-* i niektórych
innych kodowań, używane w bibliotece Haskell XML Toolbox. Obsługiwane
są ISO Latin 1-16, UTF-8, UTF-16, ASCII. Dekodowanie jest wykonywane
przy użyciu funkcji leniwych, błędy mogą być wykrywane lub ignorowane.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-hxt-charproperties-prof >= 9

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build

runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Char
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Char/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Char/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/String
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/String/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/String/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Char/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/String/*.p_hi
%endif
