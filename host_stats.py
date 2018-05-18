"""
Script for gathering host information:
- current RAM usage;
- current CPU usage;
- current number of processes running.
"""
import time
import datetime
import psutil
import logging
import argparse

STATS_TEMPLATE = '%s %s %s'
STATS_FILE = 'stats_file.log'

LOG = logger = logging.getLogger(__name__)


class HostStats(object):
    def __init__(self, save):
        self.save = save

    def process_cpu_stats(self):
        """
        Get and process host CPU usage
        """
        now = datetime.datetime.now().strftime('%H:%M:%S')
        cpu_usage = psutil.cpu_percent()
        cpu_stats = STATS_TEMPLATE % (now, 'CPU usage:', cpu_usage)
        if self.save:
            _stats_to_file(cpu_stats)
        print cpu_stats

    def process_memory_stats(self):
        """
        Get and process host RAM usage
        """
        now = datetime.datetime.now().strftime('%H:%M:%S')
        mem_usage = psutil.virtual_memory()
        mem_stats = STATS_TEMPLATE % (now, 'RAM usage:', mem_usage.used)
        if self.save:
            _stats_to_file(mem_stats)
        print mem_stats

    def process_num_pids(self):
        """
        Get and process total number of running processes on the host
        """
        now = datetime.datetime.now().strftime('%H:%M:%S')
        total_pid = len(list(psutil.process_iter()))
        pid_stats = STATS_TEMPLATE % (now, 'Total PIDs:', total_pid)
        if self.save:
            _stats_to_file(pid_stats)
        print pid_stats


def _stats_to_file(data):
    """
    Append the data to a file
    :param data: data to append
    """
    with open(STATS_FILE, 'a') as f:
        f.write(data + '\n')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(module)s: '
                               '%(message)s', datefmt="%H:%M:%S")

    parser = argparse.ArgumentParser()
    parser.add_argument("--stats",
                        required=False,
                        help="Comma separated stats to be shown. "
                             "Available: 'ram,cpu,mem'")
    parser.add_argument("--save",
                        action="store_true",
                        required=False,
                        help="Specify if need to save the stats to a file")
    args = parser.parse_args()

    if args.stats:
        args_filter = [a.strip() for a in args.stats.split(',')]
    else:
        args_filter = ['ram', 'cpu', 'pid']

    logger.info('Gathering statistics for: %s' % args_filter)

    if args.save:
        logger.info('All statistics will be saved to %s' % STATS_FILE)

    stats = HostStats(args.save)
    while True:
        for arg in args_filter:
            if 'ram' in arg:
                stats.process_memory_stats()
            if 'cpu' in arg:
                stats.process_cpu_stats()
            if 'pid' in arg:
                stats.process_num_pids()
        time.sleep(5)
