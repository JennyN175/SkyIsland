import maya.cmds as cmds
import random
import math

'''Team Members: Rebecca Yee, Jenny Nguyen
Date: April 12, 2022'''

#Create UI

chosenIsland = ""
def action_button(forestOption, winterOption, tropicalOption, randomOption):
    global chosenIsland
    if cmds.radioButton(forestOption, query=True,select=True):
        chosenIsland = "forest"
        pressedButton()
    elif cmds.radioButton(winterOption, query=True,select=True):
        chosenIsland = "winter"
        pressedButton()
    elif cmds.radioButton(tropicalOption, query=True,select=True):
        chosenIsland = "tropical"
        pressedButton() 
    elif cmds.radioButton(randomOption, query=True,select=True):
        #Get a random number to generate a random biome
        randomNum = random.randint(0,2)
        if (randomNum == 0):
            chosenIsland = "forest"
        elif (randomNum == 1):
            chosenIsland = "winter"
        elif (randomNum == 2):
            chosenIsland = "tropical"
        pressedButton()

if 'UI' in globals():
    if cmds.window(UI, exists=True):
        cmds.deleteUI(UI, window=True)
        
UI = cmds.window(title='Sky Island Generator', width=400)
cmds.columnLayout(rowSpacing=10)
cmds.text(label='Sky Island Generator')
cmds.text(label='Note: Island may take up a couple seconds to generate.')
cmds.text(label='Make sure there are no other islands in the scene before generating a new one.')

#Radio buttons
cmds.radioCollection()
forestOption = cmds.radioButton(label='Forest',align='left', select=True)
winterOption = cmds.radioButton(label='Winter',align='left')
tropicalOption = cmds.radioButton(label='Tropical',align='left')
randomOption = cmds.radioButton(label='Random Biome',align='left')
cmds.button(label='Generate Sky Island', command=lambda x:action_button(forestOption, winterOption, tropicalOption, randomOption), align='left')
cmds.showWindow()

#Material nodes
materialNodePalmTreeTrunk = cmds.shadingNode('aiStandardSurface', asShader=True)
materialNodePlant = cmds.shadingNode('aiStandardSurface', asShader=True)
materialNodePineTreeTrunk = cmds.shadingNode('aiStandardSurface', asShader=True)
materialNodePineTreeLeaves = cmds.shadingNode('aiStandardSurface', asShader=True)
materialNodeCrab = cmds.shadingNode('aiStandardSurface', asShader=True)
materialNodeMountainBody = cmds.shadingNode('aiStandardSurface', asShader=True)
materialNodeMountainSnow = cmds.shadingNode('aiStandardSurface', asShader=True)
materialNodeGrass = cmds.shadingNode('aiStandardSurface', asShader=True)            
materialNodeLog1 = cmds.shadingNode('aiStandardSurface', asShader=True)
materialNodeLog2 = cmds.shadingNode('aiStandardSurface', asShader=True)
materialNodePond = cmds.shadingNode('aiStandardSurface', asShader=True)
materialNodeDeadTree = cmds.shadingNode('aiStandardSurface', asShader=True)

#Create Sky Island Base
def generateSkyIslandBase():
    #made subdivision axis a variable in case we wanted to randomly generate it later
    subdivisionAxis = 12
    
    #Create sphere
    skyIslandBase = cmds.polySphere(sx = subdivisionAxis, sy = subdivisionAxis, r=20)
    
    materialNodeIsland = cmds.shadingNode('aiStandardSurface', asShader=True)
    cmds.select(skyIslandBase[0])
    cmds.hyperShade(assign=materialNodeIsland)
    cmds.setAttr(materialNodeIsland + '.baseColor', 0.4, 0.25, 0.15)
    
    #calculate the number of faces that make up top half of sphere
    numFacesTotal = subdivisionAxis * subdivisionAxis
    
    '''---Selecting all faces on the top half excluding the triangles faces on the top and bottom parts of the sphere---'''
    #Take total number of faces and subtract the number of triangle faces to get the last face for the selection
    endSelectedFace = numFacesTotal - subdivisionAxis*2 
    
    #Select the first face beginning at the top half of sphere 
    firstSelectedFace = int(endSelectedFace/2) 
    facesToDelete = cmds.select(skyIslandBase[0]+ '.f[' + str(firstSelectedFace) + ']')
    
    #Use for loop to iterate through all the faces that make up top half of sphere
    for x in range(firstSelectedFace + 1, endSelectedFace):
        cmds.select(skyIslandBase[0]+ '.f[' + str(x) + ']', add=True )
    
    #Selecting triangle faces on top half of sphere also
    secondSelectedFace = int(numFacesTotal - subdivisionAxis)
    for x in range(secondSelectedFace, numFacesTotal):
        cmds.select(skyIslandBase[0]+ '.f[' + str(x) + ']', add=True )
    
    cmds.delete() #Delete top half of sphere
    
    #Select each vertice (except for the ones on the top row) and offset position by a random amount   
    numVertices = cmds.polyEvaluate(skyIslandBase, v=True )
    for x in range(0, numVertices - (subdivisionAxis+1)):
        randomOffsetX = random.uniform(-2,2)
        randomOffsetY = random.uniform(-2,2) - 2
        randomOffsetZ = random.uniform(-2,2)
        vertexPosition = cmds.xform(skyIslandBase[0]+ '.vtx[' + str(x) + ']', query = True, translation = True, worldSpace = True)
        cmds.select(skyIslandBase[0]+ '.vtx[' + str(x) + ']')
        cmds.move(vertexPosition[0] + randomOffsetX, vertexPosition[1] + randomOffsetY, vertexPosition[2] + randomOffsetZ)

    #Moving the bottom vertice down to create a "point" for the island
    cmds.select(skyIslandBase[0]+ '.vtx[' + str(numVertices) + ']')
    bottomVertex = cmds.xform(skyIslandBase[0]+ '.vtx[' + str(numVertices) + ']', query = True, translation = True, worldSpace = True)
    cmds.move(bottomVertex[1] - 8, y=True)
    
    #Move bottom row of vertices down
    cmds.select(skyIslandBase[0]+ '.vtx[0]')
    for x in range(0, subdivisionAxis):
        vertexPosition = cmds.xform(skyIslandBase[0]+ '.vtx[' + str(x) + ']', query = True, translation = True, worldSpace = True)
        cmds.select(skyIslandBase[0]+ '.vtx[' + str(x) + ']')
        cmds.move(vertexPosition[1] - 3, y=True)
    return skyIslandBase

