<?php  
$combo = $argv[1];
function hapus($namaFile, $data){
	$namaFile = $namaFile;
	$getsdas = file_get_contents($namaFile);
	$replace =  str_replace("$data", '', $getsdas);
	file_put_contents($namaFile, $replace);
}

$namaFile = "trash/cache.txt";
$file = fopen($namaFile, "r");
for ($i=0; $i < count(file($namaFile)) ; $i++) { 
	$string = trim(fgets($file));
	if ($string != "") {
		// var_dump($string);
		hapus($combo, $string);
	}
	
}
file_put_contents($namaFile, "");

?>
