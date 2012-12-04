#!/bin/sh

date=`date -u '+%a, %d %b %Y %H:%M:%S %Z'`
LOG_PATH=/data/.persistent/.mrwong
if [ ! -z "${QUERY_STRING}" ]
then
	LOG_FILE="`basename ${LOG_PATH}/${QUERY_STRING}`"
	LOG_FILE="${LOG_PATH}/${LOG_FILE}"
	if [ "`dirname ${LOG_FILE}`" = "${LOG_PATH}" ] && [ -f "${LOG_FILE}" ]
	then
		LOG_BASE="`basename ${LOG_FILE}`"
		LOG_SIZE="`stat -c%s ${LOG_FILE}`"
		cat <<EOF
Expires: $date
Content-Type: application/octet-stream
Content-Disposition: attachment; filename=$LOG_BASE
Content-Length: $LOG_SIZE

EOF
		cat $LOG_FILE
	else
		echo "Location: /"
	fi
else
	echo "Location: /"
fi