#Create Sky Island Top
def generateSkyIslandTop():
    skyIslandTop = cmds.polyCylinder(sx=12, r=21, h=3)
    cmds.select(skyIslandTop)
    materialNodeGround = cmds.shadingNode('aiStandardSurface', asShader=True)
    cmds.select(skyIslandTop)
    cmds.hyperShade(assign=materialNodeGround)
    
    if (chosenIsland == "forest"):
        cmds.setAttr(materialNodeGround + '.baseColor', 0, 1.0, 0.0)
    elif (chosenIsland == "winter"):
        cmds.setAttr(materialNodeGround + '.baseColor', 1, 1, 1)
    elif (chosenIsland == "tropical"):
        cmds.setAttr(materialNodeGround + '.baseColor', 0.941, 0.890, 0.8)
    
    cmds.rotate(180, z =True)
    testLake = cmds.polyCylinder(sx=12, r=8, h=3)
    cmds.polyCBoolOp(skyIslandTop, testLake[0], op=2)
    cmds.rename("skyIslandTop")
    
    for x in range (0,4):
        numEdges = cmds.polyEvaluate('skyIslandTop', e=True )
        for k in range(0, numEdges):
            sel = cmds.select('skyIslandTop' + '.e[' + str(k) + ']')
            p = cmds.xform(sel,q=True,t=True,ws=True)
            length=math.sqrt(math.pow(p[0]-p[3],2)+math.pow(p[1]-p[4],2)+math.pow(p[2]-p[5],2))
            if (length > 12):
                print(k)
                cmds.polyDelEdge('skyIslandTop' + '.e[' + str(k) + ']', cv=False)
                break
    
    lake = cmds.polyCylinder(sx=12, r=8, h=3)
    global materialNodePond
    cmds.select(lake)
    cmds.hyperShade(assign=materialNodePond)
    cmds.setAttr(materialNodePond + '.baseColor', 0,1.0, 1.0)
    cmds.move(-0.629984, y=True)
    return skyIslandTop

#Generate plant
def generateGroundPlant():
    leaf1 = cmds.polyCube(width=0.07, height=0.5,depth = 0.2)
    cmds.select(leaf1[0] +'.f[0]')
    cmds.polyExtrudeFacet(localTranslateZ=0.2)
    cmds.select(leaf1[0]+'.f[1]',leaf1[0]+'.f[8]')
    cmds.polyExtrudeFacet(localTranslateZ=0.5)
    cmds.polyExtrudeFacet(localTranslateZ=0.3)
    cmds.select(leaf1[0] + '.vtx[20:21]', leaf1[0] + '.vtx[6:7]')
    cmds.move(0.08, z=True)
    cmds.select(leaf1[0] + '.vtx[22:23]', leaf1[0] + '.vtx[8:9]')
    cmds.move(0.12, z=True)
    cmds.select(leaf1[0] + '.vtx[15:16]', leaf1[0] + '.vtx[12]')
    cmds.move(-0.12, x=True)
    cmds.select(leaf1[0] + '.vtx[13:14]', leaf1[0] + '.vtx[17]')
    cmds.move(-0.05, x=True)
    cmds.select(leaf1[0] + '.vtx[2]', leaf1[0] + '.vtx[4]', leaf1[0] + '.vtx[11]')
    cmds.move(-0.20, x=True)
    cmds.select(leaf1[0] + '.vtx[3]', leaf1[0] + '.vtx[5]', leaf1[0] + '.vtx[10]')
    cmds.move(-0.13, x=True)
    cmds.select(leaf1[0] + '.vtx[2]', leaf1[0] + '.vtx[4]', leaf1[0] + '.vtx[11]')
    cmds.select(leaf1[0])
    cmds.rotate(-70, z=True)
    cmds.scale(3,3,3)
    
    leaf2 = cmds.duplicate(leaf1[0])
    cmds.select(leaf2[0])
    cmds.rotate(121.098, -46.387, -113.159)
    cmds.move(-0.288, -0.263, 0.761)
    
    leaf3 = cmds.duplicate(leaf1[0])
    cmds.select(leaf3[0])
    cmds.rotate(282.796, 53.271, -79.158)
    cmds.move(-0.696, -0.059, -0.613)
    
    leaf4 = cmds.duplicate(leaf1[0])
    cmds.select(leaf4[0])
    cmds.rotate(226.424, 1.96, -94.125)
    cmds.move(-1.247, -0.52, 0.02)
    
    leaf5 = cmds.duplicate(leaf1[0])
    cmds.select(leaf5[0])
    cmds.rotate(165.553, -12.285, -113.469)
    cmds.move(-1.162, 0.066, 0.376)
    
    leaf6 = cmds.duplicate(leaf1[0])
    cmds.select(leaf6[0])
    cmds.rotate(388.811, -21.933, -54.945)
    cmds.move(0.089, 0.039, 0.047)
    cmds.scale(3.615,3.615,3.615)
    
    leaf7 = cmds.duplicate(leaf1[0])
    cmds.select(leaf7[0])
    cmds.rotate(326.871, -0.946, -87.709)
    cmds.move(-0.13, -0.411, -0.218)
    
    leaf8 = cmds.duplicate(leaf1[0])
    cmds.select(leaf8[0])
    cmds.rotate(400.662, -7.675, -81.188)
    cmds.move(0.278, -0.606, 0.085)
    
    leaf9 = cmds.duplicate(leaf1[0])
    cmds.select(leaf9[0])
    cmds.rotate(276.183, 5.173, -91.1)
    cmds.move(-0.697, -0.527, -0.585)
    
    leaf10 = cmds.duplicate(leaf1[0])
    cmds.select(leaf10[0])
    cmds.rotate(127.665, -4.343, -92.285)
    cmds.move(-0.454, -0.61, 0.64)
    
    leaf11 = cmds.duplicate(leaf1[0])
    cmds.select(leaf11[0])
    cmds.rotate(167.695, -0.183, -93.194)
    cmds.move(-0.969, -0.582, 0.332)
    
    leaf12 = cmds.duplicate(leaf1[0])
    cmds.select(leaf12[0])
    cmds.rotate(77.774, 0.781, -88.799)
    cmds.move(-0.01, -0.569, 0.846)
    
    leaf13 = cmds.duplicate(leaf1[0])
    cmds.select(leaf13[0])
    cmds.rotate(244.654, 16.42, -99.293)
    cmds.move(-0.858, 0.139, -0.76)
    
    cmds.select(leaf1,leaf2,leaf3,leaf4,leaf5,leaf6,leaf7,leaf8,leaf9,leaf10,leaf11,leaf12,leaf13)
    groundPlant = cmds.polyUnite()
    global materialNodePlant
    cmds.select(groundPlant)
    cmds.hyperShade(assign=materialNodePlant)
    cmds.setAttr(materialNodePlant + '.baseColor', 0.33, 1.0, 0.33)
    cmds.delete(ch=True)
    return groundPlant

