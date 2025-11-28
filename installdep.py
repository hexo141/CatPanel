import subprocess
import lwjgl
import sys

def install():
    try:
        import uv
    except:
        try:
            subprocess.run(["pip","install","uv"])
        except subprocess.CalledProcessError as e:
            lwjgl.logging.log("ERROR", f"Failed to install uv: {e}")
            return False
    lwjgl.logging.log("INFO", "Installing dependencies from requirements.txt...")
    try:
        subprocess.run(["uv","pip","install","--requirement","requirements.txt","--break-system-packages","--python",sys.executable])
    except subprocess.CalledProcessError as e:
        lwjgl.logging.log("ERROR", f"Failed to install dependencies: {e}")
        return False
    lwjgl.logging.log("INFO", "Dependencies installed successfully.")
    return True
    