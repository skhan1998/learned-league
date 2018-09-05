#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 16:36:00 2018

@author: samirkhan
"""
import numpy as np 

#This file contains code for publishing results


def publish(neighbors, y_neighbors, new_raw, title):  
    def parse_y(y):
        if y == 1:
            return "Yes"
        else:
            return "No"
    
    with open("%s.tex" % title, "w") as f:
        f.write(r'\documentclass{article}' + "\n")
        f.write(r'\usepackage[margin=0.65in]{geometry}' + "\n")
        f.write(r'\usepackage{mathpazo}' + "\n")
        f.write(r'\usepackage{booktabs}' + "\n")
        f.write(r'\renewcommand{\arraystretch}{1.5}' + "\n")
        f.write(r'\begin{document}' + "\n")
            
        for j in range(6):            
            neigh = neighbors[j]
            y_neigh = y_neighbors[j]
            
            f.write(r'\section*{Question %.0f}' % (j+1))
            f.write("The question is: %s It is similar to:" % new_raw[j])
            f.write("\n\n")
            f.write(r'\vspace*{0.25in}')
            f.write(r'\begin{tabular}{p{6in}l}')
            f.write(r'\toprule ')
            f.write(r'{\sc Question Text}& {\sc Correct?}\\')
            f.write(r'\midrule ')        
            for z in zip(neigh, y_neigh):
                f.write(r'%s& %s\\' % (z[0].encode("utf-8"), parse_y(z[1])))
            f.write(r'\bottomrule ')
            f.write(r'\end{tabular}')
            f.write("\n\n")
            f.write(r'\vspace*{0.5in}')
            f.write(r'Of these, %.1f\%% were answered correctly.' % (100*np.mean(y_neigh)))
            f.write(r'\newpage ')
            
        f.write(r'\end{document}')