#Generate palm tree
def generatePalmTree():
    trunk = cmds.polyCylinder(sx=6, r=0.3, h=1)
    leaves = generateGroundPlant()
    cmds.select(trunk[0] + '.vtx[6:11]')
    cmds.scale( 1.5 , 1.5 , scaleXZ=True)
    cmds.select(trunk[0] + '.e[6:11]')
    cmds.polyBevel(offset=0.1)
    cmds.select(trunk[0] + '.f[13]')
    cmds.polyExtrudeFacet(localTranslateZ=1)
    cmds.select(trunk[0] + '.vtx[18:23]')
    cmds.scale( 1.4 , 1.4 , scaleXZ=True)
    cmds.select(trunk[0] + '.e[32]',trunk[0] + '.e[34]',trunk[0] + '.e[36]',trunk[0] + '.e[38]',trunk[0] + '.e[40]',trunk[0] + '.e[41]')
    cmds.polyBevel(offset=0.1)
    cmds.select(trunk[0] + '.f[19]')
    cmds.polyExtrudeFacet(localTranslateZ=1)
    cmds.select(trunk[0] + '.vtx[30:35]')
    cmds.scale( 1.3 , 1.3 , scaleXZ=True)
    cmds.select(trunk[0] + '.e[60]',trunk[0] + '.e[62]',trunk[0] + '.e[64]',trunk[0] + '.e[65]',trunk[0] + '.e[56]',trunk[0] + '.e[58]')
    cmds.polyBevel(offset=0.1)
    cmds.select(trunk[0] + '.f[31]')
    cmds.polyExtrudeFacet(localTranslateZ=1)
    cmds.select(trunk[0] + '.vtx[42:47]')
    cmds.scale( 1.3 , 1.3 , scaleXZ=True)
    cmds.select(trunk[0] + '.e[80]',trunk[0] + '.e[82]',trunk[0] + '.e[84]',trunk[0] + '.e[86]',trunk[0] + '.e[88]',trunk[0] + '.e[89]')
    cmds.polyBevel(offset=0.1)
    cmds.select(trunk[0] + '.f[43]')
    cmds.polyExtrudeFacet(localTranslateZ=1)
    cmds.select(trunk[0] + '.vtx[54:59]')
    cmds.scale( 1.3 , 1.3 , scaleXZ=True)
    cmds.select(trunk[0] + '.e[104]',trunk[0] + '.e[106]',trunk[0] + '.e[108]',trunk[0] + '.e[110]',trunk[0] + '.e[112]',trunk[0] + '.e[113]')
    cmds.polyBevel(offset=0.1)
    cmds.select(trunk[0] + '.f[55]')
    cmds.polyExtrudeFacet(localTranslateZ=1)
    cmds.select(trunk[0] + '.vtx[66:71]')
    cmds.scale( 1.3 , 1.3 , scaleXZ=True)
    cmds.select(trunk[0] + '.e[128]',trunk[0] + '.e[130]',trunk[0] + '.e[132]',trunk[0] + '.e[134]',trunk[0] + '.e[136]',trunk[0] + '.e[137]')
    cmds.polyBevel(offset=0.1)
    cmds.select(trunk[0] + '.f[0]')
    cmds.polyExtrudeFacet(localTranslateZ=0.8)
    cmds.select(trunk[0] + '.vtx[78:83]')
    cmds.scale( 3 , 3 , scaleXZ=True)
    cmds.select(leaves[0])
    cmds.move(0.393, 6.013, -0.077)
    
    global materialNodePalmTreeTrunk
    cmds.select(trunk)
    cmds.hyperShade(assign=materialNodePalmTreeTrunk)
    cmds.setAttr(materialNodePalmTreeTrunk + '.baseColor', 1.0, 0.74, 0.56)
    cmds.select(leaves[0], trunk[0])
    palmTree = cmds.polyUnite()
    cmds.delete(ch=True)
    cmds.rename("palmTree")
    return palmTree

#Generate dead tree    
def generateDeadTree():
    #main trunk
    deadTree = cmds.polyCylinder(sx=6, r=0.5, h=3)
    cmds.select(deadTree[0] +'.vtx[0:5]')
    cmds.scale( 4 , 3 , scaleXZ=True)
    cmds.select(deadTree[0] +'.vtx[2]')
    cmds.move( -1.5, x=True)
    cmds.select(deadTree[0] +'.f[7]')
    cmds.polyExtrudeFacet(localTranslateZ = 7)
    cmds.select(deadTree[0]+ '.vtx[12]')
    for x in range(12, 18):
        vertexPosition = cmds.xform(deadTree[0]+ '.vtx[' + str(x) + ']', query = True, translation = True, worldSpace = True)
        cmds.select(deadTree[0]+ '.vtx[' + str(x) + ']')
        cmds.move(vertexPosition[0] + 1.5, x=True)
    cmds.select(deadTree[0] +'.f[7]')
    cmds.polyExtrudeFacet(localTranslateZ = 4)
    cmds.select(deadTree[0]+ '.vtx[18]')
    for x in range(18, 24):
        vertexPosition = cmds.xform(deadTree[0]+ '.vtx[' + str(x) + ']', query = True, translation = True, worldSpace = True)
        cmds.select(deadTree[0]+ '.vtx[' + str(x) + ']')
        cmds.move(vertexPosition[0] + 1.6, x=True)
    
    #branch 1
    branch1 = cmds.polyCylinder(sx=6, r=0.2, h=3)
    cmds.move(-1.174,3.298,-0.101)
    cmds.rotate(-4.796,-0.479,48.066)
    cmds.select(branch1[0] +'.f[7]')
    cmds.polyExtrudeFacet(localTranslateZ = 1.42)
    cmds.select(branch1[0]+ '.vtx[12]')
    for x in range(12, 18):
        vertexPosition = cmds.xform(branch1[0]+ '.vtx[' + str(x) + ']', query = True, translation = True, worldSpace = True)
        cmds.select(branch1[0]+ '.vtx[' + str(x) + ']')
        cmds.move(vertexPosition[0] + 1, x=True)
        cmds.move(vertexPosition[0] + 10, y=True)
    
    #branch2
    branch2 = cmds.polyCylinder(sx=6, r=0.3, h=3)
    cmds.move(1.171,10.834,0.001)
    cmds.rotate(22.317, z=True)
    cmds.select(branch2[0]+ '.vtx[10]')
    cmds.move(0.776,12.091,0.25)
    cmds.select(branch2[0]+ '.vtx[6]')
    cmds.move(0.776,12.091,-0.257)
    cmds.select(branch2[0]+ '.vtx[11]')
    cmds.move(0.948,11.987,-0.004)
    cmds.select(deadTree[0] + '.vtx[6:11]')
    cmds.scale( 1.3 , 1.3 , scaleXZ=True)
    cmds.select(deadTree, branch1, branch2)
    finalDeadTree = cmds.polyUnite()
    
    global materialNodeDeadTree
    cmds.select(finalDeadTree)
    cmds.hyperShade(assign=materialNodeDeadTree)
    cmds.setAttr(materialNodeDeadTree + '.baseColor', 0.3, 0.16, 0.03)
    
    cmds.delete(ch=True)
    cmds.rename("deadTree")
    return deadTree

