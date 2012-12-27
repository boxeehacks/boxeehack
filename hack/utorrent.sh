#!/bin/sh
utorrent_path=`dirname $0`/utorrent

export LD_LIBRARY_PATH=$utorrent_path/lib:$LD_LIBRARY_PATH

$utorrent_path/lib/ld-linux.so.2 $utorrent_path/utserver -settingspath $utorrent_path -configfile $utorrent_path/utserver.conf -daemon > $utorrent_path/utorrent.log 2>&1