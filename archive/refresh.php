<?php
$sf_temperature      = todays_temperature_in_city("San+Francisco,CA");
$oakland_temperature = todays_temperature_in_city("Oakland,CA");

$cold_ass_cities[]="Minneapolis,MN";
$cold_ass_cities[]="Fargo,ND";
$cold_ass_cities[]="Laramie,WY";
$cold_ass_cities[]="Wasilla,AK";

$index=array_rand($cold_ass_cities,1);
$random_cold_ass_city=$cold_ass_cities[$index];

if( $oakland_temperature and $sf_temperature ) {
    if( $oakland_temperature > $sf_temperature ) {
        $temperature_delta = abs($oakland_temperature - $sf_temperature);
	$text_blurb = "Oakland is $temperature_delta degrees warmer than San Francisco today.";
    }
    else {
	$random_cold_ass_temperature=todays_temperature_in_city($random_cold_ass_city);
	if( $oakland_temperature > $random_cold_ass_temperature ) {
            $temperature_delta = abs($oakland_temperature - $random_cold_ass_temperature);
            $text_blurb = "Oakland is $temperature_delta degrees warmer than $random_cold_ass_city today.";
        } else {
            exit();
        }
    }
} else {
    echo "REFRESH.PHP FAILED, NO TEMPERATURE FOUND";
    exit();
} 

function todays_temperature_in_city($city) {
    $client_id='kwgBnQPUcVT53PXDHGOWT';
    $client_secret='7oPdeudzKtd6nrcPRt6s3UTszeIUfccR6eQwATnN';

    $response = file_get_contents("http://api.aerisapi.com/observations/$city?client_id=$client_id&client_secret=$client_secret");
    $json = json_decode($response);
    if ($json->success == true) {
        // create reference to our returned observation object
        $ob = $json->response->ob;
        //echo sprintf("The current weather in Seattle is %s with a temperature of %d.", strtolower($ob->weather), $ob->tempF);
        return $ob->tempF;
    }
    else {
        echo sprintf("An error occurred: %s", $json->error->description);
    }
}

$content = <<<END
<html xmlns="http://www.w3.org/1999/xhtml" id="foo" class="bar">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> 
    <title>FUCK YEAH OAKLAND</title><meta name="description" content=""/> 
    <style type="text/css">
        @import url("fuckyeah.css");
    </style>
  </head>
  <body>
  <h1>$text_blurb</h1>
  <h3>
  [also, it has <a href="http://maps.google.com/maps/ms?ie=UTF8&hl=en&msa=0&msid=111386974984487942660.00043b9b4dc191c072885&om=0&ll=37.784554,-122.23526&spn=0.086556,0.194664&z=12">better tacos.</a>]
  </h3>
  </body>
</html>
END;

$handle = fopen("/home/fuckyeahoakland/fuckyeahoakland.com/index.html", "w");
fwrite($handle, $content);
fclose($handle);

