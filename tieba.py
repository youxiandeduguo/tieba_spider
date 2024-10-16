import requests
from lxml import etree
import csv
import time
import re
import random
from datetime import datetime


def get_one(page, herf, csvwrite, header):
    comment_cot = 0
    url = f"https://tieba.baidu.com{herf}"
    ppage = page
    the_url = url
    if page != 1:
        the_url = the_url + '?pn=' + str(page)
    res = requests.get(the_url, headers=header)
    num = herf.split('/')[-1]
    print(the_url)
    parser = etree.HTMLParser(encoding='utf-8')
    content = etree.HTML(res.text, parser=parser)
    res.close()
    comment = content.xpath("/html/body/div[2]/div/div[2]/div/div[4]/div[1]/div[3]/div/div[2]/div[1]/cc/div[2]")
    # page = int(content.xpath("/html/body/div[2]/div/div[2]/div/div[3]/div[1]/ul/li[2]/span[2]/text()")[0])
    #/html/body/div[3]/div/div[2]/div/div[5]/div[2]/div[1]/ul/li[2]/span[2]
    #/html/body/div[3]/div/div[2]/div/div[5]/div[2]/div[1]/ul/li[2]/span[2]
    #/html/body/div[3]/div/div[2]/div/div[3]/div[1]/ul/li[2]/span[2]
    try:
        page = int(content.xpath("/html/body/div[2]/div/div[2]/div/div[3]/div[1]/ul/li[2]/span[2]/text()")[0])
    except:
        page=1
    str_comment = []
    dic = {}
    for i in comment:
        str_comment.append(''.join(str(s) for s in i.xpath("./text()")).strip())

    name = content.xpath("/html/body/div[2]/div/div[2]/div/div[4]/div[1]/div[3]/div/div[1]/ul/li[3]/a/text()")
    po=content.xpath('//*[@id="j_p_postlist"]/div/div[2]/div[2]/div[1]/div/span[1]/text()')
    timee=content.xpath('//*[@id="j_p_postlist"]/div/div[2]/div[2]/div[1]/div/span[6]/text()')
    if min(len(name), len(str_comment)) > 0:
        for d in range(min(len(name), len(str_comment),len(timee))):
            if len(str_comment[d])>2:
                dic = {'name': name[d],
                       'comment': str_comment[d],
                       'time':timee[d],
                       'position':po[d]}
                csvwrite.writerow(dic.values())
                comment_cot += 1

    time.sleep(random.random())
    url2 = f"https://tieba.baidu.com/p/totalComment?t=1729087530500&tid={num}&fid=422204&pn={ppage}&see_lz=0"
    #https://tieba.baidu.com/p/totalComment?t=1721021685857&tid=9075740237&fid=2541667&pn=2&see_lz=0
    #https://tieba.baidu.com/p/totalComment?t=1721021734768&tid=9086479895&fid=2541667&pn=1&see_lz=0
    res2 = requests.get(url2,headers=header)
    content2 = res2.json()
    comment_list = content2['data']['comment_list']
    res2.close()
    for i in comment_list:
        comment_info = comment_list[i]['comment_info']
        cot = comment_list[i]['comment_list_num']
        if cot > 0:
            for j in range(0, len(comment_info)-1):
                if len(str(comment_info[j]['content'])) <2:
                    continue
                if str(comment_info[j]['content'])[0:2] == "回复":
                    # print(str(comment_info[j]['content']))
                    # <re.Match object; span=(3, 252), match='<a href=""  onclick="Stats.sendRequest(\'fr=tb0_f>
                    result = re.sub(r'<.*?>', '', str(comment_info[j]['content']), re.S)
                    result = re.sub(r'.*?:', '', result, re.S)
                    # print(result)
                    dic = {
                        'name': str(comment_info[j]['show_nickname']),
                        'comment': str(result),
                        'time': str(datetime.fromtimestamp(comment_info[j]['now_time']))
                    }

                    csvwrite.writerow(dic.values())
                    comment_cot += 1
                    continue
                dic = {
                    'name': str(comment_info[j]['show_nickname']),
                    'comment': str(comment_info[j]['content']).split("<")[0],
                    'time': str(datetime.fromtimestamp(comment_info[j]['now_time']))
                }

                csvwrite.writerow(dic.values())
                comment_cot += 1
    return page, comment_cot
