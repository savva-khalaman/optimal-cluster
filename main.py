'''
Created on Nov 5, 2013

@author: KHS
'''

from operator import itemgetter
from Clustering import Clustering
from ResManager import ResManager
from ScoreFunction import GeometricScoreFunction

OFFLINE_CLASTERING  = 'offline'
ONLINE_CLASTERING   = 'online'

def main():
    
    #************************** PARAMETERS *****************************
    fileCollectionSimilarities  = "./CollectionSimilarities/dbToDb.gov2.formattedExp"
    fileCollectionRanks         = "./CollectionRanks/ranks_gov2_crcs_clustfuse_ideal_50_50_0.0_701-850"
    fileCollectionRanksUpd      = "./CollectionRanks/ranks_gov2_crcs_clustfuse_ideal_50_50_0.0_701-850_upd"
    clusteringType              = "online"
    fileCollectionRanksColumns  = 3
    clusterSize                 = 3
    collectionRerankCutoff      = 10
    collectionSearchCutoff      = 5
    #*******************************************************************
    
    # compute clusters
    clustering = Clustering()
    clustering._readSimilarities(fileCollectionSimilarities)
    if clusteringType == OFFLINE_CLASTERING:
        clustering.computeOfflineClusters( fileCollectionSimilarities, clusterSize)
        #clustering.printClusters()
    
    
    # read collection scores
    resManager = ResManager()
    resManager.clean()
    resManager.readResults(fileCollectionRanks, fileCollectionRanksColumns)  
    
    # open output stream
    otp = open(fileCollectionRanksUpd, 'w')
    
    # compute scores
    for query in resManager.getQueries():
        
        if clusteringType == ONLINE_CLASTERING:
            initialCollectionSet = resManager.getDocs(query, collectionRerankCutoff)
            clustering.computeOnlineClusters(initialCollectionSet, clusterSize)
            print query, clustering.clusters.keys()
            print query, clustering.clusters

        scoreFunction   = GeometricScoreFunction()
        clusterScores   = scoreFunction.scoreClusters( clustering, resManager, query )
        
        # prepare result collection ranking
        boost = 100 
        rerankedCollections  = scoreFunction.scoreCollections(clustering, resManager, clusterScores, query, boost )
        print query, rerankedCollections
        
        # check if number of re-ranked collections satisfies collection cutoff
        # if it does not, then append more collections to the end of the list
        if len(rerankedCollections) < collectionSearchCutoff:
            initialCollectionIds    = resManager.getDocs(query)
            initialCollectionScores = resManager.getScores(query)
            pos = 0
            while pos < len(initialCollectionIds) and len(rerankedCollections) < collectionSearchCutoff :
                collectionId = initialCollectionIds[pos]
                if not rerankedCollections.has_key(collectionId):
                    rerankedCollections[collectionId] = initialCollectionScores[pos]
                pos += 1
        
        
        # save results to a file
        for collection in sorted( rerankedCollections.iteritems(), key=itemgetter(1), reverse=True ):
            otp.write( " ".join( [query, collection[0], str(collection[1])] ) + '\n' )
    
    otp.close()
    print "ready"
    
    
    

if __name__ == '__main__':
    main()