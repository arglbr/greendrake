<?php
/*
// Abre o arquivo

funcao buscaCategoria(p_categ = null) {
    busca o historico na lista de categorias

    se encontrar
        categoria = categoria encontrada
    senao
        categoria = ask user
    fim-se

    return (categoria is set?) ? categoria : null;
}

i = 0;

para cada linha, a partir da linha 3
    # Data;Historico;Docto.;Credito (R$);Debito (R$);Saldo (R$);
    data[i]['mov_id']       = uuid();
    data[i]['mov_data']     = converte a data para iso-8601;
    data[i]['mov_categ']    = buscaCategoria();
    data[i]['mov_bankdesc'] = historico;
    data[i]['mov_bankid']   = docto;
    data[i]['mov_value']    = (credito is set) ? credito : debito * -1;
fim-para

save the array as csv

*/
ini_set('auto_detect_line_endings', TRUE);
$datafile = $argv[1];
$i        = 0;
$table    = array();

function buscaCategoria($p_categ = null) {
    return 'nova_categoria';
}

if (($handle = fopen($datafile, "r")) !== FALSE) {
    while (($data = fgetcsv($handle, 1000, ";")) !== FALSE) {
        # Data;Historico;Docto.;Credito (R$);Debito (R$);Saldo (R$);

        /*
        $num = count($data);
        echo "<p> $num campos na linha $row: <br /></p>\n";
        $row++;

        for ($c = 0; $c < $num; $c++) {
            echo $data[$c] . "<br />\n";
        }
        */

        // Just from the 3rd line
        if ($i > 2) {
            $date = DateTime::createFromFormat('d/m/y', $data[0]);

            if ($date !== FALSE) {
                $table[$i]['mov_id']       = md5(uniqid(rand(), true));
                $table[$i]['mov_data']     = $date->format('Y-m-d');
                $table[$i]['mov_categ']    = buscaCategoria($data[1]);
                $table[$i]['mov_bankdesc'] = $data[1];
                $table[$i]['mov_bankid']   = $data[2];
                $table[$i]['mov_value']    = (isset($data[3])) ? floatval($data[3]) : floatval($data[4]) * -1;    
            }
        }

        $i++;
    }

    fclose($handle);
}

unset($datafile, $i);
print print_r($table, true);