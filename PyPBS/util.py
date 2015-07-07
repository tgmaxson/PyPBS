from subprocess import PIPE, Popen

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def subset(mydict, func):
    return dict((key, mydict[key]) for key in mydict if func(mydict[key]))
