'''
Created on Nov 5, 2013

@author: KHS
'''

from operator import itemgetter

class GeometricScoreFunction:
    
    
    def scoreClusters(self, clusterManager, resultManager, queryId ):
        """
        Score clusters using geometric cluster representation.
        Return a dictionary of cluster scores
        """
        clusterScores = {} # cluster scores
        
        for collection in clusterManager.getCollections(): # first collection name serves as the cluster id
            cluster = clusterManager.getCluster(collection)
            clusterScore = 1
            for clusterCollection in cluster:
                collectionScore = resultManager.getDocScore(queryId, clusterCollection)
                clusterScore *= collectionScore
            clusterScores[ collection ] = clusterScore
            
        return clusterScores
            
    
    def scoreCollections(self,  clusterManager, resultManager, clusterScores, queryId, boost=100 ):
       
        # sort clusters by score and extract unique collections
        clusterScoresSorted = sorted( clusterScores.iteritems(), key=itemgetter(1), reverse=True )
        
        # prepare result collection ranking        
        rerankedCollections  = {}
        
        for cluster in clusterScoresSorted:
            clusterId       = cluster[0]
            clusterScore    = cluster[1]
            if clusterScore != 0:
                
                clusterCollections = clusterManager.getCluster( clusterId )
                
                # add to each collection its initial score and sort it accordingly
                for pos in range(len(clusterCollections)):
                    collectionId    = clusterCollections[pos]
                    collectionScore = resultManager.getDocScore(queryId, collectionId)
                    #print collectionId, collectionScore
                    clusterCollections[pos] = ( collectionId, collectionScore )
                #print queryId, sorted(clusterCollections, key=itemgetter(1), reverse=True)
                
                # add collections to the results collection rankings
                for collection in clusterCollections:
                    collectionId    = collection[0] 
                    collectionScore = collection[1]
                    if collectionId not in rerankedCollections.iterkeys():
                        rerankedCollections[collectionId] = boost+collectionScore
                boost -=1
        
        return rerankedCollections