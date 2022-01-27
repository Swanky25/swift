from server import Server

from setup_swift import verify_apt_packages, verify_pip3_packages

if __name__ == "__main__":
    server = Server(host = "3.129.67.194", user="ubuntu", key_filename="/Users/greg/.ssh/lightsail-ohio-gsd.pem")
    verify_apt_packages(server)
    verify_pip3_packages(server)
    print("done.")