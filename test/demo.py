#!/usr/bin/env python
#-*- coding: utf-8 -*-
#PROJECT_NAME: F:\code\comencode\test
#CREATE_TIME: 2023-11-02 
#E_MAIL: renoyuan@foxmail.com
#AUTHOR: reno 
#note:  test

import sys,os
sys.path.insert(0,"..")
from comencode import Code_Compile

need_build_moduel = ["yourmoduel"]  # 指定需要编译的模块，需要有__init__.py 文件
filter_build_module = [ "setup.py", "config.py" "server.py","compile.py"]  # 指定不需要加密的文件目录或者文件
Code_Compile(need_build_moduel,filter_build_module,mode="obf_so")() # 指定模式 mode obf 混淆 so 编译c   obf_so混淆后编译 可能会出问提