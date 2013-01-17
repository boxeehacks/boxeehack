#!/bin/sh
# Requires: writable_etc.sh
CONFDIR=/etc/dropbear

[ -d ${CONFDIR} ] || mkdir -p ${CONFDIR};
[ -f ${CONFDIR}/dropbear_rsa_host_key ] || dropbearkey -t rsa -f ${CONFDIR}/dropbear_rsa_host_key;
[ -f ${CONFDIR}/dropbear_dss_host_key ] || dropbearkey -t dss -f ${CONFDIR}/dropbear_dss_host_key;

dropbear;
