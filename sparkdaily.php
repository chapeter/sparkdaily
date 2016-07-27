<?php
$sparkaccesstoken="";
$sparkroomid="Y2lzY29zcGFyazovL3VzL1JPT00vNzA5MGNmMzAtOTdhMy0xMWU1LWIyNzAtZDM2ZWRmMzJlODMz";

date_default_timezone_set("America/Chicago");

$messagedata = GetRoomMessages($sparkaccesstoken, $sparkroomid);
$messagefull = GetHeader($strtitle) . $messagedata . GetFooter();
file_put_contents("daily.html", $messagefull);

function GetRoomMessages($token,$rid) {
$rettext = "";
$arr_users = array();
//Use Spark API to get List of Messages
$arr_ret = DoGet("https://api.ciscospark.com/v1/messages?roomId=$rid&max=3$beforemsg","","","Authorization: Bearer $token");
$retbody = $arr_ret[0];
$arr_mess = json_decode($retbody, true);
if(count($arr_mess["items"]) <= 0) { break; }

for($y=0;$y<count($arr_mess["items"]);$y++) {
$currentdate = date("Y-m-d");
$msgcre = $arr_mess["items"][$y]["created"];
$messagedate = gmdate('Y-m-d', strtotime($msgcre));
if($currentdate==$messagedate) {
$msgid = $arr_mess["items"][$y]["id"];
$msgtext = $arr_mess["items"][$y]["text"];
$msghtml = $arr_mess["items"][$y]["html"];
if($msghtml=="") { $msgoutput = $msgtext; } else { $msgoutput = $msghtml; }
$msgfrom = $arr_mess["items"][$y]["personId"];
$msgeml = $arr_mess["items"][$y]["personEmail"];
$userdname = $msgeml;
//Get Display Name from User ID
if(array_key_exists($msgfrom, $arr_users)) {
$msgfromname = $arr_users[$msgfrom];
} else {
$arr_name = DoGet("https://api.ciscospark.com/v1/people/$msgfrom","","","Authorization: Bearer $token");
$retuser = $arr_name[0];
$arr_user = json_decode($retuser, true);
$msgfromname = $arr_user["displayName"];
}
echo "DEBUG. sparkdaily. Message: =[$msgtext]=.\n";

$rettext .= GetBody($msgeml, $msgfromname, $msgcre, $msgoutput);
}
}
return $rettext;
}




function DoGet($strURL, $credentials, $cookie, $rawauth) {
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $strURL);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_ANY);
curl_setopt($ch, CURLOPT_USERPWD, base64_decode($credentials));

$headers = array($rawauth
);

if($cookie!="") { array_push($headers,"Cookie: ".$cookie); }

curl_setopt($ch, CURLOPT_HEADER, 1);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

$data = curl_exec($ch);
$header_size=curl_getinfo($ch,CURLINFO_HEADER_SIZE);
$header=trim(substr($data,0,$header_size)); //Get the header and trim it to remove \r\n
$body=substr($data,$header_size); //Get the body
$ret = array($body,$header);

curl_close($ch);

return $ret;
}

function GetHeader($strtitle) {
$ret = "";
$ret .= "<html>\n";
$ret .= "<head>\n";
$ret .= "<title>$strtitle</title>\n";
$ret .= "<table width=\"100%\">\n";
$ret .= "<tr valign=\"baseline\">\n";
$ret .= "<td align=\"left\"><div class=\"msgSubject\">\n";
$ret .= "<h2>$strtitle</h2>\n";
$ret .= "</div></td>\n";
$ret .= "</tr>\n";
$ret .= "</table>\n";

return $ret;
}

function GetBody($useremail, $userfullname, $messagedate, $messagebody) {
$ret .= "<div class=\"msgHead\">\n";
$ret .= "<!--X-Subject-Header-End-->\n";
$ret .= "<!--X-Head-of-Message-->\n";
$ret .= "<table class=\"msgHeadTbl\" width=\"100%\"\n>";
$ret .= "<tr valign=\"baseline\">\n";
$ret .= "<th align=\"left\">\n";
$ret .= "<strong>Date</strong>:&nbsp;</th>\n";
$ret .= "<td align=\"left\" width=\"100%\">\n";
$ret .= $messagedate . "</td>\n";
$ret .= "</tr>\n";
$ret .= "\n";
$ret .= "<tr valign=\"baseline\">\n";
$ret .= "<th align=\"left\">\n";
$ret .= "<strong>From</strong>:&nbsp;</th>\n";
$ret .= "<td align=\"left\" width=\"100%\">\n";
$ret .= "<a href=\"mailto:$useremail\">$useremail</a> (\"$userfullname\")</td>\n";
$ret .= "</tr>\n";
$ret .= "\n";
$ret .= "</table>\n";
$ret .= "<!--X-Head-of-Message-End-->\n";
$ret .= "<!--X-Head-Body-Sep-Begin-->\n";
$ret .= "</div>\n";
$ret .= "<div class=\"msgBody\">\n";
$ret .= "<table class=\"msgBodyTbl\" cellspacing=\"1\" width=\"100%\"><tr><td>\n";
$ret .= "<!--X-Head-Body-Sep-End-->\n";
$ret .= "<!--X-Body-of-Message-->\n";
$ret .= "<pre style=\"margin: 0em;\">$messagebody</pre>\n";
$ret .= "<!--X-Body-of-Message-End-->\n";
$ret .= "<!--X-MsgBody-End-->\n";
$ret .= "<!--X-Follow-Ups-->\n";
$ret .= "\n";
$ret .= "</td></tr></table>\n";
$ret .= "<!--/mha-cisco:msgdata-->\n";
$ret .= "<hr></div>\n";
return $ret;
}

function GetFooter() {
$ret = "";
$ret .= "</body>\n";
$ret .= "</html>\n";
return $ret;
}
?>



	Josh Anderson
Systems Engineer

7400 College Blvd, Suite 400
Overland Park, KS, 66210
United States

Email Me: joshand@cisco.com
Video Call Me: joshand@cisco.com
Call Me: +1 913 323 5606
Browser-Based Video Call: JabberGuest
Join My Meeting Room
Video:
joshand@acecloud.webex.com  | 204 219 571

WebEx:
https://acecloud.webex.com/meet/joshand | 204 219 571