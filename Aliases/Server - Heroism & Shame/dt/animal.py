embed -footer "Usage - !dt animal -name \"name\" [adv] [-rr #] [setup -animal \"name\" -cr -train [tamed/trained]"
<drac2>
# sets primary variables
me, pargs = character(), argparse(&ARGS&)

# sets roll variables
baseroll, advroll  = "1d20+", "2d20kh1+"

# sets the booleans
withAdv = True if pargs.get("adv") else False
hasAnimal = True if exists("DTAnimalTrain") else False
choseAnimalType = True if pargs.get("animal") else False
choseAnimalName = True if pargs.get("name") else False
choseCR = True if pargs.get("cr") else False
hasPrevTraining = True if pargs.get("train") else False
enterSetup = True if pargs.get("setup") else False

# sets the repeats
repeats = pargs.get("rr")[0] if pargs.get("rr") else 1

# sets the return strings
returnstr = ""
setupstr = f' -title "{name} must setup their animal training"' \
           f' -f "Do|Setup the settings with `!dt animal setup -animal \\"name\\" -cr #`"' \
           f' -f "Then|Run your training rolls with `!dt animal -name \\"name\\" -rr X`"'

# sets check variables
crCheck = ["1/8","1/4","1/2"]
animal= ""

# Creates needed CVAR
me.set_cvar("DTAnimalTrain", {}) if not hasAnimal else 0
loadedAnimal = load_json(DTAnimalTrain)

# Error Checks missing things before running the code body
if enterSetup:
    activity = "setup"
    if not choseAnimalType or not choseCR:
        return setupstr
if not enterSetup:
    if not choseAnimalName:
        return setupstr
    currentTrainingLevel = loadedAnimal[animal]["traininglevel"]
    activity = "taming" if currentTrainingLevel == "none" \
    else "training" if currentTrainingLevel == "tamed" \
    else "drilling" if currentTrainingLevel == "trained" else "none"
returnstr += f' -title "{name} conducts {activity} training with an animal"' if not activity == "setup" else \
             f' -title "{name} conducts {activity}" '
# runs the setup portion
if activity == "setup":
    # passes values to local v from pargs
    animal, cr = pargs.get("animal")[0].lower(), pargs.get("cr")[0]
    # error check if an invalid CR was passed
    if cr in crCheck:
        cr = "1"
    if int(cr) not in range(0,31):
        return setupstr
    canTrain = True if int(cr) <= floor(me.levels.total_level/2) else False
    if canTrain == False:
        return f' -title "{name} conducts {activity}" -f "Oops|You can\'t train that animal at your level. Darnit." '
    if pargs.get("train"):
        currentLevel = "tamed" if pargs.get("train")[0] == "tamed" \
        else "trained" if pargs.get("train")[0] == "trained" \
        else "none"
    else:
        currentLevel = "none"
    daysToTrain = int(cr) * 10
    trainDC = 14+int(cr) if currentLevel == "trained" else 12+int(cr) if currentLevel == "tamed" else 10+int(cr)
    me.create_cc_nx(f'Animal Training-{animal}', "0", f'{daysToTrain}', "none",desc=f'Trained Level: {currentLevel}')
    me.set_cc(f'Animal Training-{animal}', "0")
    setupAnimal.update({animal:{"cr":cr,"traininglevel":currentLevel, "dc":trainDC}})
    me.set_cvar("DTAnimalTrain", dump_json(setupAnimal))
    returnstr += f' -f "Setup Complete|You will be training `{animal}` for `{daysToTrain}` days with a DC `{trainDC}`\n'\
                 f'Begin training with `!dt animal {animal}`"'
    return returnstr
    #runs the training portion


for x in range(repeats):
    #first checks to see if the CC has been completed, otherwise, wont roll
    if me.cc(f'Animal Training-{animal}').value >= me.cc(f'Animal Training-{animal}').max:
        returnstr += f' -f "COMPLETE| Training Complete, will not roll anymore."'
    #builds the roll
    animalroll = vroll(baseroll+str(me.skills.animalHandling.value))
    passedRoll = True if animalroll.total >= setupAnimal[animal]["dc"] else False
    if passedRoll:
        me.set_cc(f'Animal Training-{animal}', +1)
        #does things when training is complete
        if me.cc(f'Animal Training-{animal}').value >= me.cc(f'Animal Training-{animal}').max:
            nextLevel = "tamed" if currentLevel == "none" else "trained" if currentLevel == "tamed" \
            else "drilled" if currentLevel == "trained" else ""
            setupAnimal.update({animal:{"completion":True, "trainingLevel":nextLevel}})
    # builds the return str
    returnstr += f' -f "Attempt {x-1}|DC: {dc}\n{animalroll.full}\n{"Passed, +1 to training" if passedRoll else "Failed"}|inline"'
# builds the title string for activity

# returns all
return returnstr
</drac2>

{
    "AnimalName":{
        "CR" : "1"
        "TrainingLevel" : "None",
        "DC" : 10
    }
}