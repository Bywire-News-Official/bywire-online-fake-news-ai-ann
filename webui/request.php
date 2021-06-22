<?php

function call_api($method, $url, $data = false) {
    $curl = curl_init();

    switch ($method)
    {
        case "POST":
            curl_setopt($curl, CURLOPT_POST, 1);

            if ($data)
                curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
            break;
        case "PUT":
            curl_setopt($curl, CURLOPT_PUT, 1);
            break;
        default:
            if ($data)
                $url = sprintf("%s?%s", $url, http_build_query($data));
    }

    // Optional Authentication:
    //curl_setopt($curl, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
    //curl_setopt($curl, CURLOPT_USERPWD, "username:password");

    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);

    $result = curl_exec($curl);

    curl_close($curl);

    return $result;
}

$action        = $_REQUEST["action"];
$data          = json_decode($_REQUEST["data"]);
//print_r($data);
//$server = "ec2-99-81-187-79.eu-west-1.compute.amazonaws.com:5055";
$server = "ec2-54-75-171-71.eu-west-1.compute.amazonaws.com:5055";
$routes = array("text"=>$server."/analyze/text",
		"ipfs"=>$server."/analyze/ipfs",
		"flag"=>$server."/analyze/flag",
		"query"=>$server."/analyze/query");
echo json_encode(call_api("POST", $routes[$action], $data));

?>