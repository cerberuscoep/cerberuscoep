file1 = open('/etc/nginx/sites-available/reverse-proxy.conf', 'r+')
etc = file1.read()
etc = etc.split('}')
print(etc)
etc.pop()
etc.pop()
etc.append("\n\tlocation /deployment/demo {\n\trewrite ^/lekana/demo(.*)$ $1 break;\n\tproxy_pass http://localhost:5000;\n\t}\n");
file1.close()
file1 = open('/etc/nginx/sites-available/reverse-proxy.conf', 'w')
for i in etc:
    file1.write(f"{i}" + "}")