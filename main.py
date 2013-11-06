'''
Created on Nov 5, 2013

@author: KHS
'''

from operator import itemgetter
from Clustering import Clustering
from ResManager import ResManager
from ScoreFunction import GeometricScoreFunction

def main():
    
    #************************** PARAMETERS *****************************
    fileCollectionSimilarities  = "./CollectionSimilarities/dbToDb.gov2.formattedExp"
    fileCollectionRanks         = "./CollectionRanks/ranks_gov2_crcs_clustfuse_ideal_50_50_0.0_701-850"
    fileCollectionRanksColumns  = 3
    clusterSize                 = 3
    collectionCutoff            = 5
    #*******************************************************************
    
    # compute clusters
    clustering = Clustering()
    clustering.computeOfflineClusters( fileCollectionSimilarities, clusterSize)
    #clustering.printClusters()
    
    
    # read colleciton scores
    resManager = ResManager()
    resManager.clean()
    resManager.readResults(fileCollectionRanks, fileCollectionRanksColumns)  
    
    # compute scores
    for query in resManager.getQueries():
        
        scoreFunction   = GeometricScoreFunction()
        clusterScores   = scoreFunction.scoreClusters( clustering, resManager, query )
        
        # prepare result collection ranking
        boost = 100 
        rerankedCollections  = scoreFunction.scoreCollections(clustering, resManager, clusterScores, query, boost )
       
        
        # check if the number of re-ranked collections satisfies collection cutoff
        # if it does not then append more collections to the end of the list
        if len(rerankedCollections) < collectionCutoff:
            initialCollectionIds    = resManager.getDocs(query)
            initialCollectionScores = resManager.getScores(query)
            pos = 0
            while pos < len(initialCollectionIds) and len(rerankedCollections) < collectionCutoff :
                collectionId = initialCollectionIds[pos]
                if not rerankedCollections.has_key(collectionId):
                    rerankedCollections[collectionId] = initialCollectionScores[pos]
                pos += 1
       
    
    
    print "ready"
    
    
    

if __name__ == '__main__':
    main()