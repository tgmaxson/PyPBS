#! /usr/bin/env python
from util import cmdline
import xml.etree.ElementTree as ET


def qstat_processor(qresult):
    qdict = {}
    root = ET.XML(qresult)
    for job in root:
        id = job_root.find("Job_Id")
        qdict[id] = {}
        

    for job_root in root:
     id = job_root.find("Job_Id").text.split(".")[0]
     name = job_root.find("Job_Name").text
     variables = job_root.find("Variable_List").text.split(",")
     for v in variables:
        if pwd == v:
            print "Killing {0} ({1})".format(name, id)
            cmdline("qdel {0} &".format(id))

def qstat(user=None, queue=None, extra=None, remote=None):
    command = ""
    if remote is not None:
        command += 'ssh -x {0} '.format(str(remote))
    command += "qstat -x -f "
    if user is not None:
        command += "-u {0} ".format(str(user))
    if queue is not None:
        command += str(queue)
    if extra is not None:
        command += str(extra)

    qresult = cmdline(command)
    return qresult
