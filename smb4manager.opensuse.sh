#! /bin/sh
#
# Author: Nilton OS
# Starts the SMB4MANAGER Daemon on OpenSUSE 12.2
#
# To execute automatically at startup
# cp /opt/smb4manager/smb4manager.opensuse.sh /etc/init.d/smb4manager
# chmod +x /etc/init.d/smb4manager
# chkconfig --add smb4manager
# systemctl --system daemon-reload
#
# and symbolic its link
# ln -s /etc/init.d/smb4manager /usr/sbin/rcsmb4manager
# /usr/sbin/rcsmb4manager
#
### BEGIN INIT INFO
# Provides: smb4manager
# Required-Start: $network $remote_fs
# Required-Stop: $network $remote_fs
# Default-Start: 3 5
# Default-Stop: 0 1 2 6
# Description: Start the smb4manager daemon
### END INIT INFO

PYTHON="python"
WEB2PY_DIR="/opt/smb4manager"
WEB2PY_PIDFILE="/var/run/smb4manager.pid"
WEB2PY_DESC="SMB4MANAGER"

WEB2PY_ADMINPASS="smb4manager"
WEB2PY_IP="0.0.0.0"
WEB2PY_PORT="8010"

## Add config SSL
WEB2PY_SSL="-c $WEB2PY_DIR/ssl/server.crt -k $WEB2PY_DIR/ssl/server.key"

WEB2PY_OPTS="-Q --nogui $WEB2PY_SSL -a $WEB2PY_ADMINPASS -d $WEB2PY_PIDFILE -i $WEB2PY_IP -p $WEB2PY_PORT"


. /etc/rc.status

# Shell functions sourced from /etc/rc.status:
#      rc_check         check and set local and overall rc status
#      rc_status        check and set local and overall rc status
#      rc_status -v     ditto but be verbose in local rc status
#      rc_status -v -r  ditto and clear the local rc status
#      rc_failed        set local and overall rc status to failed
#      rc_reset         clear local rc status (overall remains)
#      rc_exit          exit appropriate to overall rc status

# First reset status of this service
rc_reset

case "$1" in
    start)
	echo -n "Starting $WEB2PY_DESC daemon"

	$PYTHON $WEB2PY_DIR/web2py.py $WEB2PY_OPTS &

	# Remember status and be verbose
	rc_status -v
	;;
    stop)
	echo -n "Shutting down $WEB2PY_DESC daemon"

	killproc -p $WEB2PY_PIDFILE -TERM $PYTHON

	# Remember status and be verbose
	rc_status -v
	;;
    restart)
        ## Stop the service and regardless of whether it was
        ## running or not, start it again.
        $0 stop
        $0 start

        # Remember status and be quiet
        rc_status
        ;;
    status)
	echo -n "Checking for service $WEB2PY_DESC "

        # Status has a slightly different for the status command:
        # 0 - service running
        # 1 - service dead, but /var/run/  pid  file exists
        # 2 - service dead, but /var/lock/ lock file exists
        # 3 - service not running

	checkproc -p $WEB2PY_PIDFILE $PYTHON

	rc_status -v
	;;
    *)
	echo "Usage: $0 {start|stop|status}"
	exit 1
	;;
esac
rc_exit
