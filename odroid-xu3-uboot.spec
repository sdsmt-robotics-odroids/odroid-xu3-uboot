%global commit fe2f831fd44a4071f58a42f260164544697aa666

Name:           odroid-xu3-uboot
Version:        2015.11.04
Release:        1%{?dist}
Summary:        U-boot for ODROID-XU3/XU4

Group:          System Environment/Base
License:        GPLv2
URL:            http://odroid.com/dokuwiki/doku.php?id=en:odroid-xu3
Source0:        https://github.com/hardkernel/u-boot/archive/%{commit}/u-boot-%{commit}.tar.gz
Source1:        boot.ini
Source2:        grubby
Patch0:         %{name}-2015.02.11-smc.patch
Patch1:         %{name}-2015.02.11-gcc5.patch
Patch2:         %{name}-2015.02.11-arm-asm-io-h-use-static-inline.patch
Patch3:         %{name}-2015.02.11-leds-weak.patch
Patch4:         %{name}-2015.02.11-show-boot-progress-weak.patch
Patch5:         %{name}-2015.11.04-ext4load.patch

# We always need to use a cross compiler because we can't use hardfloat static
# libraries. This means that we'll always produce an ARM package, even when
# built on x86 machines. The code compiled here is also indifferent of the
# architecture used on the ODROID's OS.
BuildArch:      noarch

BuildRequires:  arm-none-eabi-gcc-cs
BuildRequires:  dos2unix
Requires:       grubby

%description
U-boot for Hardkernel's ODROID-XU3/XU4. This package installs u-boot.bin and a
default boot.ini, and also configures grubby.

%prep
%setup -qn u-boot-%{commit}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
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
/boot/uboot/u-boot.bin

%changelog
* Sat Dec 26 2015 Scott K Logan <logans@cottsay.net> - 2015.11.04-1
- Update to latest upstream
- Remove boot.scr
- Add patch for EXT4 support

* Wed Sep 09 2015 Scott K Logan <logans@cottsay.net> - 2015.02.11-2
- Update grubby config and boot.ini to store kernel and image in /boot

* Thu Apr 09 2015 Scott K Logan <logans@cottsay.net> - 2015.02.11-1
- Initial package
