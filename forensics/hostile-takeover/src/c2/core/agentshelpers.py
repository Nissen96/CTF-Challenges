from common import *
from encryption import *

from collections import OrderedDict
from shutil import rmtree
from base64 import b64decode

agents = OrderedDict()

def checkAgentsEmpty(s):
    uagents()
    global agents
    if len(agents) == 0:
        if s == 1:
            error("There are no active agents.")
        return True
    
    return False

def isValidAgent(name, s):
    uagents()
    vAgents = []
    for agent in agents:
        vAgents.append(agents[agent].name)

    if name in vAgents:
        return True

    if s == 1:
        error("Invalid agent.")
    return False

def viewAgents():
    if checkAgentsEmpty(1) == False:
        success("Active Agents:")
        print(YELLOW)
        print(" Name                         Listener                         External IP                         Hostname")
        print("------                       ----------                       -------------                       ----------")
        for i in agents:
            print(" {}".format(agents[i].name) + " " * (29 - len(agents[i].name)) + "{}".format(agents[i].listener) + " " * (33 - len(agents[i].listener)) + agents[i].remoteip + " " * (36 - len(agents[i].remoteip)) + agents[i].hostname)
        print(cRESET)

def renameAgent(args):
    if len(args) != 2:
        error("Invalid arguments.")
        return
        
    name    = args[0]
    newname = args[1]

    if not isValidAgent(name, 1):
        return 0

    if isValidAgent(newname, 0):
        error("Agent {} already exists.".format(newname))
        return 0
    
    agents[name].rename(newname)
    
    if os.path.exists(agents[name].Path):
        rmtree(agents[name].Path)

    removeFromDatabase(agentsDB, name)
    agents[name].name = newname
    agents[name].update()
    writeToDatabase(agentsDB, agents[name])
    
    uagents()


def removeAgent(args):
    if len(args) != 1:
        error("Invalid arguments.")
        return

    name = args[0]
    if isValidAgent(name, 1):
        taskAgentToQuit(name)
        rmtree(agents[name].Path)
        removeFromDatabase(agentsDB,name)
        uagents()


def getAgentsForListener(name):
    result = []
    for agent in agents:
        if agents[agent].listener == name:
            result.append(agents[agent].name)
    return result

def interactWithAgent(args):
    if len(args) != 1:
        error("Invalid arguments.")
        return

    name = args[0]
    if isValidAgent(name, 1):
        agents[name].interact()


def clearAgentTasks(name):
    if isValidAgent(name, 0):
        agents[name].clearTasks()


def displayResults(name, result):
    if not isValidAgent(name,0):
        return
    
    if result == "":
        success("Agent {} completed task.".format(name))
        return
        
    key = agents[name].key
    if agents[name].Type == "p":
        try:
            plaintext = DECRYPT(result, key)
        except:
            error("Error decrypting response.")
            return 0
    
        if plaintext[:5] == "VALID":
            success("Agent {} returned result:".format(name))
            print(plaintext[6:])
        else:
            error("Agent {} returned invalid result:".format(name))
            print(plaintext)
            return 0

    success("Agent {} returned result:".format(name))
    print(result)


def taskAgentToQuit(name):
    agents[name].Quit()


def uagents():
    global agents    
    try:
        temp = readFromDatabase(agentsDB)
        agents = OrderedDict()
        for agent in temp:
            agents[agent.name] = agent
    except:
        pass
