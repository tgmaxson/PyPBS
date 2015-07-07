#! /usr/bin/env python
from util import cmdline
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def qstat(user=None, queue=None, extra=None, remote=None, process=False):
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
    if process:
        qresult = qstat_process(qresult)
    return qresult

def qstat_process(qresult):
    qdict = {}
    root = ET.XML("<WRAPPER>"+qresult+"</WRAPPER>")
    for data in root:
        for job in data:
            def find(tag):
                try:
                    return job.find(tag).text
                except:
                    return None
            id = find("Job_Id")
            qdict[id] = {}
            qdict[id]["Name"] = find("Job_Name")
            qdict[id]["Owner"] = find("Job_Owner")
            qdict[id]["State"] = find("job_state")
            qdict[id]["Queue"] = find("queue")
            qdict[id]["Server"] = find("server")
            qdict[id]["Checkpoint"] = find("Checkpoint")
            qdict[id]["Timing"] = {"Creation":find("ctime"),
                                   "Eligible":find("etime"),
                                   "Modified":find("mtime"),
                                   "Queued": find("qtime")}
            qdict[id]["Error"] = find("Error_Path")
            qdict[id]["Holds"] = find("Hold_Types")
            qdict[id]["MixIO"] = find("Join_Path")
            qdict[id]["KeepIO"] = find("Keep_Files")
            qdict[id]["MailTime"] = find("Mail_Points")
            qdict[id]["Output"] = find("Output_Path")
            qdict[id]["Priority"] = find("Priority")
            qdict[id]["RebootRun"] = find("Rerunable")
            qdict[id]["SubmitArgs"] = find("submit_args")
            qdict[id]["FaultTolerant"] = find("fault_tolerant")
            qdict[id]["Radix"] = find("job_radix")
            qdict[id]["SubmitHost"] = find("submit_host")
            qdict[id]["Resources"] = {}
            for res in job.find("Resource_List"):
                qdict[id]["Resources"][res.tag] = res.text
            qdict[id]["Variables"] = {}
            try:
                for var in find("Variable_List").split(","):
                    var_data = var.split("=")
                    qdict[id]["Variables"][var_data[0]] = var_data[1]
            except:
                pass
    return qdict
