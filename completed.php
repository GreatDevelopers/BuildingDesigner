<html>
<head>
	<title>BRL-CAD at your service</title>
	<link href="formlayout.css" media="screen" rel="stylesheet" type="text/css" />
</head>
<body>
<center>
<?php $name = $_GET['name']; ?>
<h1>BRL-CAD at your service</h1>
<table border = 1 cellpadding = 5 bordercolor = "black">
<tr><td>Felt Input File</td><td><a href = "outputs/output_<?php echo $name; ?>/felt_<?php echo $name; ?>.flt">Download</a></td></tr>
<tr><td>Felt Analysis</td><td><a href = "outputs/output_<?php echo $name; ?>/analysis_<?php echo $name; ?>.txt">Download</a></td></tr>
<tr><td>Staad Pro Input File</td><td><a href = "outputs/output_<?php echo $name; ?>/stad_<?php echo $name; ?>.anl">Download</a></td></tr>
<tr><td>BRL-CAD Input File</td><td><a href = "outputs/output_<?php echo $name; ?>/work_<?php echo $name; ?>.txt">Download</a></td></tr>
<tr><td>BRL-CAD Database File</td><td><a href = "outputs/output_<?php echo $name; ?>/database_<?php echo $name; ?>.g">Download</a></td></tr>
</table>
<table>
<tr><td>
	<img src="outputs/output_<?php echo $name; ?>/images/iso.png">
	</td><td>
	<img src="outputs/output_<?php echo $name; ?>/images/side.png">
</td></tr>
<tr><td>
	Isometric View
	</td><td>
	Elevation along length
</td></tr>
<tr><td>
	<img src="outputs/output_<?php echo $name; ?>/images/front.png">
	</td><td>
	<img src="outputs/output_<?php echo $name; ?>/images/top.png">

</td></tr>
<tr><td>
	Elevation along width (Showing section)
	</td><td>
	Top View
</td></tr>
</table></center>

</body>
</html>
