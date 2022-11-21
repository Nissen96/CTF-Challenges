<?php
session_start();
if (!isset($_SESSION["access"]) || !$_SESSION["access"]) {
    header("location: access.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
    <title> Vault </title>
</head>
<body>
    <h1> Super Secure Vault 9001 </h1>
    <br>
    <h2> Kun for CEO Lone Skum! </h2>
    <br>
    <h3> Secrets </h3>
    <ul>
        <li> CPR: 133773-4242</li>
        <li> Computer password: Winter1998 </li>
        <li> FB password:       letmein    </li>
        <li> Twitter password:  letmein    </li>
        <li> Bank password:     letmein    </li>
    </ul>
    <h3> Dokumenter </h3>
    <ul>
        <li><a href="https://www.arla.dk/opskrifter/frikadeller/">
            Min egen personlige hemmelige opskrift på hjemmelavede frikadunser
        </a></li>
        <li><a href="skolefoto86.jpg">Skolefoto 1986</a></li>
        <li><a href="fortrolig.pdf">FORTROLIG</a></li>
        <li><a href="navne.txt">Mulige navne til kommende bebs</a></li>
    </ul>
    <button onclick="location.href='/lock.php'">Lås Vault</button>
</body>
</html>
