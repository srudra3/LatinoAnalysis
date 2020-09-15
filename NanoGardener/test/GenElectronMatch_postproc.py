#!/usr/bin/env python
import os, sys 
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
#from LatinoAnalysis.NanoGardener.modules.qq2vv2lnujjEWKcorrectionsWeightProducer import *
#from LatinoAnalysis.NanoGardener.modules.qq2vvEWKcorrectionsWeightProducer2 import *
from LatinoAnalysis.NanoGardener.modules.GenElectronMatchProducer import *

files=[
    #'/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6/nanoLatino_WWTo2L2Nu__part2.root'
    #'/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__Semilep2017/nanoLatino_VBFHToWWToLNuQQ_M120__part0.root'
#    '/afs/cern.ch/work/s/srudrabh/ZH3l/CMSSW_10_2_0/src/LeptonMVA/samples/Signal/DYJetsToLL_M-50_v7.root'
    '/afs/cern.ch/work/s/srudrabh/ZH3l/CMSSW_10_2_0/src/LeptonMVA/samples/Background/TTToSemiLeptonic_v7.root'
#    '/afs/cern.ch/work/s/srudrabh/ZH3l/CMSSW_10_2_0/src/LeptonMVA/samples/Background/WJetsToLNu_v7.root'
]
#selection = None
selection = "nElectron > 0"
p=PostProcessor(
    ".",
    files,
    cut=selection,
    branchsel=None,
    modules=[
       GenElectronMatchProducer("Electron"), 
       #qq2vv2lnujjEWKcorrectionsWeightProducer("ww")
    ],  
    postfix='_ElePromptGenMatched',
    provenance=True,
    fwkJobReport=True
)
p.run()
print "DONE" 


