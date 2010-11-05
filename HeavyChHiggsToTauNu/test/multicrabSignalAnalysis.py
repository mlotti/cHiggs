#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

multicrab = Multicrab("crab_analysis.cfg")

# Select the pattuple version to use as an input
pattupleVersion = "pattuple_v3"
#pattupleVersion = "pattuple_v6"


# Change this to true if you want to run the PAT on the fly (for
# datasets where no pattuples are produced, or for testing something
# where information not stored in pattuples is needed). 
runPatOnTheFly = False
#runPatOnTheFly = True
if runPatOnTheFly:
    # At the moment we need the RECO for running PAT due to the
    # electron ID
    #pattupleVersion = "AOD"
    pattupleVersion = "RECO"


# Uncomment below the datasets you want to process
# The dataset definitions are in python/tools/multicrabDatasets.py
multicrab.addDatasets(pattupleVersion,
    [
        # Data
#        "BTau_141950-144114",  # v3
#        "BTau_146240-147454",  # v3
#        "BTau_146240-148107", # not yet ready 
#        "BTau_148108-148864", # not yet ready
        # MC Signal Fall10
#        "TTToHplusBWB_M90",  # not yet ready
#        "TTToHplusBWB_M100", # not yet ready
#        "TTToHplusBWB_M120", # not yet ready
#        "TTToHplusBWB_M140", # not yet ready
#        "TTToHplusBWB_M160", # not yet ready
        # MC Signal Spring10
#        "TTToHpmToTauNu_M90",  # v3, v6
#        "TTToHpmToTauNu_M100", # v3, v6
#        "TTToHpmToTauNu_M120", # v3, v6
#        "TTbar_Htaunu_M140",   # v3, v6
#        "TTbar_Htaunu_M160",   # v3, v6
        # MC Background Fall10
#        "QCD_Pt30to50_Fall10",   # v3, v6
#        "QCD_Pt50to80_Fall10",   # v3, v6
#        "QCD_Pt80to120_Fall10",  # v3
#        "QCD_Pt120to170_Fall10", # v3
#        "QCD_Pt170to300_Fall10", # v3, v6
        # MC Background Summer10
#        "QCD_Pt30to50",   # v3, v6
#        "QCD_Pt50to80",   # v3, v6
#        "QCD_Pt80to120",  # v3, v6
#        "QCD_Pt120to170", # v3, v6
#        "QCD_Pt170to230", # v3
#        "QCD_Pt230to300", # v3, v6
#        "TTbar",          # v3, v6
#        "TTbarJets",      # v3, v6
#        "WJets",          # v3
        ])

# Force all jobs go to jade, in some situations this might speed up
# the analysis (e.g. when there are O(1000) Alice jobs queueing, all
# CMS jobs typically go to korundi).
if not runPatOnTheFly:
    multicrab.addBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])


# If PAT is ran on the fly, set the lumi mask for data and add the
# "doPat=1" command line argument for all datasets. In addition it
# could be wise to decrease the number of jobs as the defaults are
# adjusted for the pattuple file size, and when only histograms or
# small ntuples are produced, stageout is not the issue
if runPatOnTheFly:
    multicrab.setDataLumiMask("Cert_132440-148864_7TeV_StreamExpress_Collisions10_JSON.txt")
    multicrab.addArgAll("doPat=1")

    #multicrab.modifyLumisPerJobAll(lambda nlumis: nlumis*2)
    #multicrab.modifyNumberOfJobsAll(lambda njobs: njobs*0.5)

# Generate configuration only
#multicrab.createTasks(configOnly=True)

# Genenerate configuration and create the crab tasks
multicrab.createTasks()