
<?php
#www-data         //使用的时候注意用户不一定是www-data，根据实际情况来
system("kill `ps aux | grep www-data | awk '{print $2}' | xargs kill -9`");

#php-fpm        //杀php-fpm进程

system("kill `ps -ef | grep php-fpm | grep -v grep | awk '{print $2}'`");

#php-apache     //杀httpd进程

system("kill `ps -ef | grep httpd | grep -v grep | awk '{print $2}'`");
?>