def get_page(page, herf, csvwrite, header):
    comment_cot = 0
    url = f"https://tieba.baidu.com{herf}"
    ppage = page
    the_url = url
    if page != 1:
        the_url = the_url + '?pn=' + str(page)
    res = requests.get(the_url, headers=header)
    num = herf.split('/')[-1]
    print(the_url)
    parser = etree.HTMLParser(encoding='utf-8')
    content = etree.HTML(res.text, parser=parser)
    res.close()
    comment = content.xpath("/html/body/div[2]/div/div[2]/div/div[4]/div[1]/div[3]/div/div[2]/div[1]/cc/div[2]")
    str_comment = []
    dic = {}
    for i in comment:
        str_comment.append(''.join(str(s) for s in i.xpath("./text()")).strip())

    name = content.xpath("/html/body/div[2]/div/div[2]/div/div[4]/div[1]/div[3]/div/div[1]/ul/li[3]/a/text()")
    po=content.xpath('//*[@id="j_p_postlist"]/div/div[2]/div[2]/div[1]/div/span[1]/text()')
    timee=content.xpath('//*[@id="j_p_postlist"]/div/div[2]/div[2]/div[1]/div/span[6]/text()')
    if min(len(name), len(str_comment)) > 0:
        for d in range(min(len(name), len(str_comment),len(timee))):
            if len(str_comment[d]) > 2:
                dic = {'name': name[d],
                       'comment': str_comment[d],
                       'time': timee[d],
                       'position': po[d]}
                csvwrite.writerow(dic.values())
                comment_cot += 1

    time.sleep(random.random())
    url2 = f"https://tieba.baidu.com/p/totalComment?t=1729087530500&tid={num}&fid=422204&pn={ppage}&see_lz=0"
    #https://tieba.baidu.com/p/totalComment?t=1721021685857&tid=9075740237&fid=2541667&pn=2&see_lz=0
    #https://tieba.baidu.com/p/totalComment?t=1721021734768&tid=9086479895&fid=2541667&pn=1&see_lz=0
    res2 = requests.get(url2,headers=header)
    content2 = res2.json()
    comment_list = content2['data']['comment_list']
    res2.close()
    for i in comment_list:
        comment_info = comment_list[i]['comment_info']
        cot = comment_list[i]['comment_list_num']
        if cot > 0:
            for j in range(0, len(comment_info)-1):
                if len(str(comment_info[j]['content'])) <2:
                    continue
                if str(comment_info[j]['content'])[0:2] == "回复":
                    # print(str(comment_info[j]['content']))
                    # <re.Match object; span=(3, 252), match='<a href=""  onclick="Stats.sendRequest(\'fr=tb0_f>
                    result = re.sub(r'<.*?>', '', str(comment_info[j]['content']), re.S)
                    result = re.sub(r'.*?:', '', result, re.S)
                    # print(result)
                    dic = {
                        'name': str(comment_info[j]['show_nickname']),
                        'comment': str(result),
                        'time':str(datetime.fromtimestamp(comment_info[j]['now_time']))
                    }

                    csvwrite.writerow(dic.values())
                    comment_cot += 1
                    continue
                dic = {
                    'name': str(comment_info[j]['show_nickname']),
                    'comment': str(comment_info[j]['content']).split("<")[0],
                    'time': str(datetime.fromtimestamp(comment_info[j]['now_time']))
                }

                csvwrite.writerow(dic.values())
                comment_cot += 1
    return comment_cot

def get_main(pn, header):
    comment_cot = 0
    url = f"https://tieba.baidu.com/f?kw=%E4%B8%AD%E5%9B%BD%E4%BA%BA%E5%8F%A3&ie=utf-8&pn={pn * 50}"
    # https://tieba.baidu.com/f?kw=%E5%8F%8D%E4%BA%8C%E6%AC%A1%E5%85%83&ie=utf-8&pn=50


    respond = requests.get(url, headers=header)
    obj2 = re.compile(r'title="回复">(?P<cot>.*?)<')
    obj = re.compile(r'<a rel="noopener" href="(?P<href>.*?)" title=')
    # <a rel="noopener" href="/p/9085888833" title="二刺螈新规矩" target="_blank" class="j_th_tit ">二刺螈新规矩</a>
    result = obj.finditer(respond.text)
    result2 = obj2.finditer(respond.text)
    respond.close()
    for j, k in zip(result, result2):

        if int(k.group('cot')) > 40:
            page = 1
            time.sleep(random.random()+1)
            page, the_cot = get_one(page, j.group('href'), csvwrite, header)
            comment_cot += the_cot
            if page > 1:
                for i in range(2, page):
                    time.sleep(random.random())
                    the_cot = get_page(i, j.group('href'), csvwrite, header)
                    comment_cot += the_cot
    return comment_cot


