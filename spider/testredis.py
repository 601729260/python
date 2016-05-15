import rediscluster
from rediscluster.client import StrictRedisCluster

startup_nodes=[{"host":"127.0.0.1","port":"7000"}]
rc=StrictRedisCluster(startup_nodes=startup_nodes,decode_responses=True)
rc.set('foo','bar')
value=rc.get('foo')
print value
    