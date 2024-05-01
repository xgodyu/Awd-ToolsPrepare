<?php
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = './.shell.php';#发现的不死马文件名和路径
while (1){
    unlink($file);
    usleep(10000);#记住，一定要比不死马更快，但不要太小，如果机子撑不住就gg了
}
?>
