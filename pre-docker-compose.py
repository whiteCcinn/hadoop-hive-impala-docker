#! /usr/bin/env python

#- * -coding: utf - 8 - * -

import os, sys, yaml, json,copy

class Boot:
    composeFilePath = "./docker-compose.yml"
    templateFilePath = "./hadoop-slave-template.yml"

    def __init__(self):
        self.openHandler('composeFileHandler', Boot.composeFilePath)
        self.openHandler('templateFileHandler', Boot.templateFilePath)

        self.initDockerComposeContent()
        self.initTemplate()

    def __del__(self):
        self.closeHandler()

    def closeHandler(self, isComposeFileHandler = False, isTemplateFileHandler = False):
        if isComposeFileHandler == False and isTemplateFileHandler == False:
            self.composeFileHandler.close()
            self.templateFileHandler.close()
        elif isComposeFileHandler:
            self.composeFileHandler.close()
        else:
            self.templateFileHandler.close()

    def openHandler(self, attrName, path, mode = 'r+'):
        setattr(self, str(attrName), open(path, mode))

    def initDockerComposeContent(self):
        self.dockerComposeContent = yaml.load(self.composeFileHandler)
        self.closeHandler(isComposeFileHandler = True)

    def initTemplate(self):
        self.template = yaml.load(self.templateFileHandler)
        self.closeHandler(isTemplateFileHandler = True)

    def run(self, nodeNumber):
        nodeNumber = int(nodeNumber)

        containers = self.dockerComposeContent['services'].keys()
        hadoopSlaveContainerName = "hadoop-slave";
        slaveNamePool = []
        for container in containers:
            if container.startswith(hadoopSlaveContainerName):
                slaveNamePool.append(container)

        count = 1
        while (count <= nodeNumber):
            if hadoopSlaveContainerName + str(count) not in slaveNamePool:
                self.template['hadoop-slave' + str(count)] = copy.deepcopy((self.template['hadoop-slave$1']))
            count = count + 1

        del self.template['hadoop-slave$1']
        self.dockerComposeContent['services'].update(self.template)
        content = yaml.dump(self.dockerComposeContent, default_flow_style=False, indent=2, encoding='utf-8')
        self.openHandler('composeFileHandler', Boot.composeFilePath, 'w+')
        self.composeFileHandler.write(content)

    def displayDockerComposeContent(self):
            print yaml.dump(self.dockerComposeContent)


Boot().run(sys.argv[1])
