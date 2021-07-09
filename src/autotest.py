# -*- coding: utf-8 -*-
import clickhouse_driver
import openlookeng_driver
import json,time,logging,sys
import configparser
olconfig = {}
chconfig = {}

time1,time2 = '',''
sql_timeout = 2000
def change_sql(origin_sql):
    changed_sql = origin_sql.replace("$time1","'" + time1 + "'").replace("$time2","'" + time2 + "'")
    return changed_sql


def execute_sql(client,sql):
    start = time.time()
    ans = client.execute(sql)
    end = time.time()
    return end-start
    
def get_current_time():
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

def run_ch(test_sql,now_time = '2021'):
    client = clickhouse_driver.Client(host=chconfig['host'],port=chconfig['port'],user=chconfig['user'] ,password=chconfig['password'])
    results = {}
    total_time = 0
    suc_num,fail_num = 0,0
    for k,v in test_sql.items():
        result = {}
        run_sql = change_sql(v)
        result['sql'] = run_sql
        try:
            used_time = execute_sql(client,run_sql)
            if k == 'pre':
                continue
            total_time += used_time
            result['used_time'] = used_time
            result['data_num'] = 0
            result['info'] = ''
            suc_num += 1
            print("running Q{} success , {}√，{}×".format(k,suc_num,fail_num))
        except Exception as e:
            result['used_time'] = -1
            result['data_num'] = -1
            result['info'] = str(e)
            fail_num += 1
            print("running Q{} success , {}√，{}×".format(k,suc_num,fail_num))

        results[k] = result
        try:
            with open("../log/ch-"+now_time + ".json",'w') as file:
                file.write(json.dumps(results))
        except Exception as e:
            print("error",e)
        try:
            with open("../log/ch-result.log","a+") as file:
                file.write("{} success num: {}  failed num: {} \n".format(now_time,suc_num,fail_num))
        except Exception as e:
            print(e)
        time.sleep(10)



def run_olk(test_sql,now_time = '2021'):
    client = openlookeng_driver.Client(host=olconfig['host'],port=int(olconfig['port']),user=olconfig['user'],catalog=olconfig['catalog'],schema=olconfig['schema'])
    client.add_logging(log_level=logging.DEBUG)
    results = {}
    total_time = 0
    suc_num,fail_num = 0,0
    for k,v in test_sql.items():
        result = {}
        run_sql = change_sql(v)
        result['sql'] = run_sql
        web_result = client.web_execute(run_sql)
        used_time = float(web_result.get_used_time(sql_timeout))  # second
        total_time += used_time
        result['used_time'] = used_time
        result['data_num'] = 0
        result['info'] = web_result.error_info
        if web_result.error_info == '':
            suc_num += 1
            print("running Q{} success , {}√，{}×".format(k,suc_num,fail_num))

        else:
            fail_num += 1
            print("running Q{} success , {}√，{}×".format(k,suc_num,fail_num))
        results[k] = result
        try:
            with open("../log/ol-" + now_time + ".json",'w') as file:
                file.write(json.dumps(results))
        except Exception as e:
            print("error",e)
        try:
            with open("../log/ol-result.log","a+") as file:
                file.write("{} success num: {}  failed num: {} \n".format(now_time,suc_num,fail_num))
        except Exception as e:
            print(e)
    time.sleep(10)

def ch_poc():
    with open("poc-ch.json",'r') as file:
        now_time = get_current_time()
        poc = json.loads(file.read())
        run_ch(poc,now_time)

def ol_poc():
    with open("auto-ol.json",'r') as file:
        now_time = get_current_time()
        poc = json.loads(file.read())
        run_olk(poc,now_time)


def read_conf():
    global time1,time2,sql_timeout,olconfig,chconfig
    config = configparser.ConfigParser()
    config.read("config")
    time1 = config.get("run","time1")
    time2 = config.get("run","time2")
    sql_timeout = config.get("run","time_out")
    chconfig['host'] = config.get("clickhouse","host")
    chconfig['port'] = config.get("clickhouse","port")
    chconfig['user'] = config.get("clickhouse","user")
    chconfig['password'] = config.get("clickhouse","password")

    olconfig['host'] = config.get("openlookeng","host")
    olconfig['port'] = config.get("openlookeng","port")
    olconfig['user'] = config.get("openlookeng","user")
    olconfig['catalog'] = config.get("openlookeng","catalog")
    olconfig['schema'] = config.get("openlookeng","schema")


if __name__ == "__main__":
    read_conf()
    if sys.argv[1] == 'ch':
        print("run ch")
        ch_poc()
    else:
        print("run ol")
        ol_poc()
    

    
        
