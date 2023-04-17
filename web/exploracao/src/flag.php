<?php
define("ONDEI3GEO", ".");
include "ms_configura.php";
include "./init/head.php";
?>

<body style="padding-top: 90px;" id="topo">
    <nav class="navbar navbar-default navbar-fixed-top">
        <div class="container-fluid">
            <div class="navbar-header">
                <button type="button" title="icon-bar" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                    <span class="sr-only"></span> <span class="icon-bar"></span> <span class="icon-bar"></span> <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" onclick="$('.cartao').fadeIn(600);" href="./init/index.php">
                    <span class="material-icons md-18">home</span> <?php echo $mensagemInicia;?>
                </a>
            </div>
            <div id="navbar" class="navbar-collapse collapse navbar-responsive-collapse">

            </div>
        </div>
    </nav>

    <!-- FLAG -->
    <div class="container-fluid row center-block;" style="width:100%" id="conteudoPrincipal" tabindex="-1">
        <div class="row center-block text-center" style="max-width:1000px">
            <?php
            if ($_SESSION["usuario"] === "administrador") {
                echo "<h2>DDC{1nclu54o_d3_4rqu1v0_l0c4l}</h2>";
            } else {
                echo "<h2>Flag is only visible to admin user</h2>";
            }
            ?>
        </div>
    </div>

    <div tabindex="-1" class="navbar-fixed-bottom container-fluid" style="background-color: #fff; margin-top: 10px; padding-top: 10px;">
        <div class="row text-center">
            <div class="col-lg-12 center-block">
                <a tabindex="-1" rel="license" href="http://creativecommons.org/licenses/GPL/2.0/legalcode.pt" target="_blank">
                    <img alt="Licen&ccedil;a Creative Commons" style="border-width: 0" src="https://i.creativecommons.org/l/GPL/2.0/88x62.png" />
                </a>
                <br />O i3Geo est&aacute; licenciado com uma Licen&ccedil;a
                <a tabindex="-1" rel="license" href="http://creativecommons.org/licenses/GPL/2.0/legalcode.pt" target="_blank">Creative Commons - Licen&ccedil;a P&uacute;blica
                    Geral GNU (&#34;GNU General Public License&#34;)</a>
            </div>
        </div>
    </div>
</body>
</html>
