<?php
require('connect_db.php');
$input = explode(',', $_GET['info']);
$q = "SELECT * FROM locationMapping WHERE name = '$input[0]'";
$r = @mysqli_query($dbc, $q);
if (mysqli_num_rows($r) > 0) {
        $q = "UPDATE locationMapping SET GPS='$input[1]', datetime=NOW() WHERE name = '$input[0]'";
        $r = @mysqli_query($dbc, $q);
}
else {
$q = "INSERT INTO locationMapping (name, GPS, datetime) VALUES ('$input[0]', '$input[1]', NOW() )";
$r = @mysqli_query($dbc, $q);
}
$q = "SELECT * FROM locationMapping";
$r = @mysqli_query($dbc, $q);
$s = '';
while ($row = mysqli_fetch_array($r, MYSQLI_ASSOC)) {
        $s .= $row['name'].','.$row['GPS'].','.$row['datetime'].';';
}
echo $s;
mysqli_close($dbc);
?>
