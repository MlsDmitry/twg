#!/bin/bash

gltf2bam $1.gltf $1.bam
bam2egg $1.bam $1.egg
