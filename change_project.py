import json
import requests

saas_ip = 

def get_token_and_tenant_uuid():  # 获取token和admin租户uuid
    endpoint = 'http://%s:35357/v3/auth/tokens' % (saas_ip)
    payload = {"auth": {"identity": {"methods": ["password"], "password": {
        "user": {"name": "admin", "domain": {"name": "Default"}, "password": ""}}}}}
    payload["auth"]["identity"]["password"]["user"]["password"] = saas_pass
    headers = {'Content-type': 'application/json'}
    req = requests.post(endpoint, data=json.dumps(payload), headers=headers)
    token = req.headers['x-subject-token']
    tenant_uuid = req.json()['token']['user']['domain']['id']
    list_tau = [token, tenant_uuid]

    return list_tau


def get_flavor_name(token, tenant_uuid, instance_uuid):  # 获取flavor的name
    # endpoint = 'http://%s:8774/v2.1/%s/flavors/detail' % (saas_ip,
    #                                                             tenant_uuid)
    # headers = {'X-Auth-Token': token}
    # req = requests.get(endpoint, headers=headers)
    # res = req.json()
    # flavors_list = res['flavors']
    # for flavor_detail in flavors_list:
    #     if flavor_detail['ram'] == 2048 and flavor_detail['vcpus'] == 2:
    #         flavor_uuid = flavor_detail['id']
    #         return flavor_uuid
    endpoint = 'http://%s:8774/v2.1/%s/servers/%s' % (saas_ip,
                                                      tenant_uuid,
                                                      instance_uuid)
    headers = {'X-Auth-Token': token}
    req = requests.get(endpoint, headers=headers)
    res = req.json()
    flavors_name = res["server"]["flavor"]["original_name"]
    return flavors_name


def get_volume_id(token, tenant_uuid, instance_uuid):
    endpoint = 'http://%s:8774/v2.1/%s/servers/%s/os-volume_attachments' % (saas_ip,
                                                                            tenant_uuid,
                                                                            instance_uuid)
    headers = {'X-Auth-Token': token}
    req = requests.get(endpoint, headers=headers)
    res = req.json()
    volume_attachments = res["volumeAttachments"]
    temp = []
    for i in range(len(volume_attachments)):
        temp.append(volume_attachments["volumeAttachments"][i]["id"])
    return temp


def get_instance_net_info(token, tenant_uuid, instance_uuid):
    endpoint = 'http://%s:8774/v2.1/%s/servers/%s/os-interface' % (saas_ip,
                                                                   tenant_uuid,
                                                                   instance_uuid)

    headers = {'X-Auth-Token': token}
    req = requests.get(endpoint, headers=headers)
    res = req.json()
    instance_ip = res["interfaceAttachments"][0]["fixed_ips"][0]["ip_address"]
    instance_port_mac = res["interfaceAttachments"][0]["mac_addr"]
    instance_port_id = res["interfaceAttachments"][0]["port_id"]
    instance_net_id = res["interfaceAttachments"][0]["net_id"]
    instance_subnet_id = res["interfaceAttachments"][0]["fixed_ips"][0]["subnet_id"]
    return instance_ip, instance_port_mac, instance_port_id, instance_net_id, instance_subnet_id
