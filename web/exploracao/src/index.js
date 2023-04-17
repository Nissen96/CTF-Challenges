botoesIni = [
{
        "img":"imagens/openlayers.png",
        "href": location.href.replace("init/index.php"+window.location.search,"") + customDir + "/ol.php",
        "titulo":$trad(4,g_traducao_init),
        "subtitulo": $trad("4a",g_traducao_init),
        "fa": "map-o",
        "target": "_blank"
},{
        "img":"imagens/osm.png",
        "href": location.href.replace("init/index.php"+window.location.search,"") + customDir + "/osm.php",
        "titulo":$trad(23,g_traducao_init),
        "subtitulo": $trad("23a",g_traducao_init),
        "fa": "map-o",
        "target": "_blank"
},{
        "img":"imagens/window-duplicate.png",
        "href": "../mapas/index.php",
        "titulo":$trad(34,g_traducao_init),
        "subtitulo": $trad("34a",g_traducao_init),
        "fa": "map-o",
        "target": "_self"
},{
        "img":"imagens/psymap.png",
        "href": "../flag.php",
        "titulo":"Flag",
        "subtitulo":"Flags of the world - and DDC",
        "fa": "flag",
        "target": "_self"
},{
        "img":"imagens/ogc_logo.png",
        "href": "../ogc/index.php",
        "titulo":$trad(11,g_traducao_init),
        "subtitulo": $trad("11a",g_traducao_init),
        "fa": "download",
        "target": "_self"
},{
        "img":"imagens/application-vnd-google-earth-kml.png",
        "href": "../kml.php?tipoxml=kml",
        "titulo":$trad(12,g_traducao_init),
        "subtitulo": $trad("12a",g_traducao_init),
        "fa": "download",
        "target": "_self"
},{
        "img":"imagens/openlayersdebug.png",
        "href": location.href.replace("init/index.php"+window.location.search,"") +  customDir + "/openlayersdebug.php",
        "titulo":$trad(5,g_traducao_init),
        "subtitulo": $trad("5a",g_traducao_init),
        "fa": "cogs",
        "target": "_blank"
},{
        "img":"imagens/certificate-server.png",
        "href": "../testainstal/index.php",
        "titulo":$trad(2,g_traducao_init),
        "subtitulo": $trad("2a",g_traducao_init),
        "fa": "cogs",
        "target": "_self"
},{
        "img":"imagens/applications-development-web.png",
        "href": "../admin/index.php",
        "titulo":$trad(3,g_traducao_init),
        "subtitulo": $trad("3a",g_traducao_init),
        "fa": "cogs",
        "target": "_self"
},{
        "img":"imagens/applications-development.png",
        "href": "../utilitarios/index.php",
        "titulo":$trad(33,g_traducao_init),
        "subtitulo": $trad("33a",g_traducao_init),
        "fa": "cogs",
        "target": "_self"
}
];
reordenaBotoesPorFavoritos();
//TODO um dia, remover as imagens da pasta init e deixar apenas as da pasta init/imagens
function mostraBotoesBT(men){
        var html = "";
        //menu
        html = Mustache.to_html(
                        $("#menuTpl").html(),
                        i3GEO.idioma.objetoIdioma(g_traducao_init)
        );
        $("#menuTpl").html(html);
        //
        $("#mensagemLogin").html(men);
        html = Mustache.to_html(
                        $("#jumbotron").html(),
                        {
                                "jumbotron" : $trad(35,g_traducao_init),
                                "host" : location.host,
                                "href" : location.href
                        }
        );
        $("#jumbotron").html(html);
        i3GEO.configura = {"locaplic" : ".."};
        html = Mustache.to_html(
                        "{{#d}}" + $("#botoesTpl_template").html() + "{{/d}}",
                        {"d":botoesIni,"abrir" : $trad(36,g_traducao_init)}
        );
        $("#botoesTpl").html(html);
        aplicaFavoritos();
}
function findBootstrapDeviceSize() {
        var dsize = ['lg', 'md', 'sm', 'xs'];
        for (var i = dsize.length - 1; i >= 0; i--) {

                // Need to add &nbsp; for Chrome. Works fine in Firefox/Safari/Opera without it.
                // Chrome seem to have an issue with empty div's
                $el = $('<div id="sizeTest" class="hidden-'+dsize[i]+'">&nbsp;</div>');
                $el.appendTo($('body'));

                if ($el.is(':hidden')) {
                        $el.remove();
                        return dsize[i];
                }
        }
        return 'unknown';
}
//cookies sao armazenados em favoritosInit
function favorita(obj){
        $(obj).find("span").toggleClass("amarelo");
        //
        //modifica os cookies
        //
        var cookies = [];
        $(".amarelo").each(
                        function(i,el){
                                cookies.push($(el).attr("data-cookie"));
                        }
        );
        i3GEO.util.insereCookie("favoritosInit",cookies.join("|"),200);
}
function aplicaFavoritos(){
        var favoritos = i3GEO.util.pegaCookie("favoritosInit");
        if(favoritos){
                favoritos = favoritos.split("|");
                $(favoritos).each(
                                function(i,el){
                                        $('span[data-cookie="'+el+'"]').toggleClass("amarelo");
                                }
                );
        }
}
function reordenaBotoesPorFavoritos(){
        var f = [],
        nf = [],
        favoritos = i3GEO.util.pegaCookie("favoritosInit");
        $(botoesIni).each(
                function(i,el){
                        el.href = el.href.replace("#topo","");
                }
        );
        if(favoritos){
                favoritos = favoritos.split("|");
                $(botoesIni).each(
                                function(i,el){
                                        if(jQuery.inArray(el.img,favoritos) >= 0){
                                                f.push(el);
                                        }
                                        else{
                                                nf.push(el);
                                        }
                                }
                );
                botoesIni = jQuery.merge( f, nf );
        }
}