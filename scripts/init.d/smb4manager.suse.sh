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

APP_ROOT="/opt/smb4manager"
NAME="SMB4Manager"
DESC="SMB4Manger service"


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
        echo -n "Starting $DESC daemon"
        cd $APP_ROOT
        ./runserver.py &
        # Remember status and be verbose
        rc_status -v
        ;;
    stop)
        echo -n "Shutting down $DESC daemon"
        PID=$(ps x | grep flask | head -n1 | awk '{ print $1 }')
        /bin/kill -9 $PID

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
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac
rc_exit

