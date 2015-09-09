%global commit d80b05d5624ecba99c15ee2a7b3f59ebf6f8f1e8

Name:           odroid-xu3-uboot
Version:        2015.02.11
Release:        2%{?dist}
Summary:        U-boot for ODROID-XU3

Group:          System Environment/Base
License:        GPLv2
URL:            http://odroid.com/dokuwiki/doku.php?id=en:odroid-xu3
Source0:        https://github.com/hardkernel/u-boot/archive/%{commit}/u-boot-%{commit}.tar.gz
Source1:        boot.ini
Source2:        grubby

# We always need to use a cross compiler because we can't use hardfloat static
# libraries. This means that we'll always produce an ARM package, even when
# built on x86 machines. The code compiled here is also indifferent of the
# architecture used on the ODROID's OS.
BuildArch:      noarch

BuildRequires:  arm-none-eabi-gcc-cs
BuildRequires:  dos2unix
Requires:       grubby

%description
U-boot for Hardkernel's ODROID-XU3. This package installs u-boot.bin and a
default boot.ini, and also configures grubby.

%prep
%setup -qn u-boot-%{commit}
dos2unix COPYING.txt
chmod 644 COPYING.txt

%build
make %{?_smp_mflags} odroid_config
make %{?_smp_mflags} CROSS_COMPILE=arm-none-eabi-

%install
install -p -m0644 -D %{SOURCE2} %{buildroot}%{_datadir}/%{name}/grubby-%{version}-%{release}
install -p -m0644 -D %{SOURCE1} %{buildroot}/boot/uboot/boot.ini
install -p -m0755 -D u-boot.bin %{buildroot}/boot/uboot/u-boot.bin

ln -s grubby-%{version}-%{release} %{buildroot}%{_datadir}/%{name}/grubby

touch %{buildroot}/boot/uboot/boot.scr

%post
cat %{_datadir}/%{name}/grubby-%{version}-%{release} >> %{_sysconfdir}/sysconfig/uboot

%preun
while read l; do
  sed -i "0,/^`echo "$l" | sed 's/\//\\\\\//g'`/{//d}" %{_sysconfdir}/sysconfig/uboot
done < %{_datadir}/%{name}/grubby-%{version}-%{release}

%files
%doc COPYING COPYING.txt CREDITS MAINTAINERS README
%{_datadir}/%{name}/grubby
%{_datadir}/%{name}/grubby-%{version}-%{release}
%config(noreplace) /boot/uboot/boot.ini
%config(noreplace) /boot/uboot/boot.scr
/boot/uboot/u-boot.bin

%changelog
* Wed Sep 09 2015 Scott K Logan <logans@cottsay.net> - 2015.02.11-2
- Update grubby config and boot.ini to store kerneland image in /boot

* Thu Apr 09 2015 Scott K Logan <logans@cottsay.net> - 2015.02.11-1
- Initial package
