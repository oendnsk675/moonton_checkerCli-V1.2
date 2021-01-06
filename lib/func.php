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
// $namaFile2 = $combo;
// $file2 = fopen($namaFile2, "r");
// for ($x=0; $x < count(file($namaFile2)) ; $x++) { 
// 	$string2 = trim(fgets($file2));
// 	if ($string2 != "") {
// 		$file = fopen($namaFile2, "a");
// 		fwrite($file, "$string2\n");
// 		fclose($file);
// 	}
// }

?>