#Generate pine tree    
def generatePineTree():
    #Start with cylinder
    pineTree = cmds.polyCylinder(sx=6, r=6.4, h=5.6)
    
    #Bottom section of pinetree
    cmds.select(pineTree[0]+ '.vtx[6]')
    for x in range(7, 12):
        cmds.select(pineTree[0] + '.vtx[' + str(x) + ']', add=True)
    cmds.scale( 0.5 , 0.5, 0.5 , scaleXYZ=True)
    
    #Mid section of pinetree
    cmds.select(pineTree[0]+ '.f[7]')
    cmds.polyExtrudeFacet(localTranslateZ = 4.5)
    cmds.select(pineTree[0]+ '.f[8]')
    for x in range(9, 14):
        cmds.select(pineTree[0] + '.f[' + str(x) + ']', add=True)
    cmds.polyExtrudeFacet(localTranslateZ = 2.3)
    cmds.select(pineTree[0]+ '.vtx[12]')
    for x in range(13, 18):
        cmds.select(pineTree[0] + '.vtx[' + str(x) + ']', add=True)
    cmds.select(pineTree[0]+ '.vtx[20]', pineTree[0]+ '.vtx[21]', add=True)
    for x in range(23, 30, 2):
        cmds.select(pineTree[0] + '.vtx[' + str(x) + ']', add=True)
    cmds.scale( 0.5 , 0.5, 0.5 , scaleXZ=True)
    
    #Top section of pinetree
    cmds.select(pineTree[0]+ '.f[7]')
    cmds.select(pineTree[0]+ '.f[15]', add=True)
    for x in range(17, 26, 2):
        cmds.select(pineTree[0] + '.f[' + str(x) + ']', add=True)
    cmds.polyExtrudeFacet(localTranslateZ = 5.8)
    cmds.select(pineTree[0]+ '.f[26]')
    for x in range(27, 32):
        cmds.select(pineTree[0] + '.f[' + str(x) + ']', add=True)
    cmds.polyExtrudeFacet(localTranslateZ = 2.2)
    cmds.select(pineTree[0]+ '.vtx[38]')
    for x in range(39, 48, 2):
        cmds.select(pineTree[0] + '.vtx[' + str(x) + ']', add=True)
    for x in range(30, 36):
        cmds.select(pineTree[0] + '.vtx[' + str(x) + ']', add=True)
    for x in range(24, 30):
        cmds.select(pineTree[0] + '.vtx[' + str(x) + ']', add=True)
    cmds.scale( 0.1 , 0.1, 0.1 , scaleXZ=True)
    
    #Tree trunk
    treeTrunk = cmds.polyCylinder(sx=6, r=1.2, h=5)
    cmds.move(-5, y=True)
    
    global materialNodePineTreeLeaves
    global materialNodePineTreeTrunk
    cmds.select(pineTree)
    cmds.hyperShade(assign=materialNodePineTreeLeaves)
    cmds.setAttr(materialNodePineTreeLeaves + '.baseColor', 0, 1, 0)
    
    cmds.select(treeTrunk)
    cmds.hyperShade(assign=materialNodePineTreeTrunk)
    cmds.setAttr(materialNodePineTreeTrunk + '.baseColor', 0.3, 0.16, 0.03)
    
    cmds.select(pineTree, treeTrunk)
    finalPineTree = cmds.polyUnite()
    cmds.delete(ch=True)
    cmds.rename("pineTree")
    return finalPineTree

'''---Turtle Graphics Functions---'''
iteration = 0;
forwardVectors = [[0,0,3], [-3,0,0], [0,0,-3], [3,0,0]]
axiom = 'F'
rule1 = ['F', 'F+G']
rule2 = ['G', 'F-G']
sentence = axiom

#Generating a sentence using the rules
def generateSentence(sentence):
    workingSentence = ''
    for x in sentence:
        #iterates through sentence, if encounters "F", replace it with "F+G"
        if (x == rule1[0]):
            workingSentence += rule1[1]
        elif (x == rule2[0]):
            #if encounters, "G", replace with "F-G"
            workingSentence += rule2[1]
        else:
            workingSentence += x
    global iteration
    iteration += 1
    return workingSentence

def drawLine(startPosition, directionVector):
    newLine = cmds.curve(p=[(startPosition[0], startPosition[1], startPosition[2]), (startPosition[0] + directionVector[0], startPosition[1] + directionVector[1], startPosition[2] + directionVector[2])], degree = 1)
    startPoint = cmds.pointOnCurve(newLine, parameter=0, position=True)
    endPoint = cmds.pointOnCurve(newLine, parameter=1.0, position=True)
    return [newLine, startPoint, endPoint]

'''---POINT OF INTERSECTION FUNCTIONS---'''
def drawRaycastLine(start, end):
    return cmds.curve(p=[(start[0], start[1], start[2]), (start[0] + end[0], start[1] + end[1], start[2] + end[2])], degree = 1)

def scalarMultiply(vector, scalar):
    return [vector[0] * scalar, vector[1] * scalar, vector[2] * scalar]

def getObjectWorldTranslation(object):
    return cmds.xform(object, query = True, worldSpace = True, rotatePivot = True)
    
def getVertices(object, faceID):
    vertexIDs = cmds.polyInfo('{}.f[{}]'.format(object, faceID), faceToVertex = True)
    vertexIDs = str(vertexIDs).split()
    vertexA = cmds.xform('{}.vtx[{}]'.format(object, vertexIDs[2]), query = True, translation = True, worldSpace = True)
    vertexB = cmds.xform('{}.vtx[{}]'.format(object, vertexIDs[3]), query = True, translation = True, worldSpace = True)
    vertexC = cmds.xform('{}.vtx[{}]'.format(object, vertexIDs[4]), query = True, translation = True, worldSpace = True)
    vertexD = []
    if (len(vertexIDs) == 7):
        vertexD = cmds.xform('{}.vtx[{}]'.format(object, vertexIDs[5]), query = True, translation = True, worldSpace = True)
    return [vertexA, vertexB, vertexC, vertexD]
    
def getDotProduct(vectorA, vectorB):
    return (vectorA[0] * vectorB[0]) + (vectorA[1] * vectorB[1]) + (vectorA[2] * vectorB[2])

def vectorFromPoints(pointA, pointB):
    return [pointB[0] - pointA[0], pointB[1] - pointA[1], pointB[2] - pointA[2]]

def getVectorMagnitude(vector):
    return ((vector[0] ** 2) + (vector[1] ** 2) + (vector[2] ** 2)) ** 0.5 #pythagorean theorem

