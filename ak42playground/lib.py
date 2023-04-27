from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
import os


def parse_file(filename):
    config = TemplateMinerConfig()
    config.load("drain3.ini")
    template_miner = TemplateMiner(config=config)    
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        template_miner.add_log_message(line)

    cluster_file = filename + ".cluster"
    print("Generate cluster file: ", cluster_file)
    sorted_clusters = sorted(template_miner.drain.clusters, key=lambda it: it.size, reverse=True)
    with open(cluster_file, 'w') as f:
        f.write('cluster_id,count,signature\n')
        for cluster in sorted_clusters:
            f.write(str(cluster.cluster_id))
            f.write(',')
            f.write(str(cluster.size))
            f.write(',')
            f.write(cluster.get_template())
            f.write('\n')
    
    output_file = filename + ".output"
    print("Generate output file: ", output_file)
    with open(output_file, 'w') as f:
        f.write('cluster_id,message\n')
        for line in lines:
            line = line.strip()
            masked = template_miner.masker.mask(line)
            cluster = template_miner.drain.match(masked)
            if cluster is None:
                f.write('None')
            else:
                f.write(str(cluster.cluster_id))
            f.write(',')
            f.write(line)
            f.write('\n')