if __name__ == '__main__':

    goal_comment = 100000
    f = open("tieba中国人口吧.csv", mode="w", encoding="utf-8", newline="")
    csvwrite = csv.writer(f)
    comment_cot = 0


    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "Cookie": '__bid_n=18894b4c8ee66df7214207; BIDUPSID=3E9B05F3C72FEE90FFBEA1B4934E0D55; PSTM=1689813886; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1713698121,1714547366,1715648287; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22351639208%22%2C%22first_id%22%3A%221902e6e23e98f8-069a749520ecf4-4c657b58-1327104-1902e6e23eafde%22%2C%22props%22%3A%7B%7D%2C%22%24device_id%22%3A%221902e6e23e98f8-069a749520ecf4-4c657b58-1327104-1902e6e23eafde%22%7D; BAIDU_WISE_UID=wapp_1720683359756_891; H_PS_PSSID=60274; BDUSS=GRvZ2Uyb2t3OEVIUUZSaURDYm5kQ3pES3EtcmdLZ3hNeDRpLXFYLWRBSi1STHhtRVFBQUFBJCQAAAAAAAAAAAEAAAAxjamOw87I1M60vqEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH63lGZ-t5RmW; BDUSS_BFESS=GRvZ2Uyb2t3OEVIUUZSaURDYm5kQ3pES3EtcmdLZ3hNeDRpLXFYLWRBSi1STHhtRVFBQUFBJCQAAAAAAAAAAAEAAAAxjamOw87I1M60vqEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH63lGZ-t5RmW; STOKEN=121fa088199a6e69ec425417b356827712047532d9bc7b5cfd2aed80acd3642e; BAIDUID=41C00538D4C78591108721AF75FFDE04:FG=1; ZFY=DYZUSuza3Obhn8v7afNyn6CwSx65jdrzsTija8sgqu8:C; BAIDUID_BFESS=41C00538D4C78591108721AF75FFDE04:FG=1; arialoadData=false; USER_JUMP=-1; Hm_lvt_292b2e1608b0823c1cb6beef7243ef34=1721977229,1722000004,1722045429,1722068259; HMACCOUNT=02F90352768B486B; st_key_id=17; wise_device=0; XFI=0f6386b0-4bfb-11ef-9fb8-47676d2f0284; ab_sr=1.0.1_ODk0N2EwNWExYWE2M2VjNzAwYTU4Nzk3NmIyOTliMTMxMjYzNGRkMDFjNGRlNGQ4ZmM3ZDQwYTMyMDljYmEzYWEwNmRhNGQwZjdhY2ZjMjlkYWYzYzEzZjFiYzI3MTRjMWVhNDk5N2Y2YjJlMWYyN2FkOGRlNTg0YTc5MmI1N2MyNTdiNDA2YWUxOTQ1NDE4ZTM5NTc1ZGMzZThhOGJjNzI2Y2JkNjNmYTczYjA0NDBkNTFhY2I5MDhmN2RmZGQy; st_data=06e029c40dc3eae4ff91000a5dea287f2b01886e0d87b4ad0f78a32739d57a07a3e1995d1d01b44ed4c39b1a436691287036e0c05522ca6a45dc84c40a41667a8149799250ac1f18ce863c9bd19cd60807a8dd5086664b39ef036d3af157bb3fefe88d2d0105aef9717abe20be414022e687ca7cb1eb86508e861332d15c93e98e220607996dedd6a756c5922caad3f3; st_sign=89bc6c38; XFCS=6E0418963F7EE708F63ABF9DBA8694F56B8F6B9F738FC25430379B8344A47D3D; XFT=NzVcAiQRKeOYRTAaqpzsS0ckC88T/Yr3+aV7kcYF9u4=; RT="z=1&dm=baidu.com&si=b4d986d5-5bef-4608-a306-aec245402e22&ss=lz3hdvlh&sl=19&tt=w60&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=g8wae&ul=iku3x&hd=iku8o"; tb_as_data=e0738a5425e486c02090c02148e8a35e0e0f876efe6d4010211b5f99157dbc7408c0989acb7d5be1d4304b6060ee9ff100aed09cd7d6e2fdd43f8b4a1a1efcee53c6836b8da97d44d2837287ebb9e6cac3347272a486b5b9220b475455a7e9388c523196b472d52039d0b847383ae273; Hm_lpvt_292b2e1608b0823c1cb6beef7243ef34=1722076641',
        "Referer": 'https://tieba.baidu.com/f?kw=%E5%8F%8D%E4%BA%8C%E6%AC%A1%E5%85%83&p_tk=8305fB1wWa6IY9y59hWOGz9JqgEwC9r29bColtsWYbKHQJsQ8Ibkw6yopADwOHID6W6xg%2FXC%2BLOzE2AjpP5iWSit6Ebg4it%2Fl%2BJAAlCArcSpV36uTSANJfz%2BUVHqF0FQEVPMe9n%2Fya0wXlpYJzqbJFwLuAW%2F7jwMKTrAD1DOiXpRxys%3D&p_timestamp=1721039117&p_sign=ffa45461e4c4eb2d06fecca262da14d5&p_signature=72a03c5daef015bc1ebe98f8cd804229&__pc2ps_ab=8305fB1wWa6IY9y59hWOGz9JqgEwC9r29bColtsWYbKHQJsQ8Ibkw6yopADwOHID6W6xg%2FXC%2BLOzE2AjpP5iWSit6Ebg4it%2Fl%2BJAAlCArcSpV36uTSANJfz%2BUVHqF0FQEVPMe9n%2Fya0wXlpYJzqbJFwLuAW%2F7jwMKTrAD1DOiXpRxys%3D|1721039117|72a03c5daef015bc1ebe98f8cd804229|ffa45461e4c4eb2d06fecca262da14d5'
    }
    page_cot = 0
    #0
    while comment_cot < goal_comment:
        print('-' + str(page_cot))
        time.sleep(random.random() + 1)
        comment_cot += get_main(page_cot, header)
        page_cot += 1

    f.close()