def getCrossProduct(vectorA, vectorB):
    crossProduct = [0.0,0.0,0.0]
    crossProduct[0] = (vectorA[1] * vectorB[2]) - (vectorA[2] * vectorB[1])
    crossProduct[1] = (vectorA[2] * vectorB[0]) - (vectorA[0] * vectorB[2])
    crossProduct[2] = (vectorA[0] * vectorB[1]) - (vectorA[1] * vectorB[0])
    return crossProduct
    
def getNormalVector(triangleVertices):
    vectorA = vectorFromPoints(triangleVertices[0], triangleVertices[1])
    vectorB = vectorFromPoints(triangleVertices[0], triangleVertices[2]) #vertexA is the common base
    crossProduct = getCrossProduct(vectorA, vectorB)
    magnitude = getVectorMagnitude(crossProduct)
    return [crossProduct[0] / magnitude, crossProduct[1] / magnitude, crossProduct[2] / magnitude]

#Getting the area of a triangle
def getAreaTriangle(vertices):
    vector1 = vectorFromPoints(vertices[0], vertices[1])
    vector2 = vectorFromPoints(vertices[0], vertices[2])
    crossProduct = getCrossProduct(vector1, vector2)
    area = 0.5*(math.sqrt(crossProduct[0]*crossProduct[0] + crossProduct[1]*crossProduct[1] + crossProduct[2]*crossProduct[2]))
    return area

#Calculating the point of intersection using vertices of a plane, and points on a raycast
def getPointIntersection(planeVertices, pointA, pointB):
    normal = getNormalVector([planeVertices[0], planeVertices[1], planeVertices[2]])
    D = -((planeVertices[0][0]*normal[0]) + (planeVertices[0][1]*normal[1]) + (planeVertices[0][2]*normal[2]))
    t = (normal[0]*pointA[0] + normal[1]*pointA[1] + normal[2]*pointA[2] + D)/((normal[0] * (pointA[0] - pointB[0])) + (normal[1] * (pointA[1] - pointB[1])) + (normal[2] * (pointA[2] - pointB[2])))
    pointIntersection = [(pointA[0] + (t*(pointB[0]-pointA[0]))), (pointA[1]+ (t*(pointB[1]-pointA[1]))), (pointA[2]+ (t*(pointB[2]-pointA[2])))]
    return pointIntersection

#Function that checks whether the point of intersection lies within the boundaries of a triangle    
def checkIfIntersectingTriangle(triangleVertices, pointA, pointB): 
    isIntersecting = False 
    normal = getNormalVector([triangleVertices[0], triangleVertices[1], triangleVertices[2]])
    #calculate point of intersection
    pointIntersection = getPointIntersection([triangleVertices[0], triangleVertices[1], triangleVertices[2]], pointA, pointB)
    #calculate area of the triangle
    totalArea = getAreaTriangle(triangleVertices)
    #splitting triangle into three smaller triangles and calculating the area of each one
    innerAreas = [0, 0, 0]
    innerAreas[0] = getAreaTriangle([pointIntersection, triangleVertices[0], triangleVertices[1]])
    innerAreas[1] = getAreaTriangle([pointIntersection, triangleVertices[0], triangleVertices[2]])
    innerAreas[2] = getAreaTriangle([pointIntersection, triangleVertices[1], triangleVertices[2]])
    #if the sum of the triangle areas is roughly the same as the triangle's total area, it intersects
    if (((sum(innerAreas)) > (totalArea-0.5)) and ((sum(innerAreas)) < (totalArea+0.5))):
        isIntersecting = True
    else:
        isIntersecting = False
    
    return isIntersecting

#Function that checks whether an object is on the island
def checkIfOnIsland(objectVertices, raycastEndVertex):
    normal = getNormalVector([objectVertices[0], objectVertices[1], objectVertices[2]])
    skyIslandTop = cmds.ls('skyIslandTop')
    #Get a list of the vertices on the surface of the island
    islandVertexIDs = cmds.polyInfo('{}.f[{}]'.format(skyIslandTop[0], 15), faceToVertex = True)
    islandVertexIDs = str(islandVertexIDs).split()
    normalForIslandTop = getNormalVector([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[2]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[3]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[4]), query = True, translation = True, worldSpace = True)])
    dotProduct = getDotProduct(normalForIslandTop, normal) 
    
    #Dividing the island surface into small triangles in order to calculate the point of intersection of each one  
    listIslandAreas =  [False for i in range(24)]
    
    #information on whether or not an object has intersected with each triangle is stored in an array
    #for example, if all the array elements are false, then it means the object is not intersecting any part of the island
    #if the object is intersecting with the island, one element in the array should be true
    if (islandVertexIDs[3] == '13'):
        listIslandAreas[0] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[15]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[7]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[8]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[1] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[15]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[8]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[14]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[2] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[14]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[8]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[9]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[3] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[14]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[9]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[25]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[4] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[25]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[9]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[10]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[5] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[25]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[10]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[24]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[6] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[24]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[10]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[11]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[7] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[24]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[11]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[23]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[8] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[23]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[11]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[12]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[9] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[23]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[12]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[22]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[10] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[22]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[12]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[13]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[11] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[22]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[13]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[21]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[12] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[21]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[13]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[2]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[13] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[21]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[2]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[20]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[14] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[20]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[2]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[3]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[15] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[20]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[3]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[19]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[16] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[19]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[3]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[4]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[17] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[19]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[4]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[18]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[18] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[18]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[4]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[5]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[19] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[18]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[5]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[17]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[20] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[17]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[5]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[6]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[21] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[17]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[6]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[16]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[22] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[16]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[6]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[7]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[23] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[16]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[7]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[15]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
    else:
        #When the island top is generated, there is an alternate arrangement of vertices that may be generated (resulting from applying the boolean difference). The same process is repeated for this alternate arrangement
        listIslandAreas[0] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[15]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[7]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[8]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[1] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[15]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[8]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[14]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[2] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[14]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[8]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[9]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[3] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[14]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[9]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[25]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[4] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[25]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[9]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[10]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[5] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[25]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[10]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[24]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[6] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[24]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[10]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[11]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[7] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[24]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[11]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[23]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[8] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[23]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[11]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[12]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[9] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[23]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[12]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[22]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[10] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[22]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[12]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[13]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[11] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[22]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[13]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[21]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[12] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[21]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[13]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[2]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[13] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[21]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[2]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[20]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[14] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[20]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[2]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[3]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[15] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[20]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[3]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[19]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[16] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[19]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[3]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[4]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[17] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[19]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[4]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[18]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[18] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[18]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[4]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[5]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[19] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[18]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[5]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[17]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[20] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[17]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[5]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[6]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[21] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[17]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[6]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[16]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[22] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[16]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[6]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[7]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
        listIslandAreas[23] = checkIfIntersectingTriangle([cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[16]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[7]), query = True, translation = True, worldSpace = True), cmds.xform('{}.vtx[{}]'.format(skyIslandTop[0], islandVertexIDs[15]), query = True, translation = True, worldSpace = True)], objectVertices[2], raycastEndVertex)
    
    return listIslandAreas    
        
