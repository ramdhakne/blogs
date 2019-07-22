var couchbase = require('couchbase')
var cluster = new couchbase.Cluster('couchbases://cb-gke-demo-0000.cb-gke-demo.sewestus.com?certpath=./ca.crt');
cluster.authenticate('Administrator', 'password');
var bucket = cluster.openBucket('default');
var N1qlQuery = couchbase.N1qlQuery;
bucket.operationTimeout = 100000;

console.log("Start upserting now...")
bucket.upsert('cip_request_id_874', {
                  "_id": "cip_request_id_873",
                  "doc_type": "user",
                  "requestId": "873",
                  "clientId": "68136",
                  "inputFeedType": "Baby",
                  "pipelineState": "RESPONSE_COMPLETE",
                  "feedStatus": "INCOMPLETE",
                  "feedFormat": "JSON",
                  "jobParams": "Inventore aliquam at quae molestiae qui qui voluptate qui voluptate. Harum dolores dolor minus provident impedit ea ut. Aut sint et non eum qui omnis excepturi magni ea. Autem hic magnam cum suscipit reiciendis suscipit. Et cum ipsa eius asperiores expedita temporibus voluptatem qui. Eum explicabo dolore voluptas illum quas odio dignissimos.",
                  "activeConfigSpecPath": "Veritatis et saepe quibusdam consequatur expedita ipsam.",
                  "creationDate": 1520417238660,
                  "lastModifiedDate": 1527661013485,
                  "fileSize": "97213",
                  "recordCount": "56754",
                  "failrecordCount": "54169",
                  "successrecordCount": "18513",
                  "type": "CIP_REQUEST_ID",
                  "mode": null,
                  "machineIp": "55.108.142.104"
                }, function(err, result) {
if (err) throw err;
 
bucket.get('cip_request_id_874', function(err, result) {
  if (err) throw err;
})
    console.log('Success!', result)
})
console.log("Done upserting!!!")
// Success!
//process.exit(0);
