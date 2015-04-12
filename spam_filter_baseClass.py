# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 11:15:49 2015

@author: Taikor
"""


from lib import kw_spam_detect, read_from_json, retrive_basename, retrive_dirname


class spam_filter:
    """ spam_filter base class """
    def __init__(self, file_path, rule_path):   
        self.kwargs_rules = read_from_json(rule_path)
        self.file_path = file_path
        self.kwargs_field_position = None
        
    def kw_spam_recognize(self, line):
        """ filting and remove spams via spam kewword search """
        return kw_spam_detect(line, self.kwargs_rules, self.kwargs_field_position)
              
    def open_file(self, file_path):
        """ import data source from plain text file (routine) """ 
        with open(file_path, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            fields = lines.pop(0)    #remove the first element, which is the tag row in excel 
            
            field_list = fields.split('\t')
            field_list[0] = field_list[0].strip('\ufeff')
            field_list[-1] = field_list[0].strip('\n')
            self.kwargs_field_position = {key: field_list.index(key) for key in self.kwargs_rules.keys()}
            
            return lines
            
    def kw_batch_spam_rm(self):
        lines = self.open_file(self.file_path)
        offset = 0
        for i in range(len(lines)):
            if self.kw_spam_recognize(lines[i-offset]):
                del lines[i-offset]
                offset = offset + 1
        return lines
        
    def kw_spam_rm(self):
        lines = self.kw_batch_spam_rm()
        txt_string = "".join(lines)
        
        filted_basename = '(filted) ' + retrive_basename(self.file_path)
        filted_dirname = retrive_dirname(self.file_path)
        path = filted_dirname + '\\' + filted_basename
        with open(path, 'w') as f:
            f.write(txt_string)