def generateForest(sentence):
    #Generate forest using turtle graphic sentence
    lineData = ['', [0,0,0], [0,0,0]]
    forwardVectorIndex = 0
    currentDirection = forwardVectors[forwardVectorIndex]
    position = [0,0,0]
    forestGroup = []
    
    for x in sentence:
        if(x == 'F' or x == 'G'):
            newLine = drawLine(lineData[2], currentDirection)
            lineData = newLine
            if (chosenIsland == "forest"):
                tree = generatePineTree()
                cmds.scale(0.2,0.2,0.2)
            elif (chosenIsland == "winter"):
                tree = generateDeadTree()
                cmds.scale(0.4,0.4,0.4)
            elif (chosenIsland == "tropical"):
                tree = generatePalmTree()
                cmds.scale(0.5,0.5,0.5)
            cmds.move(lineData[1][0], lineData[1][1]+2, lineData[1][2])
            selection = cmds.ls(sl=True)
            forestGroup.append(selection)
            cmds.delete(newLine[0])
        elif (x == '+'):
            forwardVectorIndex += 1
            if (forwardVectorIndex > 3):
                forwardVectorIndex = 0
            currentDirection = forwardVectors[forwardVectorIndex]
        elif (x == '-'):
            forwardVectorIndex -= 1
            if (forwardVectorIndex < 0):
                forwardVectorIndex = 3
            currentDirection = forwardVectors[forwardVectorIndex]
    
    for x in forestGroup:
        cmds.select(x, add=True)
    cmds.group()
    cmds.rename("forest")
    
    #Move forest ro random position
    randomRangeX = random.randint(-10,10)
    randomRangeZ = random.randint(-10,10)
    cmds.move(randomRangeX, x=True)
    cmds.move(randomRangeZ, z=True)
    if (chosenIsland == "forest"):
        cmds.move(1, y=True)
    
    forestOnIsland = False
    
    for x in forestGroup:
        if (chosenIsland == "forest"):
            vertexIDs = cmds.polyInfo('{}.f[{}]'.format(x[0], 50), faceToVertex = True)
        elif (chosenIsland == "winter"):
            vertexIDs = cmds.polyInfo('{}.f[{}]'.format(x[0], 6), faceToVertex = True)
        elif (chosenIsland == "tropical"):
            vertexIDs = cmds.polyInfo('{}.f[{}]'.format(x[0], 286), faceToVertex = True)
        vertexIDs = str(vertexIDs).split()
        vertexA = cmds.xform('{}.vtx[{}]'.format(x[0], vertexIDs[3]), query = True, translation = True, worldSpace = True)
        vertexB = cmds.xform('{}.vtx[{}]'.format(x[0], vertexIDs[5]), query = True, translation = True, worldSpace = True)
        vertexC = cmds.xform('{}.vtx[{}]'.format(x[0], vertexIDs[7]), query = True, translation = True, worldSpace = True)
        #print(vertexIDs)
        treeVertices = [vertexA, vertexB, vertexC]
        normal = getNormalVector([treeVertices[0], treeVertices[1], treeVertices[2]])
        raycastEndVertex = [treeVertices[0][0] + (normal[0]*5.0) , treeVertices[0][1] + (normal[1]*5.0) , treeVertices[0][2] + (normal[2]*5.0)]
        raycastScaled = scalarMultiply(normal, 5)
        #drawRaycastLine(treeVertices[0], raycastScaled )
        checkOnIsland = checkIfOnIsland(treeVertices, raycastEndVertex)
        
        #if not on island, remove it
        if (not any(checkOnIsland) == True):
            cmds.delete(x[0])

