import socket as client

class Minsat:

    def __init__(self, ip, port):
        self.ip_port = (ip, port)
        self.minsat = client.socket(client.AF_INET, client.SOCK_STREAM)

    def connect(self):
        self.minsat.connect(self.ip_port)

    def send_command(self, cmd):
        cmd += "\r\n"
        self.minsat.send(bytes(cmd.encode()))
        final_response = ''
        while True:
            data = self.minsat.recv(1024*2)
            res = data.decode('utf-8')
            final_response += res
            if len(res) == 0 or res[-1] == '\n':
                break
        return final_response
    
    def login(self, username, password):
        reply = self.send_command(f'LOGIN:{username}:{password};')
        if reply != None:
            resp_code = int(reply.split(':')[1].strip()[0])
            return resp_code == 0
        return False

    def logout(self):
        self.send_command('LOGOUT;')

    def close(self):
        self.logout()
        self.minsat.close()

if __name__ == '__main__':
    server = Minsat('10.195.2.222', 7020)
    server.connect()
    if (server.login('minsat', 'Minsat@2019')):
        reply = server.send_command(
            'GET:ACCOUNTINFORMATION:2:SubscriberNumber,245966002971;')
        print(reply, end='')
        server.close()

