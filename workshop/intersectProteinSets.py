#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:13:27 2020

@author: jan
"""
#------------------------------------------------------------------------------
#   Import Libraries
#------------------------------------------------------------------------------
import argparse
import os
import pandas as pd


#------------------------------------------------------------------------------
#   Functions
#------------------------------------------------------------------------------
def loadProteinSet(proteinSetPath):
    """Load protein set
    
    Parameters
    ----------
    proteinSetPath : str
        Name of the proteinSet file
        
    Returns
    -------
    pandas.DataFrame
        Returns DataFrame object of Pandas containing the Protein set.
    """
    proteinSetFullPath=os.path.realpath(proteinSetPath)
    return pd.read_csv(proteinSetFullPath, sep="\t")

def mergeProteinSets(proteinSetA,proteinSetAName, proteinSetB, proteinSetBName):
    """ Merge "Entry" columns of protein set A and B on Organism column
    
    Parameters
    ----------
    proteinSetA : pandas.DataFrame
        DataFrame object of protein set A
    proteinSetB : pandas.DataFrame
        DataFrame object of protein set B
    
    Returns
    -------
    pandas.DataFrame
        DataFrame object containing all the organisms with both an entry for
        proteinSetA and proteinSetB.
    """
    merged = pd.DataFrame()
    merged[["Organism",proteinSetAName,proteinSetBName]] = pd.merge(proteinSetA,proteinSetB,
          on="Organism")[["Organism","Entry_x","Entry_y"]]
    return merged

def writeProteinSets(mergedProteinSet):
    """ Returns a proteinSet.list file for merged protein sets
    
    Parameters
    ----------
    mergedProteinSet : pandas.DataFrame
        DataFrame object containing the merged protein sets
        
    Effect
    ------
    Generate proteinSetA.list and proteinSetB.list files
    Generate merged.tab file
    
    Returns
    -------
    List of generated filenames
    """
    columns = mergedProteinSet.columns
    fileNames = list()
    for column in columns:
        fileName=column+"_merged.list"
        fileNames+=[fileName]
        uniqueList = mergedProteinSet[column].unique()
        uniqueDataFrame = pd.DataFrame(data=uniqueList,columns = [column])
        uniqueDataFrame.to_csv(fileName, sep="\t", index=False)
    aggregatedProteinSet = mergedProteinSet.groupby("Organism").aggregate(list)
    fileName = "_".join(columns)+".tab"
    fileNames+=[fileName]
    aggregatedProteinSet.to_csv(fileName,sep="\t")
    return fileNames

def intersectProteinSets(proteinSetAPath, proteinSetBPath):
    """ Intersect Protein sets and generate files
    
    Parameters
    ----------
    proteinSetAPath : str
        Name of the proteinSetA file
    proteinSetAPath : str
        Name of the proteinSetB file
    
    Effect
    ------
    Generate proteinSetA.list and proteinSetB.list files
    Generate merged.tab file
    
    Returns
    -------
    List of generated filenames
    """
    setA = loadProteinSet(proteinSetAPath)
    setB = loadProteinSet(proteinSetBPath)
    setAName = proteinSetAPath.replace(".tab","")
    setBName = proteinSetBPath.replace(".tab","")
    merged = mergeProteinSets(setA, setAName, setB, setBName)
    return writeProteinSets(merged)

if __name__ == '__main__':
    #--------------------------------------------------------------------------
    #   Definition of the command line arguments
    #--------------------------------------------------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("proteinSetA",
                        help="""Protein set A, given in tab format. Must 
                        contain 'Entry' and 'Organism' column """)
    parser.add_argument("proteinSetB",
                        help="""Protein set B, given in tab format. Must 
                        contain 'Entry' and 'Organism' column """)
    args = parser.parse_args()
    
    #--------------------------------------------------------------------------
    #   Main Code
    #--------------------------------------------------------------------------
    intersectProteinSets(args.proteinSetA, args.proteinSetB)