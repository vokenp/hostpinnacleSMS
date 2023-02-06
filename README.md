<p align="center">
  Send SMS Message Via Host Pinnacle 
</p>
<p align="center">
</p>
##Prequisets 
* pip install pymysql
* pip install python-decouple
* pip install requests


##Create a .env File and Add the Following
<pre>
DB_CONNECTION=mysql
DB_HOST=localhost
DB_DATABASE=hostpinsms
DB_USERNAME=root
DB_PASSWORD=???

HPApiKey = ??
HPUserID = ??
HPPassword = ??
HPSenderID = HPKSMS
smsLength = 160
</pre>

##Run the following Create Table Scripts in your Database
<pre>
DROP TABLE IF EXISTS `sms_outbox_hostpins`;
CREATE TABLE `sms_outbox_hostpins` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_by` varchar(255) DEFAULT NULL,
  `msgid` varchar(255) DEFAULT NULL,
  `send_status` varchar(255) NOT NULL DEFAULT 'pending',
  `response_message` varchar(255) DEFAULT NULL,
  `short_code` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `message` text,
  `transactionId` varchar(255) DEFAULT NULL,
  `sms_units` int DEFAULT NULL,
  `sms_length` int DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `statusCode` varchar(255) DEFAULT NULL,
  `deliveryTime` timestamp NULL DEFAULT NULL,
  `deliveryStatus` varchar(255) DEFAULT 'DELIVERED',
  `sms_balance_onsend` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `msgid` (`msgid`)
) ;
</pre>

##Run the main.py