#generating logs    
def generateLogs():
    log1 = cmds.polySphere(sx=6, sy=4, r=1)
    cmds.rotate(-90,0,0)
    cmds.select(log1[0] +'.f[18:23]')
    cmds.move( '0', '3', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.scale(1.5,1.5,1.5)
    cmds.select(log1[0] +'.f[12:17]')
    cmds.move( '0', '-3', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.scale(1.5,1.5,1.5)
    cmds.select(log1[0] + '.vtx[18]')
    cmds.move( '0', '0.4', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.select(log1[0] + '.vtx[19]')
    cmds.move( '0', '-0.4', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.select(log1[0] +'.f[0:11]')
    cmds.polyExtrudeFacet()
    cmds.scale(1.2,1,1)
    cmds.scale(1,1,1.2)


    log2 = cmds.polySphere(sx=6, sy=4, r=1)
    cmds.move( '2.5', '0', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.rotate(-90,0,0)
    cmds.select(log2[0] +'.f[18:23]')
    cmds.move( '0', '3', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.scale(1.5,1.5,1.5)
    cmds.select(log2[0] +'.f[12:17]')
    cmds.move( '0', '-3', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.scale(1.5,1.5,1.5)
    cmds.select(log2[0] + '.vtx[18]')
    cmds.move( '0', '0.4', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.select(log2[0] + '.vtx[19]')
    cmds.move( '0', '-0.4', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.select(log2[0] +'.f[0:11]')
    cmds.polyExtrudeFacet()
    cmds.scale(1.2,1,1)
    cmds.scale(1,1,1.2)

    log3 = cmds.polySphere(sx=6, sy=4, r=1)
    cmds.move( '1.2', '2', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.rotate(-90,0,32)
    cmds.select(log3[0] +'.f[18:23]')
    cmds.move( '0', '3', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.scale(1.5,1.5,1.5)
    cmds.select(log3[0] +'.f[12:17]')
    cmds.move( '0', '-3', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.scale(1.5,1.5,1.5)
    cmds.select(log3[0] + '.vtx[18]')
    cmds.move( '0', '0.4', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.select(log3[0] + '.vtx[19]')
    cmds.move( '0', '-0.4', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.select(log3[0] +'.f[0:11]')
    cmds.polyExtrudeFacet()
    cmds.scale(1.2,1,1)
    cmds.scale(1,1,1.2)

    cmds.select(log1,log2,log3)
    logs = cmds.polyUnite()
    #Material Outside Assign
    global materialNodeLog1
    cmds.select(logs)
    cmds.hyperShade(assign=materialNodeLog1)
    cmds.setAttr(materialNodeLog1 + '.baseColor', 0.3, 0.16, 0.03)
    cmds.delete(ch=True)

    #Material Inside Assign
    global materialNodeLog2
    cmds.select(logs[0] +'.f[12:23]')
    cmds.hyperShade(assign=materialNodeLog2)
    cmds.setAttr(materialNodeLog2 + '.baseColor', 1, 0.78, 0.6)
    cmds.select(logs[0] +'.f[48:59]')
    cmds.hyperShade(assign=materialNodeLog2)
    cmds.select(logs[0] +'.f[84:95]')
    cmds.hyperShade(assign=materialNodeLog2)
    cmds.delete(ch=True)
    cmds.select(logs[0])
    return logs

#generating grass    
def generateGrass():
    Grass1 = cmds.polyCube(width=0.1, height=1.0,depth = 0.3)
    cmds.rotate(0,0,12)
    cmds.select(Grass1[0] +'.f[1]')
    cmds.polyExtrudeFacet(translate=(-0.4,0.7,0))
    cmds.scale(0.5,1,0.5)
    cmds.polyExtrudeFacet(translate=(-0.1,0.3,0))
    cmds.scale(0.5,1,0.5)
    cmds.move( '-0.4', '0.1', '0', relative=True, objectSpace=True, worldSpaceDistance=True )

    Grass2 = cmds.polyCube(width=0.1, height=0.7,depth = 0.3)
    cmds.rotate(90,-80,-90)
    cmds.move( '0.4', '0', '-0.3', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.select(Grass2[0] +'.f[1]')
    cmds.polyExtrudeFacet(translate=(0,0.5,0.5))
    cmds.scale(0.5,1,0.5)
    cmds.polyExtrudeFacet(translate=(0,0.3,0.4))
    cmds.scale(1,1,0.5)

    Grass3 = cmds.polyCube(width=0.1, height=0.7,depth = 0.3)
    cmds.move( '0.5', '0', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.rotate(-9,30,-15)
    cmds.select(Grass3[0] +'.f[1]')
    cmds.polyExtrudeFacet(translate=(0.5,0.5,-0.3))
    cmds.scale(0.5,1,0.5)

    cmds.select(Grass1,Grass2,Grass3)
    Grass = cmds.polyUnite()
    
    global materialNodeGrass
    cmds.select(Grass)
    cmds.hyperShade(assign=materialNodeGrass)
    cmds.setAttr(materialNodeGrass + '.baseColor', 0,1.0, 0.0)
    cmds.delete(ch=True)
    return Grass

#Generating crab
def generateCrab():
    Crab = cmds.polySphere(sx=6, sy=4, r=1)
    cmds.scale(0.5,1,1)
    cmds.rotate(0,0,90)
    cmds.select(Crab[0] +'.f[9]')
    cmds.polyExtrudeFacet(translate=(-2,0,0.5))
    cmds.scale(1,0.3,1)
    cmds.polyExtrudeFacet(translate=(-0.3,0,-0.5))
    cmds.scale(1,1,1.5)
    cmds.rotate(-20,0,0)
    cmds.polyExtrudeFacet(translate=(-6,0,-0.1))
    cmds.scale(0.2,0.2,0.2)

    cmds.select(Crab[0] +'.f[6]')
    cmds.polyExtrudeFacet(translate=(-2,0,-0.5))
    cmds.scale(1,0.3,1)
    cmds.polyExtrudeFacet(translate=(-0.3,0,0.5))
    cmds.scale(1,1,1.5)
    cmds.rotate(20,0,0)
    cmds.polyExtrudeFacet(translate=(-6,0,0.1))
    cmds.scale(0.2,0.2,0.2)

    cmds.select(Crab[0] +'.f[3]')
    cmds.polyExtrudeFacet(translate=(0.2,0,1.2))
    cmds.scale(0.5,0.5,0.5)
    cmds.polyExtrudeFacet(translate=(-0.2,0,0.5))
    cmds.polyExtrudeFacet(translate=(-2,0,8))
    cmds.scale(0.2,0.2,0.2)

    cmds.select(Crab[0] +'.f[0]')
    cmds.polyExtrudeFacet(translate=(0.2,0,-1.2))
    cmds.scale(0.5,0.5,0.5)

    cmds.polyExtrudeFacet(translate=(-0.2,0,-0.5))
    cmds.polyExtrudeFacet(translate=(-2,0,-8))
    cmds.scale(0.2,0.2,0.2)
    cmds.select(Crab[0])
    
    global materialNodeCrab
    cmds.select(Crab)
    cmds.hyperShade(assign=materialNodeCrab)
    cmds.setAttr(materialNodeCrab + '.baseColor', 1.0, 0.0, 0.0)
    cmds.delete(ch=True)
    return Crab

#Generate mountain
def generateMountain():
    Mountain = cmds.polyCube(width=2, height=1,depth = 2)
    cmds.select(Mountain[0] +'.vtx[6:7]')
    cmds.move( '0.1', '0', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.select(Mountain[0] +'.vtx[0:1]')
    cmds.move( '-0.1', '0', '0', relative=True, objectSpace=True, worldSpaceDistance=True )

    cmds.select(Mountain[0] +'.f[1]')
    cmds.polyExtrudeFacet(translate=(0,1,0))
    cmds.scale(0.8,0.8,0.8)
    cmds.polyExtrudeFacet(translate=(0,1,0))
    cmds.scale(0.9,0.9,0.9)
    cmds.polyBevel(segments=2,offset=0.2)
    cmds.select(Mountain[0] +'.f[17]')
    cmds.move( '0', '0.2', '0', relative=True, objectSpace=True, worldSpaceDistance=True )
    
    global materialNodeMountainBody
    global materialNodeMountainSnow

    cmds.select(Mountain)
    cmds.hyperShade(assign=materialNodeMountainBody)
    cmds.setAttr(materialNodeMountainBody + '.baseColor', 0.4, 0.4,0.4)


    cmds.select(Mountain[0] +'.f[10:11]',Mountain[0] +'.f[13]',Mountain[0] +'.f[15]',Mountain[0] +'.f[17]')
    cmds.hyperShade(assign=materialNodeMountainSnow)
    cmds.setAttr(materialNodeMountainSnow + '.baseColor', 1, 1,1)

    mini = cmds.duplicate(Mountain[0])
    cmds.select(mini[0])
    cmds.move( '0', '-0.25', '-1.5', relative=True, objectSpace=True, worldSpaceDistance=True )
    cmds.scale(0.5,0.5,0.5)

    cmds.select( Mountain, mini )
    FinalMountain = cmds.polyUnite()
    cmds.delete(ch=True)
    return FinalMountain

def checkDistanceFromForest(object, forestGroup, faceID):
    #checking distance from forest objects
    tooCloseToTree = False
    
    #get point of object
    vertexIDsSel = cmds.polyInfo('{}.f[{}]'.format(object, 0), faceToVertex = True)
    selPoints = str(vertexIDsSel).split()
    selPoint = cmds.xform('{}.vtx[{}]'.format(object, selPoints[2]), query = True, translation = True, worldSpace = True)
    distanceFromTree = 10
    lengthList = int((len(forestGroup)/2))
            
    for x in forestGroup[0:lengthList]:
        #get point of tree
        vertexIDs = cmds.polyInfo('{}.f[{}]'.format(x, faceID), faceToVertex = True)
        objectPoints = str(vertexIDs).split()
        objectPoint = cmds.xform('{}.vtx[{}]'.format(x, objectPoints[2]), query = True, translation = True, worldSpace = True)
        
        #calculate distance
        distanceFromTree = (((selPoint[0]-objectPoint[0])**2) + ((selPoint[1]-objectPoint[1])**2) + ((selPoint[2]-objectPoint[2])**2)) ** 0.5
        if (distanceFromTree < 3):
            tooCloseToTree = True
            break
    return tooCloseToTree       

#Randomly generating objects in different            
def positionObjectsRandomly():
    forestGroup = []
    if (chosenIsland == "forest"):
        forestGroup.extend(cmds.ls('pineTree*'))
    elif (chosenIsland == "winter"):
        forestGroup.extend(cmds.ls('deadTree*'))
    elif (chosenIsland == "tropical"):
        forestGroup.extend(cmds.ls('palmTree*'))
    
    #Generating 50 random assets
    for x in range(0, 50):
        #for each x, choose a random asset to generate
        randomAsset = random.randint(1,3)
        randomRangeX = random.randint(-20,20)
        randomRangeZ = random.randint(-20,20)
        if (randomAsset == 1):
            faceID = 0
            #generate asset associated to chosen biome
            if (chosenIsland == "forest"):
                logs = generateLogs()
                cmds.move(1.6, y=True)
                cmds.scale(0.1,0.1,0.1)
            elif (chosenIsland == "winter"):
                mountains = generateMountain()
                cmds.move(1.6, y=True)
                cmds.scale(0.2,0.2,0.2)
            elif (chosenIsland == "tropical"):
                plant = generateGroundPlant()
                cmds.move(1.6, y=True)
                cmds.scale(0.2,0.2,0.2)
            cmds.move(randomRangeX, x=True)
            cmds.move(randomRangeZ, z=True)
            selection = cmds.ls(sl=True)
            
            #getting information to determine whether the asset generated on the island
            if (chosenIsland == "forest"):
                vertices = getVertices(selection[0], 0)
                faceID = 0
            elif (chosenIsland == "winter"):
                vertices = getVertices(selection[0], 2)
                faceID = 2
            elif (chosenIsland == "tropical"):
                vertices = getVertices(selection[0], 224)
                faceID = 224
            normal = getNormalVector([vertices[0], vertices[1], vertices[2]])
            raycastEndVertex = [vertices[0][0] + (normal[0]*5.0) , vertices[0][1] + (normal[1]*5.0) , vertices[0][2] + (normal[2]*5.0)]
            checkOnIsland = checkIfOnIsland(vertices, raycastEndVertex)
            #if not on island, remove it
            if (not any(checkOnIsland) == True):
                cmds.delete(selection[0])
        
        #repeat process for other assets too
        elif (randomAsset == 2):
            faceID = 0
            if (chosenIsland == "forest"):
                grass = generateGrass()
                cmds.move(1.6, y=True)
                cmds.scale(0.2,0.2,0.2)
            elif (chosenIsland == "winter"):
                mountains = generateMountain()
                cmds.move(1.6, y=True)
                cmds.scale(0.4,0.4,0.4)
            elif (chosenIsland == "tropical"):
                crab = generateCrab()
                cmds.move(1.6, y=True)
                cmds.scale(0.2,0.2,0.2)
            cmds.move(randomRangeX, x=True)
            cmds.move(randomRangeZ, z=True)
            selection = cmds.ls(sl=True)
            if (chosenIsland == "forest"):
                vertices = getVertices(selection[0], 3)
                faceID = 3
            elif (chosenIsland == "winter"):
                vertices = getVertices(selection[0], 2)  
                faceID = 2
            elif (chosenIsland == "tropical"):
                vertices = getVertices(selection[0], 7)  
                faceID = 7
            normal = getNormalVector([vertices[0], vertices[1], vertices[2]])
            raycastEndVertex = [vertices[0][0] + (normal[0]*5.0) , vertices[0][1] + (normal[1]*5.0) , vertices[0][2] + (normal[2]*5.0)]
            checkOnIsland = checkIfOnIsland(vertices, raycastEndVertex)
            if (not any(checkOnIsland) == True):
                cmds.delete(selection[0])
        
        elif (randomAsset == 3): 
            faceID = 0
            if (chosenIsland == "forest"):
                tree = generatePineTree()
                cmds.move(2.6, y=True)
                cmds.scale(0.2,0.2,0.2)
            elif (chosenIsland == "winter"):
                tree = generateDeadTree()
                cmds.move(1.5, y=True)
                cmds.scale(0.4,0.4,0.4)
            elif (chosenIsland == "tropical"):
                tree = generatePalmTree()
                cmds.move(2.4, y=True)
                cmds.scale(0.5,0.5,0.5)
            cmds.move(randomRangeX, x=True)
            cmds.move(randomRangeZ, z=True)
            selection = cmds.ls(sl=True)
            if (chosenIsland == "forest"):
                vertices = getVertices(selection[0], 50)
                faceID = 50
            elif (chosenIsland == "winter"):
                vertices = getVertices(selection[0], 6)
                faceID = 6
            elif (chosenIsland == "tropical"):
                vertices = getVertices(selection[0], 286)
                faceID = 286
            normal = getNormalVector([vertices[0], vertices[1], vertices[2]])
            raycastEndVertex = [vertices[0][0] + (normal[0]*5.0) , vertices[0][1] + (normal[1]*5.0) , vertices[0][2] + (normal[2]*5.0)]
            #raycastScaled = scalarMultiply(normal, 5)
            checkOnIsland = checkIfOnIsland(vertices, raycastEndVertex)
            if (not any(checkOnIsland) == True):
                cmds.delete(selection[0])
    
#Generate Sky Island
def generateSkyIsland():
    base = generateSkyIslandBase()
    top = generateSkyIslandTop()
    finalIsland = cmds.group(base, top)
    cmds.rename("skyIsland")
    return finalIsland

#Function that is called when the user presses the generate button
def pressedButton():
    island = generateSkyIsland()
    global sentence
    global axiom
    sentence = axiom
    #7 iterations for turtle graphics
    for x in range(0, 7):
        sentence = generateSentence(sentence)
    
    generateForest(sentence)
    print(sentence)
    positionObjectsRandomly()
    obj = cmds.select(all = True)
    finalIsland = cmds.group()
    cmds.delete(ch=True)
    cmds.rename("finalSkyIsland")