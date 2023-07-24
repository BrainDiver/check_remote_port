import asyncio
import aiofiles
import re
from tqdm import tqdm
import os

print("""
Make file ips_diap.txt in directory with program file. 
In this file enter ranges ip adresses. 
Ip range must be like start_ip-end_ip. Each range must be at new line: ip-ip
                                                                       ip-ip
""")
port=int(input("Введите порт "))

def diap_to_ips(ip_diap, count_name):
    split_diap=ip_diap.split("-")
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    first_ip=split_diap[0]
    second_ip=split_diap[1]
    if re.search(regex, first_ip) and re.search(regex, second_ip):
        first_ip_split=first_ip.split(".")
        second_ip_split=second_ip.split(".")
        list_result=[]
        if first_ip_split[1] != second_ip_split[1]:
            start_ip=int(first_ip_split[1])
            stop_ip=int(second_ip_split[1])
            part_ip=f"{first_ip_split[0]}"
            count_ip=0
            for item in range(start_ip, stop_ip+1):
                for first_number in range(0,256):
                    for second_number in range(0,256):
                        if count_ip <100:
                            with open("{os.getcwd()}/trash_dir/ips_{count_name}.txt", "a") as myfile:
                                myfile.write(f"{part_ip}.{item}.{first_number}.{second_number}\n")
                            count_ip+=1
                        else:
                            count_name+=1
                            with open("{os.getcwd()}/trash_dir/ips_{count_name}.txt", "a") as myfile:
                                myfile.write(f"{part_ip}.{item}.{first_number}.{second_number}\n")
                            count_ip=0
                            count_ip+=1
            return count_name


        elif first_ip_split[1] == second_ip_split[1]:
            start_ip=int(first_ip_split[2])
            stop_ip=int(second_ip_split[2])
            part_ip=f"{first_ip_split[0]}.{first_ip_split[1]}"
            count_ip=0
            for item in range(start_ip, stop_ip+1):
                for number in range(0, 256):
                    if count_ip < 100:
                        if not os.path.isdir("trash_dir"):
                            os.makedirs("trash_dir")
                        else:
                            pass
                        with open(f"{os.getcwd()}/trash_dir/ips_{count_name}.txt", "a") as myfile:
                            myfile.write(f"{part_ip}.{item}.{number}\n")
                        count_ip+=1
                    else:
                        count_name+=1
                        with open(f"{os.getcwd()}/trash_dir/ips_{count_name}.txt", "a") as myfile:
                            myfile.write(f"{part_ip}.{item}.{number}\n")
                        count_ip=0
                        count_ip+=1
            return count_name


    else:
        print(f"incorrect ip range: {ip_diap}")


def ips_diap():
    count_name=0
    with open("ips_diap.txt", "r") as file1:
        for line in file1:
            count_name=diap_to_ips(line, count_name)
        return count_name


count_name=ips_diap()


async def request(ip, port):
    try:
        reader, writer= await asyncio.wait_for(asyncio.open_connection(host=ip, port=port), timeout=3)
        print(True)
        asyncio.open_connection(host=ip, port=port).close()
        string_result=f"{ip}T"
        return string_result
    except Exception:
        asyncio.open_connection(host=ip, port=port).close()
        string_result=f"{ip}F"
        return string_result


async def main(port, item):
    with open(f"{os.getcwd()}/trash_dir/ips_{item}.txt") as file2:
        results=[]
        for line in file2:
            results.append(request(ip=line[:-1], port=port))
        os.remove(f"{os.getcwd()}/trash_dir/ips_{item}.txt")
        return await asyncio.gather(*results)

for item in tqdm(range(0, count_name+1)):
    results=asyncio.run(main(port, item))
    for result in results:
        if result[-1]=="T":
            with open("good.txt", "a") as file3:
                file3.write(f"{result[:-1]}\n")
        else:
            with open("bad.txt", "a") as file4:
                file4.write(f"{result[:-1]}\n")
