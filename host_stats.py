"""
Script for gathering host information:
- current RAM usage;
- current CPU usage;
- current number of processes running.
"""
import argparse
import datetime
import logging
import time

import psutil

STATS_TEMPLATE = '%s %s %s'


class HostStats(object):

    """
    Class for gathering CPU, RAM and PID statistics
    """

    def __init__(self, file_name):
        self._file_name = file_name

    def process_cpu_stats(self):
        """Get and process host CPU usage"""
        now = datetime.datetime.now().strftime('%H:%M:%S')
        cpu_usage = psutil.cpu_percent()
        cpu_stats = STATS_TEMPLATE % (now, 'CPU usage:', cpu_usage)

        if self._file_name:
            self._stats_to_file(cpu_stats)

        print cpu_stats

    def process_memory_stats(self):
        """Get and process host RAM usage"""
        now = datetime.datetime.now().strftime('%H:%M:%S')
        mem_usage = psutil.virtual_memory()
        mem_stats = STATS_TEMPLATE % (now, 'RAM usage:', mem_usage.used)

        if self._file_name:
            self._stats_to_file(mem_stats)

        print mem_stats

    def process_num_pids(self):
        """Get and process total number of running processes"""
        now = datetime.datetime.now().strftime('%H:%M:%S')
        total_pid = len(list(psutil.process_iter()))
        pid_stats = STATS_TEMPLATE % (now, 'Total PIDs:', total_pid)

        if self._file_name:
            self._stats_to_file(pid_stats)

        print pid_stats

    def _stats_to_file(self, data):
        """
        Append the data to a file
        :param data: data to append
        """
        with open(self._file_name, 'a') as files:
            files.write(data + '\n')

    def run(self, args):
        """Runs the stats gathering"""
        if args.ram:
            self.process_memory_stats()
        if args.cpu:
            self.process_cpu_stats()
        if args.pid:
            self.process_num_pids()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpu',
                        required=False,
                        action='store_true',
                        help='Process CPU usage')
    parser.add_argument('--ram',
                        required=False,
                        action='store_true',
                        help='Process RAM usage')
    parser.add_argument('--pid',
                        required=False,
                        action='store_true',
                        help='Process total number of running processes')
    parser.add_argument('--file-name',
                        dest='file_name',
                        required=False,
                        help='Name of the file to save the stats into')
    parser.add_argument('--delay',
                        type=int,
                        required=False,
                        help='Run stats gather in a loop with specified delay.'
                             'Only one stats measurement if not specified')

    args = parser.parse_args()
    return args


def main():
    """Initialize HostStats class object and run the stats gathering"""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(module)s: '
                               '%(message)s', datefmt='%H:%M:%S')
    logger = logging.getLogger(__name__)

    args = parse_args()
    metrics = [args.ram, args.cpu, args.pid]
    if not any(metrics):
        logger.warning('No metrics specified for stats gathering. Exiting.')
        exit(0)

    logger.info('Getting statistics from the host')
    if args.file_name:
        logger.info('The stats will be saved to specified file')

    stats = HostStats(args.file_name)

    if args.delay:
        logger.info('Running stats gathering in a loop '
                    'with %s seconds delay', args.delay)
        try:
            while True:
                stats.run(args)
                time.sleep(args.delay)
        except KeyboardInterrupt:
            logger.warning('The script was interrupted by user')
    else:
        stats.run(args)


if __name__ == '__main__':
    main()
