cookie_string = '_frid=80a35ec3d6b44eb5af3b7c765563083a; cbc-sid=204936ea380af66f0881426359f7394bd6001bcb334ed41e1e587ace1ba1e5d3a516ef2c4629377b373c; vk=dc9a41cb-775e-4c46-911b-d698cd48a412; SessionID=86cdb5cb-7273-4767-973b-508ef6931489; ad_sc=; ad_mdm=; ad_cmp=; ad_ctt=; ad_tm=; ad_adp=; cf=Direct; ukey_sn=""; domain_tag=06ce3c51e88010570fe6c015b15326c0; user_tag=0749b96d628010001f4ac015ed5e4ae3; masked_domain=h****nchen; masked_user=t****ewang; masked_phone=176****3192; usite=cn; popup_max_time=1440; x-framework-ob=""; SID=Set2; browserCheckResult=A; ua=06ce3c51e88010570fe6c015b15326c0; cfLatestRecordTimestamp=1745221204961; HWWAFSESID=932817612790bd52f6; HWWAFSESTIME=1745221238364; devclouddevuigzagencyID=0749b96d628010001f4ac015ed5e4ae3; devclouddevuigzcftk=2BP9-NXNK-KR1J-JQ34-UXGL-PLY4-V1UY-Z1CO; _w3Fid=0749b96d628010001f4ac015ed5e4ae3; flowcard06ce3c51e88010570fe6c015b15326c0CodeArts-Req=06ce3c51e88010570fe6c015b15326c0; locale=zh-cn; _fr_ssid=cfe3825f20d04033833caa6d7992805d; devclouddevuigzJ_SESSION_ID=f4b3ecaec644a7a3fae03e36ea80cdbd2cd01af7aca1ed6e; BENSESSCC_TAG=f4b3ecaec644a7a3fae03e36ea80cdbd2cd01af7aca1ed6e; _fr_pvid=06ccfcf8b0ca414f9ed397895b111b79'

# 解析成字典
cookies = {}
for part in cookie_string.split(';'):
    if '=' in part:
        name, value = part.strip().split('=', 1)
        cookies[name] = value

print(cookies)