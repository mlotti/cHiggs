#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("crab.cfg", "muonSkim_cfg.py")

multicrab.addDatasets(
    "AOD",
    [
        # Data
#        "Mu_135821-144114", # HLT_Mu9
        "Mu_146240-147116", # HLT_Mu9
#        "Mu_147196-149442", # HLT_Mu15_v1
        # Signal MC
#        "TTbarJets",
#        "WJets",
        ])

multicrab.setDataLumiMask("../Cert_132440-149442_7TeV_StreamExpress_Collisions10_JSON.txt")

multicrab.getDataset("WJets").setNumberOfJobs(50)

#multicrab.modifyLumisPerJobAll(lambda nlumis: nlumis*0.5)
#multicrab.modifyNumberOfJobsAll(lambda njobs: njobs*2)

def addOutputName(dataset):
    path = dataset.getDatasetPath().split("/")
    name = path[2].replace("-", "_")
    name += "_"+path[3]
    name += "_tauembedding_skim_v1"

    dataset.addLine("USER.publish_data_name = "+name)
multicrab.forEachDataset(addOutputName)

multicrab.createTasks()
#multicrab.createTasks(configOnly=True)