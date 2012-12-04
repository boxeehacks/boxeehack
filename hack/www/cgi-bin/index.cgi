#!/bin/sh

date=`date -u '+%a, %d %b %Y %H:%M:%S %Z'`
LOG_PATH=/data/.persistent/.mrwong
PP_BIN=/opt/local/bin/get_platform_params
DTOOL_BIN=/opt/local/bin/dtool
VERSION="`cat /opt/boxee/VERSION`"

BX_MODEL="`${PP_BIN} 1`"
BX_SERIAL="`${PP_BIN} 2`"
BX_RTFIRM="${VERSION}"
BX_CPUTMP="`${DTOOL_BIN} 2`"
BX_FANSPD="`${DTOOL_BIN} 3`"

cat << EOF
Content-type: text/html
Expires: $date

<html>
<head>
	<title>Boxee Support Tool</title>
	<style type='text/css'>
	html, body, table, th, td { font: 10pt arial, sans serif; margin: 0px; padding: 0px; }
	th { font-weight: bold; text-align: left; }
	td { padding-left: 5px; }
	</style>
</head>
<body>

EOF
if [ ! -z "$QUERY_STRING" ]; then
	if [ "$QUERY_STRING" = "MAIL_FAIL" -o "$QUERY_STRING" = "MAIL_INVALID" ]; then
		MSG="Failure occured while sending report to Boxee. Please try again later."
		COL="#ff4000"
	elif [ "$QUERY_STRING" = "MAIL_SUCCESS" ]; then
		MSG="Your report has been successfully sent to Boxee."
		COL="#98c35c"
	else
		MSG="Unknown status."
		COL="#ff4000"
	fi
	echo "<div style='margin: 0px; padding: 0px; text-align: center; margin-bottom: 5px; width: 100%; border-bottom: 1px solid black; background-color: ${COL};'>${MSG}</div>"
else
	echo "<div style='margin-top: 1px;'>&nbsp;</div>"
fi


echo "<p style='font-weight: bold; margin-left: 5px;'>BOXEE SUPPORT TOOL</p>"

echo "<table style='margin-left: 10px; padding: 3px; border: 1px solid black;'>"
echo "<tr><td>Hardware Model:</td><td>${BX_MODEL}</td></tr>"
echo "<tr><td>Serial Number:</td><td>${BX_SERIAL}</td></tr>"
echo "<tr><td>Boxee Version:</td><td>${BX_RTFIRM}</td></tr>"
echo "<tr><td>CPU Temperature:</td><td>${BX_CPUTMP} C</td></tr>"
echo "<tr><td>Fan Speed:</td><td>${BX_FANSPD}%</td></tr>"
echo "</table>"

# boxee logs
f=`( cd ${LOG_PATH}; find . -name boxee.\* ) | sort -r | xargs`
c=`echo $f | wc -w`

echo "<br/><br/><p style='border-bottom: 1px solid black;'>Boxee Logs [<a href='get_log.cgi'>Get latest</a>&nbsp;|&nbsp;<a href='clear_log.cgi'>Clear all</a>&nbsp;|&nbsp;<a href="../index.php">Back</a>]&nbsp;</p><table>"
echo "<tr><th style='width: 180px;'>Date</th><th style='width: 100px;'>Size</th><th style='width: 400px;'>File</th></tr>"
if [ $c -gt 0 ]                                                                                                              
then                                                                                                                         
	for r in $f
	do
		t=`stat -c%y ${LOG_PATH}/$r | sed 's/\.000000000//'`
		s=`stat -c%s ${LOG_PATH}/$r | awk '{ printf("%.02f kb", $1 / 1024) }'`
		r=`echo $r | sed 's/\.\///'`
		echo "<tr><td>$t</td><td>$s</td><td><a href='get_file.cgi?$r'>$r</a></td></tr>"
	done
else
	echo "<tr><td colspan='2' align='center'>None</td></tr>"
fi
echo '</table>'

# error logs
f=`( cd ${LOG_PATH}; find . -name report.\* ) | sort -r | xargs`
c=`echo $f | wc -w`

echo "<br/><br/><p style='border-bottom: 1px solid black;'>Error Logs</p><table>"
echo "<tr><th style='width: 180px;'>Date</th><th style='width: 100px;'>Size</th><th style='width: 400px;'>File</th></tr>"
if [ $c -gt 0 ]
then
	for r in $f
	do
		t=`stat -c%y ${LOG_PATH}/$r | sed 's/\.000000000//'`
		s=`stat -c%s ${LOG_PATH}/$r | awk '{ printf("%.02f kb", $1 / 1024) }'`
		r=`echo $r | sed 's/\.\///'`
		echo "<tr><td>$t</td><td>$s</td><td><a href='get_file.cgi?$r'>$r</a></td></tr>"
	done
else
	echo "<tr><td colspan='2' align='center'>None</td></tr>"
fi
echo '</table></body></html>'
