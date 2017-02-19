#!/bin/sh

if [ -e /data/etc/passwd ]; then
	pw=`head -n 1 /data/etc/passwd`
else
	pw=secret
fi

if [ ! -f /data/hack/bin/dropbear ]; then
	ln -sf /data/hack/bin/dropbearmulti-i686 /data/hack/bin/dropbear
	ln -sf /data/hack/bin/dropbearmulti-i686 /data/hack/bin/ssh
	ln -sf /data/hack/bin/dropbearmulti-i686 /data/hack/bin/dropbearkey
	ln -sf /data/hack/bin/dropbearmulti-i686 /data/hack/bin/dropbearconvert
	ln -sf /data/hack/bin/dropbearmulti-i686 /data/hack/bin/scp
fi

if [ ! -f /data/hack/.ssh/id_rsa ]; then
	mkdir -p /data/hack/.ssh
	/data/hack/bin/dropbearkey -t rsa -f /data/hack/.ssh/id_rsa
fi

if [ ! -f /data/hack/.ssh/profile ]; then
	cat /etc/profile > /data/hack/.ssh/profile
	echo PATH=/data/hack/bin:\$PATH >> /data/hack/.ssh/profile
	echo LD_LIBRARY_PATH=.:/data/hack/lib:\$LD_LIBRARY_PATH >> /data/hack/.ssh/profile
	echo TERM=vt102 >> /data/hack/.ssh/profile
fi

umount /etc/profile 2>/dev/null
umount /etc/passwd 2>/dev/null
mount -o bind /data/hack/.ssh/profile /etc/profile

echo root:`openssl passwd -1 -salt boxee $pw`:0:0:root:/:/data/hack/bin/bash > /data/hack/.ssh/passwd
tail -n+2 /etc/passwd >> /data/hack/.ssh/passwd
mount -o bind /data/hack/.ssh/passwd /etc/passwd

echo /bin/sh>/tmp/shells
echo /data/hack/bin/bash>>/tmp/shells
/data/hack/bin/dropbear -r /data/hack/.ssh/id_rsa

