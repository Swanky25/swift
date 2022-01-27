from server import Server
import os

def file_exists(server, name):
    out, _ = server.run("ls")
    print(out)
    files = out.strip().split("\n")
    print(files)
    return name in files

if __name__ == "__main__":
    server = Server(host = "3.129.67.194", user="ubuntu", key_filename="/Users/greg/.ssh/lightsail-ohio-gsd.pem")
    # server.run("ls -la", hide=False)
    # server.run("ps", hide=False)
    # server.run("echo hello >hello.txt", hide=False)
    # server.run("ls -la", hide=False)
    # server.run("cat hello.txt", hide=False)
    # out, _ = server.run("ls -la")
    # print(out.split("\n"))
    #if file_exists(server, "hello.txt"):
    #    print("file exists")
    packages = server.get_installed_apt_packages()
    print(packages)