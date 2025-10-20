import os
import updatelist

def main():
    user = os.getlogin()
    base_path = f"/home/{user}/.config/car"
    
    print(f"Creating {base_path}/")
    os.makedirs(f"{base_path}/hooks", exist_ok=True)

    hook_path = f"{base_path}/hooks/check_core.py"
    with open(hook_path, "w") as f:
        f.write(
            'import os\n'
            'def run(package):\n'
            '    os.system("curl -s -L -o cores https://raw.githubusercontent.com/redroselinux/car-coreutils-repo/refs/heads/main/cores")\n'
            '    with open(\'cores\', \'r\') as f:\n'
            '        cores = f.read()\n'
            '    if package in cores.splitlines():\n'
            '        print("Reboot recommended!")\n'
        )

    post_inst_path = f"{base_path}/post-inst-hooks"
    with open(post_inst_path, "w") as f:
        f.write(f"{hook_path}\n")
    
    print(f"Created hook script at {hook_path}")
    print(f"Created post-inst-hooks file at {post_inst_path}")

    updatelist.main()
