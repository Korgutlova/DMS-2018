from cassandra.cluster import Cluster


if __name__=='__main__':
    cluster = Cluster(['cassandra'])
    session = cluster.connect('avia')
