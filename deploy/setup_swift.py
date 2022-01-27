from server import Server
import os

def install_apt_packages(server):
    print("installing apt packages")
    server.update_apt_packages()
    server.install_apt_package("python3-pip")

def verify_apt_packages(server):
    packages = server.get_installed_apt_packages()
    assert "python3-pip" in packages
    # make sure we have git
    version = server.get_git_version()
    assert version.startswith("2.")

def install_pip3_packages(server):
    version = server.get_pip3_version()
    assert version.startswith("20.")
    assert version.endswith("3.8")
    server.install_pip3_package("dataset")
    server.install_pip3_package("bottle")

def verify_pip3_packages(server):    
    packages = server.get_installed_pip3_packages()
    assert "dataset" in packages
    assert "bottle" in packages

def get_source_code(server):
    # make sure we have a projects directory
    server.run("mkdir -p ~/projects")   # <-- idempotent, we can repeat harmlessly

    # delete old swift directory if there
    server.run("rm -rf ~/projects/swift")

    # get the code from Git
    server.run("cd ~/projects; git clone --depth 1 https://github.com/drdelozier/swift.git", hide=False)
    server.run("cd ~/projects/swift; rm -rf .git", hide=False)

def verify_source_code(server):
    # verify the code was deployed
    out, _ = server.run("ls ~/projects/swift")
    files = out.strip().split("\n")
    for f in ['LICENSE', 'README.md', 'deploy', 'setup.py', 'swift.py', 'views']:
        assert f in files
 
def initialize_database(server):
    # set up the database, etc.
    server.run("cd ~/projects/swift; python3 setup.py")

def get_process_id(process):
    parts = process.strip().split(" ")
    id = int(parts[0])
    assert type(id) is int
    return id

def start_application(server):
    server.run("cd ~/projects/swift; screen -S webapp -dm python3 swift.py")

def stop_application_processes(server):
    # find and kill the screen process
    processes = server.get_running_processes()
    processes = [p for p in processes if "SCREEN" in p and "swift.py" in p ]
    if len(processes) > 0:
        screen_id = get_process_id(processes[0])
        server.sudo(f"kill -9 {screen_id}")

    # find and kill remaining swift.py python process, if any.
    processes = server.get_running_processes()
    processes = [p for p in processes if "SCREEN" not in p and "swift.py" in p ]
    if len(processes) > 0:
        screen_id = get_process_id(processes[0])
        server.sudo(f"kill -9 {screen_id}")

    # verify that processes aren't running
    processes = server.get_running_processes()
    processes = [p for p in processes if "swift.py" in p ]
    assert len(processes) == 0

def verify_application_processes(server):
    # verify the screen process
    processes = server.get_running_processes()
    processes = [p for p in processes if "SCREEN" in p and "swift.py" in p ]
    assert len(processes) == 1, "Screen session process was not found."

    # verify the swift.py python process.
    processes = server.get_running_processes()
    processes = [p for p in processes if "SCREEN" not in p and "swift.py" in p ]
    assert len(processes) == 1, "$ python3 swift.py was not found"

if __name__ == "__main__":
    server = Server(host = "3.129.67.194", user="ubuntu", key_filename="/Users/greg/.ssh/lightsail-ohio-gsd.pem")
    print("installing apt packages...")
    install_apt_packages(server)
    verify_apt_packages(server)
    print("installing pip packages...")
    install_pip3_packages(server)
    verify_pip3_packages(server)
    print("stopping application...")
    stop_application_processes(server)
    print("getting source...")
    get_source_code(server)
    print("verifying source...")
    verify_source_code(server)
    print("initializing db...")
    initialize_database(server)
    print("starting application...")
    start_application(server)
    verify_application_processes(server)
    print("done.")