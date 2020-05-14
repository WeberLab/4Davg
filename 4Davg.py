#!/usr/bin/python3

import sys
import math

import nibabel as nib
import os

from os import listdir

filename = str(sys.argv[1])

import nipype.interfaces.fsl as fsl

from os.path import basename

fullpath = os.path.abspath(filename)

dirpath = os.path.dirname(fullpath)

index_of_dot = filename.index('.')
base = filename[:index_of_dot]

#FSL Split 4D Image into 3D Volumes
split = fsl.Split()
split.inputs.dimension = 't'
split.inputs.in_file = filename
split.inputs.out_base_name = base+'_split'
print(split.cmdline)
split_res=split.run()

#FSL Merge to Merge some 3D Images into new 4D Image
merge = fsl.Merge()
merge.inputs.in_files = [basename(split_res.outputs.out_files[1]),basename(split_res.outputs.out_files[2]),basename(split_res.outputs.out_files[3])]
merge.inputs.dimension = 't'
merge.inputs.merged_file = base+'_merge2-4.nii.gz'
print(merge.cmdline)
merge_res = merge.run()

#FSL Maths to Compute Average Across Time
maths = fsl.ImageMaths()
maths.inputs.in_file = basename(merge.inputs.merged_file)
maths.inputs.op_string = '-Tmean'
maths.inputs.out_file = base+'_avg_2-4.nii.gz'
print(maths.cmdline)
maths_res = maths.run()

#remove Split and Merged Files
os.remove(basename(merge.inputs.merged_file))
for files in split_res.outputs.out_files:
    os.remove(basename(files))

