#!/usr/bin/env python

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

def main():
    lands.generateMultiCrab(
        massPoints = lands.allMassPoints,
        datacardPatterns = [lands.taujetsDatacardPattern],
        rootfilePatterns = [lands.taujetsRootfilePattern],
        clsType = lands.LEPType(toysPerJob=50),
        numberOfJobs = 20,
        postfix = "taujets_toys1k",
        crabScheduler="arc",
#        crabOptions = {"GRID": [
#                "ce_white_list = jade-cms.hip.fi",
#                "ce_white_list = korundi.grid.helsinki.fi",
#                ]},
        )

if __name__ == "__main__":
    main()
