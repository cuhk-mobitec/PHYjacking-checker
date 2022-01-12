import os
from androguard.misc import AnalyzeAPK
import argparse
import datetime
import psutil
from analyzer import analyzer

def arg_parse():
    arg_parser = argparse.ArgumentParser(description='Analysis of PHY-Jacking Attack')
    arg_parser.add_argument('apk', metavar='FILE',
                            help='APK file to analyze')
    
    args = arg_parser.parse_args()
    return args


if __name__ == '__main__':
    
    args = arg_parse()
    apk_name = args.apk

    time_begin = datetime.datetime.now()
    print("start at:{}".format(time_begin))

    print("[*] Analyzing APK ...")
    # a for an APK object, d for an array of DalvikVMFormat object, dx for an Analysis object

    a, d, dx = AnalyzeAPK(apk_name)
    # camera1 API
    target_start = [('Landroid/hardware/Camera;','open'), ('Landroid/hardware/Camera;','startPreview'), ('Landroid/hardware/Camera;','takePicture')]
    target_close = [('Landroid/hardware/Camera;','stopPreview'), ('Landroid/hardware/Camera;','release')]
    analysis = analyzer(dx, target_start, target_close)
    result = analysis.jackvul_analysis()

    print("\n[*] Result----------------------------")
    print(result[0])
    for act in result[1]:
        print(act)
    print("[*] ----------------------------------") 
    time_end = datetime.datetime.now()
    time = time_end - time_begin
    print("\nend at:{}".format(time_end))
    print("total time:{}".format(time))
    process=psutil.Process(os.getpid())
    print("Maximum Memory Usage: {} MB".format(process.memory_info().rss/1024/1024))