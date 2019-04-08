from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import getopt
import base_logger
from tqdm import *
from wenku8toepub import Wenku8ToEpub


secret_id = 'AKIDcq7HVrj0nlAWUYvPoslyMKKI2GNJ478z'
secret_key = '70xZrtGAwmf6WdXGhcch3gRt7hV4SJGx'
region = 'ap-guangzhou'
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
# 2. 获取客户端对象
client = CosS3Client(config)

bucket = 'light-novel-1254016670'


def work(book_id: int, filename: str = None):
    wk = Wenku8ToEpub()
    if filename is None:
        filename_ = wk.id2name(book_id)
        if filename == '':
            return
        filename = "%s.epub" % filename_
    data = wk.get_book(book_id, bin_mode=True, fetch_image=False)
    response = client.put_object(
        Bucket=bucket,
        Body=data,
        # Key=filename_md5,
        Key="%s" % (filename, ),
        StorageClass='STANDARD',
        EnableMD5=False
    )
    logger.info("%s OK." % filename)


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], '-s:-e:', [])
    logger = base_logger.getLogger()
    start = 1
    end = 3000
    for name, val in opts:
        if name == '-s':
            try:
                start = int(val)
            except ValueError as e:
                logger.error(str(e))
                sys.exit()
        if name == '-e':
            try:
                end = int(val)
            except ValueError as e:
                logger.error(str(e))
                sys.exit()

    for _book_id in trange(start, end + 1, 1):
        work(_book_id)