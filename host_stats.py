"""
Script for gathering host information:
- current RAM usage;
- current CPU usage;
- current number of processes running.
"""
import time
import datetime
import logging
import argparse
import psutil

STATS_TEMPLATE = '%s %s %s'


class HostStats(object):

    """
    Class for gathering CPU, RAM and PID statistics
    """

    def __init__(self, file_name):
        self.file_name = file_name

    def process_cpu_stats(self):
        """Get and process host CPU usage"""
        now = datetime.datetime.now().strftime('%H:%M:%S')
        cpu_usage = psutil.cpu_percent()
        cpu_stats = STATS_TEMPLATE % (now, 'CPU usage:', cpu_usage)

        if self.file_name:
            self._stats_to_file(cpu_stats)

        print cpu_stats

    def process_memory_stats(self):
        """Get and process host RAM usage"""
        now = datetime.datetime.now().strftime('%H:%M:%S')
        mem_usage = psutil.virtual_memory()
        mem_stats = STATS_TEMPLATE % (now, 'RAM usage:', mem_usage.used)

        if self.file_name:
            self._stats_to_file(mem_stats)

        print mem_stats

    def process_num_pids(self):
        """Get and process total number of running processes"""
        now = datetime.datetime.now().strftime('%H:%M:%S')
        total_pid = len(list(psutil.process_iter()))
        pid_stats = STATS_TEMPLATE % (now, 'Total PIDs:', total_pid)

        if self.file_name:
            self._stats_to_file(pid_stats)

        print pid_stats

    def _stats_to_file(self, data):
        """
        Append the data to a file
        :param data: data to append
        """
        with open(self.file_name, 'a') as files:
            files.write(data + '\n')

    def run(self, args):
        """Runs the stats gathering"""
        if args.ram:
            self.process_memory_stats()
        if args.cpu:
            self.process_cpu_stats()
        if args.pid:
            self.process_num_pids()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(module)s: '
                               '%(message)s', datefmt='%H:%M:%S')
    LOGGER = logging.getLogger(__name__)

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--cpu',
                        required=False,
                        action='store_true',
                        help='Process CPU usage')
    PARSER.add_argument('--ram',
                        required=False,
                        action='store_true',
                        help='Process RAM usage')
    PARSER.add_argument('--pid',
                        required=False,
                        action='store_true',
                        help='Process total number of running processes')
    PARSER.add_argument('--file-name',
                        dest='file_name',
                        required=False,
                        help='Name of the file to save the stats into')
    PARSER.add_argument('--delay',
                        type=int,
                        required=False,
                        help='Run stats gather in a loop with specified delay.'
                             'Only one stats measurement if not specified')
    ARGS = PARSER.parse_args()

    METRICS = [ARGS.ram, ARGS.cpu, ARGS.pid]
    if not any(METRICS):
        LOGGER.warning('No metrics specified for stats gathering. Exiting.')
        exit(0)

        LOGGER.info('Getting statistics from the host')
    if ARGS.file_name:
        LOGGER.info('The stats will be saved to specified file')

    STATS = HostStats(ARGS.file_name)

    if ARGS.delay:
        LOGGER.info('Running stats gathering in a loop '
                    'with %s seconds delay', ARGS.delay)
        try:
            while True:
                STATS.run(ARGS)
                time.sleep(ARGS.delay)
        except KeyboardInterrupt:
            LOGGER.warning('The script was interrupted by user')
    else:
        STATS.run(ARGS)
