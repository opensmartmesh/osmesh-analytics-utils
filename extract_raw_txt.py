import pandas as pd
import glob
from os.path import basename, dirname, join
import datetime


def build_datetime(month, day, time_str, year=2017):
    dt_str = str(year) + '/' + str(month) + '/' + str(day) + ' ' + time_str
    dt = datetime.datetime.strptime(dt_str, '%Y/%m/%d %X')
    return dt

def get_month_from_file_name(file_name):
    return basename(dirname(file_name))

def parse_file(file_name):
    month_str = get_month_from_file_name(file_name)

    df = pd.read_csv(file_name, sep='\t', names=['day', 'time', 'value'])

    df['date'] = [build_datetime(month_str, day, time_str) for day, time_str in zip(df['day'], df['time'])]

    del(df['time'])
    del(df['day'])

    print(df.head())
    return df

def get_full_date_and_convert_to_csv(input_file_dir, output_file_dir):
    all_files_txt = glob.glob(input_file_dir + '/*txt')

    for a_file in all_files_txt:
        df = parse_file(a_file)
        output_file_name = join(output_file_dir, basename(a_file)[:-3] + 'csv')
        df.to_csv(output_file_name, index=False)


if __name__ == "__main__":
    # data_dir1 = '/home/warnier/Works/opensmartmesh/data/01'
    # data_dir2 = '/home/warnier/Works/opensmartmesh/data/02'

    import sys

    if len(sys.argv) == 3:
        # Where are the raw .txt (\t separation) files with one column for day, one column for time and month information in the dir
        # year information is 2017 by default.
        input_file_dir = sys.argv[1]

        # Where to save csv files with one column for date
        output_file_dir = sys.argv[2]
        get_full_date_and_convert_to_csv(input_file_dir, output_file_dir)
        