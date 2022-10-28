import argparse
from myYoutube import YoutubeDetailsParser
from googleapiclient.errors import HttpError

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--pid', help='Search term', default='Google')
    # parser.add_argument('--max-results', help='Max results', default=25)
    # args = parser.parse_args()
    curr_pid: str
    
    curr_pid = "PL5Q2soXY2Zi97Ya5DEUpMpO2bbAoaG7c6"
    
    try:
        dp = YoutubeDetailsParser()
        dp.parse(pid=curr_pid)

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))