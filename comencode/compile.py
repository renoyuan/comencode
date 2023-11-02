#!/usr/bin/env python
#-*- coding: utf-8 -*-
#PROJECT_NAME: /home/reno/tl_test/test
#CREATE_TIME: 2023-11-01 
#E_MAIL: renoyuan@foxmail.com
#AUTHOR: reno 
#note:  compile & encipher  编译加密 使用PyObfuscator 混淆编译代码
import os
import re
import shutil
from distutils.core import setup
from Cython.Build import cythonize
from setuptools.command.build_ext import build_ext
"""
1 编译代码 ok 具有代码混淆以及 编译成so 两种方式 
1.1 运行代码混淆 需要python 3.9 以上混淆后的代码在其他版本也可以运行（3.8测试可以 ）注意存在模块名和内置模块一致 代码行数过长都可能导致混淆失败 。如有错误的地方需要调整源码
1.2 代码编译是将python 代码转成c 代码再转成 so 执行文件 编译后的文件 运行环境和编译的系统环境和python 解释器环境绑定，编译代码变量名需符合c 规范。如有错误的地方需要调整源码

"""
# PyObfuscator example.py -o obfuscated_example.py       

class Code_Compile(object):
    """编译代码"""
    
    def __init__(self,*args,**kwargs):
        """
        need_build_moduel 需要编译python 模块 :需要是python 模块
        filter_build_module 需要过滤编译目录和文件 注意避免重名
        mode: so|obf ->obfuscate | 
        """
        self.need_build_moduel, self.filter_build_module = args[0],args[1]
        self.mode = kwargs.get("mode","so")
        self.del_ori = kwargs.get("del_ori",False)
        
    def name_reflection(self,name_path):
        """生成映射后文件名"""
        dir_p ,name = os.path.split(name_path)  # 分割文件和路径 
        return os.path.join(dir_p ,f"ref_{name}")
    
    def scan_folder(self,input_moduel):
        """
        扫描得到需要编译文件绝对路径
        """
        file_list = []

        for f in os.listdir(input_moduel):
            if f in self.filter_build_module:
                continue
            
            f_name = os.path.abspath(os.path.join(input_moduel, f))
            if not os.path.isfile(f_name):
                file_list = file_list + self.scan_folder(f_name)
            else:
                if f.endswith(".py"):
                    file_list.append(f_name)

        return file_list
    
    def build_obfuscate(self,file_list):
        """执行混淆编译"""
        for ori_file in file_list:
            ref_name = self.name_reflection(ori_file)
            print(f'PyObfuscator {ori_file} -o {ref_name}')
            os.system(f'PyObfuscator {ori_file} -o {ref_name}')
            if self.del_ori and os.path.exists(ref_name) and os.path.exists(ori_file): # 删除原始文件
                os.remove(ori_file)
                os.rename(ref_name, ori_file)
           
    
    def build_cython(self,file_list):
        """编译文件并删除c过程文件"""
        setup(
            ext_modules = cythonize(file_list, language_level=2),
            cmdclass={'build_ext': build_ext},
            script_args=['build_ext', '--build-lib', 'build']
            
        )
        for fipy in file_list:
            if fipy.endswith(".py"):
                if os.path.exists(fipy.replace(".py", ".c")):
                    os.remove(fipy.replace(".py", ".c"))
                    print(f'delete file {fipy.replace(".py", ".c")}')

    def replace_del(self,moduel):
        """替换构建后的模块"""
        for lib_file in os.listdir(os.path.join('build')):
            if lib_file.startswith('lib'):
                mid_so_folder_path = os.path.join('build', lib_file)
                so_folder_path = os.path.join( mid_so_folder_path, moduel)
                
                for root, dirs, files in os.walk(so_folder_path):
                    if files:
                        for file in files:
                            src_path = os.path.join(root, file)
                            dst_path = os.path.join(root.replace(mid_so_folder_path, '').lstrip("/"), file)
                            print(src_path,dst_path)
                            shutil.copy2(src_path, dst_path)            
                            print('copy success, src path: {}, dst path: {}'.format(src_path, dst_path))
                            os.remove(dst_path.split('.cpython')[0] + '.py')
                            print(f'delete{"-"*20}> {dst_path.split(".cpython")[0] + ".py"}')
    
    def compile_by_so(self,):
        """代码编译成so"""
        for moduel in self.need_build_moduel:

            file_list = self.scan_folder(moduel)

            self.build_cython(file_list)

            # 将py替换成so, 并删除py
            self.replace_del(moduel)
            
    def compile_by_obf(self):
        """代码混淆"""
        for moduel in self.need_build_moduel:

            file_list = self.scan_folder(moduel)

            self.build_obfuscate(file_list)

    def __call__(self,):
        if self.mode == "so":
            self.compile_by_so()
        elif self.mode == "obf":
            self.compile_by_obf()
        elif self.mode == "obf_so":
            self.compile_by_obf()
            self.compile_by_so()
    # 删除build文件夹
    # shutil.rmtree(os.path.join(moduel, 'build'))

if __name__=='__main__':
    need_build_moduel = ["text_recogntiion","test"]  # 指定需要编译的模块，需要有__init__.py 文件
    filter_build_module = ["assets", "setup.py", "app_config.py" ,"gunicorn.py", "app_classification_server.py","compile.py"]  # 指定不需要加密的文件目录或者文件
    Code_Compile(need_build_moduel,filter_build_module,mode="obf_so")()

    
        
