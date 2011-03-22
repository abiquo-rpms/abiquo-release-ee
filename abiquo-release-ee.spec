%define builtin_release_name RC2
%define base_release_version 1.7.5
%define builtin_release_variant Enterprise Edition
%define builtin_release_version %{base_release_version}
%define real_release_version %{?release_version}%{!?release_version:%{builtin_release_version}}
%define real_release_name %{?release_name}%{!?release_name:%{builtin_release_name}}
%define product_family Abiquo Linux

%define current_arch %{_arch}

Summary: %{product_family} release file
Name: abiquo-release-ee
Epoch: 10
Version: 1.7.5
Release: 4%{?dist}
License: GPL
Group: System Environment/Base
Source: %{name}-%{builtin_release_version}.tar.gz
Source1: abiquo-release
Patch: centos-release-skip-eula.patch

Obsoletes: rawhide-release redhat-release-as redhat-release-es redhat-release-ws redhat-release-de comps abiquo-release
Obsoletes: rpmdb-redhat redhat-release whitebox-release fedora-release sl-release enterprise-release
Provides: abiquo-release centos-release redhat-release yumconf
Requires: abiquo-release-notes

BuildRoot: %{_tmppath}/abiquo-release-root
BuildArch: noarch

%description
%{product_family} release files

%prep
%setup -q 
%patch -p1

%build
python -c "import py_compile; py_compile.compile('eula.py')"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc
echo "%{product_family} %{builtin_release_variant} release %{base_release_version} (%{real_release_name})" > $RPM_BUILD_ROOT/etc/redhat-release
cp $RPM_BUILD_ROOT/etc/redhat-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m" >> $RPM_BUILD_ROOT/etc/issue
cp $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue

mkdir -p $RPM_BUILD_ROOT/usr/share/firstboot/modules
cp eula.py* $RPM_BUILD_ROOT/usr/share/firstboot/modules

mkdir -p $RPM_BUILD_ROOT/usr/share/eula
cp eula.[!py]* $RPM_BUILD_ROOT/usr/share/eula

#mkdir -p $RPM_BUILD_ROOT/var/lib
#cp %{current_arch}/supportinfo $RPM_BUILD_ROOT/var/lib/supportinfo

mkdir -p -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in Abiquo*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

mkdir -p -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
        install -m 644 $file $RPM_BUILD_ROOT/etc/pki/rpm-gpg
done

cp %{SOURCE1} $RPM_BUILD_ROOT/etc/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(0644,root,root) /etc/redhat-release
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/*
%doc EULA GPL autorun-template
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
/usr/share/firstboot/modules/eula.py*
/usr/share/eula/eula.*
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*
/etc/abiquo-release
#/var/lib/supportinfo

%changelog
* Tue Mar 22 2011 Sergio Rubio <rubiojr@frameos.org> - 1.7.5-4
- bumped release to RC2

* Fri Mar 18 2011 Sergio Rubio <srubio@abiquo.com> - 1.7.5-3
- version bump: 1.7.5 RC1

* Fri Mar 04 2011 Sergio Rubio <srubio@abiquo.com> - 1.7.5-2
- added abiquo-release file

* Fri Mar 04 2011 Sergio Rubio <srubio@abiquo.com> - 1.7.5-1
- 1.7.5 preview

* Wed Feb 02 2011 Sergio Rubio <srubio@abiquo.com> - 1.7-5
- fixed build arch

* Wed Feb 02 2011 Sergio Rubio <srubio@abiquo.com> - 1.7-4
- fixed release strings

* Wed Jan 26 2011 Sergio Rubio <srubio@abiquo.com> - 1.7-3
- obsoletes abiquo-release

* Mon Dec 13 2010 Sergio Rubio <srubio@abiquo.com> - 1.7-2
- updated to 1.7

* Mon Nov 08 2010 Sergio Rubio <srubio@abiquo.com> 1.6.8-2
- updated to 1.6.8 Final Release

* Fri Oct 01 2010 Sergio Rubio <srubio@abiquo.com> 1.6.8-1
- updated to 1.6.8 preview

* Fri Oct 01 2010 Sergio Rubio <srubio@abiquo.com> 1.6.5-5
- updated to Beta3

* Fri Oct 01 2010 Sergio Rubio <srubio@abiquo.com> 1.6.5-4
- updated to Beta2

* Thu Sep 09 2010 Sergio Rubio <srubio@abiquo.com> 1.6.5-3
- updated to Beta1

* Thu Sep 09 2010 Sergio Rubio <srubio@abiquo.com> 1.6.5-2
- Fix yum repositories

* Thu Sep 02 2010 Sergio Rubio <srubio@abiquo.com>
- Initial release
