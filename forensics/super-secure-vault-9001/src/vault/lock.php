<?php
    session_start();
    $_SESSION["access"] = false;
    header("Location: access.php");
?>
