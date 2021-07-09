

## convert clickhouse's sql into openlookeng's sql

import json
def txt_to_json():
    with open("poc-ch.txt",'r') as file:
        content = file.readlines()
        i = 1
        all = {}
        for line in content:
            all['Q'+ str(i)] = line
            i += 1

    with open("poc-ch.json",'w') as file:
        content = json.dumps(all)
        file.write(content)



def change_sql(origin_sql):
    changed_sql = origin_sql.replace('toUnixTimestamp($time1)','to_unixtime(timestamp $time1)')
    changed_sql = changed_sql.replace('toUnixTimestamp($time2)','to_unixtime(timestamp $time2)')
    changed_sql = changed_sql.replace('toDateTime(common_recv_time) AS common_recv_time',"from_unixtime(common_recv_time,'UTC+8')")
    changed_sql = changed_sql.replace("notEmpty(http_url)","length(http_url)!= 0")
    changed_sql = changed_sql.replace("notEmpty(http_domain)","length(http_domain)!= 0")
    changed_sql = changed_sql.replace("notEmpty(common_l7_protocol)","length(common_l7_protocol)!= 0")
    changed_sql = changed_sql.replace("notEmpty(common_server_ip)","length(common_server_ip)!= 0")
    changed_sql = changed_sql.replace("notEmpty(http_domain)","length(http_domain)!= 0")
    changed_sql = changed_sql.replace("notEmpty(common_subscriber_id)","length(common_subscriber_id)!= 0")
    #changed_sql = changed_sql.replace("toUnixTimestamp(toDateTime(toStartOfInterval(toDateTime(common_recv_time),INTERVAL 5 MINUTE)))","floor(common_recv_time/300) * 300")
    changed_sql = changed_sql.replace("toUnixTimestamp(toDateTime(toStartOfInterval(toDateTime(common_recv_time),INTERVAL 5 MINUTE)))","cast(common_recv_time/300 as int) * 300")
    changed_sql = changed_sql.replace("`","\"")
    changed_sql = changed_sql.replace("toDateTime(intDiv(toUInt32(toDateTime(toDateTime(common_recv_time))),300)*300)","from_unixtime(cast(common_recv_time/300 as int) * 300,'UTC+8')")
    changed_sql = changed_sql.replace("toDateTime(intDiv(toUInt32(toDateTime(toDateTime(common_recv_time))),3600)*3600)","from_unixtime(cast(common_recv_time/3600 as int) * 3600,'UTC+8')")
    changed_sql = changed_sql.replace("ORDER BY toDateTime(common_recv_time)","ORDER BY common_recv_time")
    changed_sql = changed_sql.replace("common_recv_time >= toDateTime($time1) AND common_recv_time < toDateTime($time2)","common_recv_time >= to_unixtime(timestamp $time1) AND common_recv_time < to_unixtime(timestamp $time2)")
    changed_sql = changed_sql.replace("toDateTime(toUnixTimestamp(toDateTime(toStartOfInterval(toDateTime(common_recv_time),INTERVAL 30 SECOND))))","from_unixtime(cast(common_recv_time/30 as int) * 30,'UTC+8')")
    changed_sql = changed_sql.replace("toDateTime(cast(common_recv_time/300 as int) * 300)","from_unixtime(cast(common_recv_time/300 as int) * 300,'UTC+8')")
    changed_sql = changed_sql.replace("toDateTime(intDiv(toUInt32(toDateTime(toDateTime(common_recv_time))), 3600)*3600)","from_unixtime(cast(common_recv_time/3600 as int) * 3600,'UTC+8')")
    changed_sql = changed_sql.replace("toDateTime(common_recv_time)","from_unixtime(common_recv_time,'UTC+8')")
    changed_sql = changed_sql.replace("toDateTime($time2)","to_unixtime(timestamp $time2)")
    changed_sql = changed_sql.replace("toDateTime($time1)","to_unixtime(timestamp $time1)")
    changed_sql = changed_sql.replace("uniq(","approx_distinct(")
    changed_sql = changed_sql.replace("group by \"URI\"","group by http_url")
    changed_sql = changed_sql.replace("GROUP BY \"URL\" LIMIT 1048576","GROUP BY http_url LIMIT 1048576")
    changed_sql = changed_sql.replace("GROUP BY \"Http URL\" LIMIT 1048576","GROUP BY http_url LIMIT 1048576")
    changed_sql = changed_sql.replace("GROUP BY \"Domain\" LIMIT 1048576","GROUP BY http_domain LIMIT 1048576")
    changed_sql = changed_sql.replace("GROUP BY \"Http.Domain\" LIMIT 1048576","GROUP BY http_domain LIMIT 1048576")
    changed_sql = changed_sql.replace("GROUP BY stat_time ORDER BY","GROUP BY from_unixtime(cast(common_recv_time/30 as int) * 30,'UTC+8') ORDER BY")
    changed_sql = changed_sql.replace("GROUP BY \"Server Port\" LIMIT 1048576","GROUP BY common_server_port LIMIT 1048576")
    changed_sql = changed_sql.replace("GROUP BY stat_time","GROUP BY from_unixtime(cast(common_recv_time/300 as int) * 300,'UTC+8')")
    changed_sql = changed_sql.replace("GROUP BY \"Client IP\", \"SSL.SNI\" LIMIT 1048576","GROUP BY common_client_ip, ssl_sni LIMIT 1048576")
    #changed_sql = changed_sql.replace("GROUP BY stat_time ORDER BY stat_time ASC LIMIT 10000","GROUP BY from_unixtime(cast(common_recv_time/30 as int) * 30,'UTC+8') ORDER BY stat_time ASC LIMIT 10000")
    changed_sql = changed_sql.replace("GROUP BY \"Sled IP\", \"Internal IP\" LIMIT 1048576","GROUP BY common_sled_ip, common_internal_ip LIMIT 1048576")
    changed_sql = changed_sql.replace("GROUP BY \"Server ASN\", \"Client ASN\" LIMIT 1048576","GROUP BY common_server_asn, common_client_asn LIMIT 1048576")
    changed_sql = changed_sql.replace("GROUP BY \"device_id\" ORDER BY \"Bytes\" DESC LIMIT 1048576","GROUP BY common_device_id ORDER BY \"Bytes\" DESC LIMIT 1048576")
    changed_sql = changed_sql.replace("GROUP BY \"Http.Domain\" ORDER BY \"Client IP\" DESC LIMIT 1048576","GROUP BY http_domain ORDER BY \"Client IP\" DESC LIMIT 1048576")
    changed_sql = changed_sql.replace("GROUP BY \"Sled IP\", \"External IP\", \"Internal IP\" LIMIT 1048576","GROUP BY common_sled_ip, common_external_ip ,common_internal_ip LIMIT 1048576")
    changed_sql = changed_sql.replace("GROUP BY \"Http.Domain\", \"Subscriber ID\" ORDER BY \"Sessions\" DESC LIMIT 1048576","GROUP BY http_domain, common_subscriber_id ORDER BY \"Sessions\" DESC LIMIT 1048576")
    changed_sql = changed_sql.replace("GROUP BY \"source\" ORDER BY \"Sessions\" DESC LIMIT 1048576)","GROUP BY coalesce(nullif(common_subscriber_id, ''), nullif(common_client_ip, '')) ORDER BY \"Sessions\" DESC LIMIT 1048576)")
    changed_sql = changed_sql.replace("GROUP BY \"destination\" ORDER BY \"Sessions\" DESC LIMIT 1048576)","GROUP BY coalesce(nullif(http_domain, ''), nullif(common_server_ip, '')) ORDER BY \"Sessions\" DESC LIMIT 1048576)")
    changed_sql = changed_sql.replace("GROUP BY \"server_ip\" ORDER BY \"Bytes\" desc )","GROUP BY common_server_ip ORDER BY \"Bytes\" desc )")
    changed_sql = changed_sql.replace("LIMIT 0,30","LIMIT 30")
    changed_sql = changed_sql.replace("GROUP BY \"domain\" ORDER BY \"Bytes\" desc","GROUP BY http_domain ORDER BY \"Bytes\" desc")
    changed_sql = changed_sql.replace("GROUP BY \"Server IP\" , \"Http.Domain\" ORDER BY \"Bytes\" desc LIMIT 1048576","GROUP BY common_server_ip , http_domain ORDER BY \"Bytes\" desc LIMIT 1048576")
    changed_sql = changed_sql.replace("GROUP BY \"Client IP\", \"Http.Domain\" ORDER BY \"Sessions\" DESC LIMIT 1048576)","GROUP BY common_client_ip, http_domain ORDER BY \"Sessions\" DESC LIMIT 1048576)")
    changed_sql = changed_sql.replace("GROUP BY \"Receive Time\", \"Device ID\" LIMIT 10000","GROUP BY cast(common_recv_time/300 as int) * 300,common_device_id LIMIT 10000")
    changed_sql = changed_sql.replace("GROUP BY \"Receive Time\"","GROUP BY cast(common_recv_time/300 as int) * 300")

    #changed_sql = changed_sql.replace("","")

    return changed_sql

def ch_to_ol():
    with open("./poc-ch.json","r") as file:
        content = file.read()
        all = json.loads(content)
    olsql = {}
    for k,v in all.items():
        olsql[k] = change_sql(v)

    with open("./auto-ol.json","w") as file:
        file.write(json.dumps(olsql))

ch_to_ol()