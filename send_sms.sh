#!/bin/sh 

clientid='9bfe6e75de825ca7808a6b97bede94e9'
clientsecret='5a3cb2fcf99353f7'
phonenumber="+14256153816"
message=$1

accesstoken=`curl https://api.att.com/oauth/token -H "Content-Type: application/x-www-form-urlencoded" -d "client_id=$clientid&client_secret=$clientsecret&grant_type=client_credentials&scope=SMS" | grep "access_token" | sed 's/^.*:"//' | sed 's/".*$//'`

payload="{ \"outboundSMSRequest\": { \"address\":  \"tel:$phonenumber\" , \"message\":\"$message\" }}"
echo "sending SMS"
echo $payload
curl https://api.att.com/sms/v3/messaging/outbox -X POST -H "Authorization: Bearer $accesstoken" -d "$payload" -H "Content-Type: application/json"

