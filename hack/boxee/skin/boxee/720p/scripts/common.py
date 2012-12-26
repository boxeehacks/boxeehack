import os,sys

sys.path.append(os.path.abspath("./external"))

if 'linux' in sys.platform:
    sys.path.append(os.path.abspath("./external/Linux"))
elif 'win32' in sys.platform:
    sys.path.append(os.path.abspath("./external/win32"))
elif 'darwin' in sys.platform:
    sys.path.append(os.path.abspath("./external/OSX"))

# Read file contents into a string
def file_get_contents(filename):
    if os.path.exists(filename):
        fp = open(filename, "r")
        content = fp.read()
        fp.close()
        return content
    return ""

# Write string back to a file
def file_put_contents(filename, content):
    fp = open(filename, "w")
    fp.write(content)
    fp.close()