<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

#calls the python code from Homework assignment 3
#Returns an array where the first element is a message string,
#and the rest of the elements are the search results.
function search($query) {
	$command = escapeshellcmd('python3 /home/kem021/Info/Tokenizer/retrieve.py '.$query);
	$output = shell_exec($command);
	return  explode("\n", $output);	
}

#prints out an html list of the 10 results that correspond to the page number parameter
function list_results($results, $page){
	echo "<ol start=\"".(($page*10)+1)."\">";
	for($i = $page*10; $i < min(($page+1)*10, count($results)); $i++){
		if (trim($results[$i] != ''))
			echo "<li><span><a href=\"".$results[$i]."\">".$results[$i]."</a></span></li><br>";
	}
	echo "</ol>";

	#logic to determine if there should be a previous page button
	if ($page > 0) {
		echo "<button name=\"page\" value=\"".($page)."\"> Previous </button>";
	}

	#logic if there should be a next page button
	if ( ($page+1)*10+1 < count($results)) {
		echo "<button name=\"page\" value=\"".($page+2)."\"> Next </button>";
	}
}

#displays the search form
#$msg parameter is the first line from the python code output
#$results is the array that contains the search engine results
function displayHTML($msg, $results) {
?>

<html>
<head>
<title><?php echo isset($_GET['query']) ? $_GET['query'] : 'Search' ?></title>
</head>

<body>
    <h1>Welcome to Kyle Morley's Search Engine!</h1> <hr>

    <form method="get" action="search.php">
    <input type="text" name="query" value="<?php echo isset($_GET['query']) ? $_GET['query'] : '' ?>">
    <input type="hidden" name="page" value="1">
    <input type="submit" value="Search"><br><br>

    <?php echo  $msg;  ?><br><br>

    <?php 
	if (isset($_GET['query'])){

		if (!isset($_GET['page']) || $_GET['page'] < 1 ){
			list_results($results, 0);
		}
		else{
			list_results($results, $_GET['page']-1);
		}
	}

    ?>
</form>


</body>
</html>

<?php
}
?>

<?php

if (!session_start()){
	exit("Error: unable to start session.");
}
#displays the search results
elseif(isset($_GET['query'])){

	$query = $_GET['query'];

	#if a new query is entered, call the search function
	if($query != $_SESSION['previous_query']){
		$_SESSION['previous_query'] = $query;
		$_SESSION['output'] = search($query);
	}

	displayHTML($_SESSION['output'][0], array_slice($_SESSION['output'], 1));

}
#display the empty search page
else{
	if (session_status() == PHP_SESSION_NONE){
		session_start();
	}
	displayHTML("","");
	$_SESSION['previous_query'] = '';
	$_SESSION['output'];
}
?>
