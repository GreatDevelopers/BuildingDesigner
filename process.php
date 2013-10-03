<?php
//process.php
$username = $_POST['name'];
$heightspan = $_POST['heightspan'];
$lengthspan = $_POST['lengthspan'];
$widthspan = $_POST['widthspan'];
$colrad = $_POST['colrad'];
$collength = $_POST['collength'];
$colwidth = $_POST['colwidth'];
$depthofbeam = $_POST['depthofbeam'];
$widthofbeam = $_POST['widthofbeam'];
$slabthickness = $_POST['slabthickness'];
$pinthheight = $_POST['pinthheight'];
$foundationheight = $_POST['foundationheight'];
$foundationnodes = $_POST['foundationnodes'];
$materialforbeam = $_POST['materialforbeam'];
$materialforcolumn = $_POST['materialforcolumn'];
$ix = $_POST['ix'];
$iz = $_POST['iz'];
$iy = $_POST['iy'];
$j = $_POST['j'];
$g = $_POST['g'];
$wslloaddir = $_POST['wslloaddir'];
$lslloaddir = $_POST['lslloaddir'];

$e = $_POST['e'];
$a = $_POST['a'];
$colix = $_POST['colix'];
$cole = $_POST['cole'];
$cola = $_POST['cola'];

$lengthwiseweight = $_POST['lengthwiseweight'];
$widthwiseweight = $_POST['widthwiseweight'];


if($colrad==='')
{
	$coltype = 1;
	$colrad = 0;	
}
else
{
	$coltype = 0;
	$collength = 0;
	$colwidth = 0;

}

$fp = fopen('config.py', 'w+');

$string = "dep_of_foun=".$foundationheight." \n\n"."plinth_lev=".$pinthheight." \n\n"."clearh=\"". $heightspan."\" \n\n"."dep_slab=".$slabthickness." \n\n"."rep_span_len=\"".$lengthspan."\"\n\n"."rep_span_wid=\"".$widthspan."\" \n\n"."col_type=".$coltype." \n\n"."len_col=".$collength." \n\n"."wid_col=".$colwidth." \n\n"."radius_col=".$colrad." \n\n"."dep_beam=".$depthofbeam." \n\n"."wid_beam=".$widthofbeam." \n\n"."foundationnodes = \"".$foundationnodes."\"\n\nmaterialforbeam=\"".$materialforbeam."\"\n\nmaterialforcolumn=\"".$materialforcolumn."\"\n\nix=\"".$ix."\"\n\niy=\"".$iy."\"\n\niz=\"".$iz."\"\n\ng=\"".$g."\"\n\nj=\"".$j."\"\n\nlslloaddir=\"".$lslloaddir."\"\n\nwslloaddir=\"".$wslloaddir."\"\n\na=\"".$a."\"\n\ne=\"".$e."\"\n\ncolix=\"".$colix."\"\n\ncole=\"".$cole."\"\n\ncola=\"".$cola."\"\n\nlengthwiseweight=\"".$lengthwiseweight."\"\n\nwidthwiseweight=\"".$widthwiseweight."\"\n\n";
//$rmdata = "rm *.g ; rm *.flt ; rm *.txt ; rm *.anl ";
//echo exec($rmdata);

// Writing data to file
fwrite($fp, $string);

// Building making file executed
$command1 = './build.py ' . $username;
$command2 = './shell ' . $username;
exec($command1);
// Mged raytracing
#echo $command2;
exec($command2);
#exec('./shell Gagan');
#exec("./shell");
// Output page
echo '<META http-equiv="refresh" content=";URL=completed.php?name='.$username. '">';

?>
