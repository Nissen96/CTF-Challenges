<?php
$invalid_key = false;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    if ($_POST["key"] === "Sup3r_51kk3r_nøgl3_du_4ldr1g_gæ7t3r...håb3r_j3G") {
        session_start();
        $_SESSION["access"] = true;
        header("location: vault.php");
    } else {
        $invalid_key = true;
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Vault Access</title>
</head>
<body>
    <h2>VAULT ACCESS</h2><br>
    <div>
        <?php
            if ($invalid_key) {
                echo "<b style='color: red'>Ugyldig master key!</b><br><br>";
            }
        ?>
        <form method="post" action="">
            <label for="key"><b>Master Key:</b></label>
            <input type="password" name="key" id="key">
            <br><br>
            <input type="submit" value="Access">
        </form>
    </div>
</body>
</html>
