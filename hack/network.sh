#!/bin/sh
ln -s /data/etc/ppp/secrets /data/hack/ppp/chap-secrets
ln -s /data/etc/ppp/options.pptp /data/hack/ppp/options.pptp
ln -s /data/etc/ppp/secrets /data/hack/ppp/pap-secrets
ln -s /data/etc/ppp/resolv.conf /data/hack/ppp/resolv.conf
ln -s /data/etc/ppp/peers/vpn /data/hack/ppp/peers/vpn
mount -o bind /data/hack/ppp /etc/ppp
