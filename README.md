#Chordiogram

Tools for chord representation and Audio Chord Estimation.

##Dependencies and versions

- Essentia, version 2.1-beta5-dev : https://essentia.upf.edu/
- To use NNLS chroma, install vamp plugin from http://isophonics.net/nnls-chroma ; information about installation can be found at https://www.vamp-plugins.org/download.html#install
- To use chord readers (in reader.py), install pygame : https://www.pygame.org/download.shtml

Version of python used : 3.6.8

##Data

This repository uses the Jazz Audio Aligned-Harmony dataset (JAAH), developed by Vsevolod Eremenko, Emir Demirel, Baris Bozkurt and Xavier Serra.

For an optimum use, clone this repository in a folder with two other folders :
- /json : the 113 annotation files taken from https://github.com/MTG/JAAH/tree/master/annotations
- /sounds : the 113 audio files (not publicly available)

For further information about the JAAH dataset, see https://mtg.github.io/JAAH/

##Context

This repository has been elaborated at the Music Technology Group of the Universitat Pompeu Fabra in Barcelona, under the supervision of Vsevolod Eremenko and Xavier Serra.