## Sintezės emocinis garsynas

Recipe for training a vocoder for Lithuanian voice on SEG Corpus.

## Train

It trains style.melgan vocoder

### Preparation

1. Download corpus zip from: <pending>.
2. Prepare Makefile configuration file: `Makefile.options`:
   Add:
   1. full path to corpus file
   2. speaker 
   3. working dir for the experiment
   4. version (optional) - for marking the final file

Sample:
```make
corpus_file?=/home/user/dwn/corpus/AGN-1.0.zip
speaker?=agn
work_dir?=agn-01
version?=v01
```

### Test configuration
Run `make info`
Expected output:
```txt
corpus_file: 	/home/user/dwn/corpus/AGN-1.0.zip
work_dir: 		agn-01
train_config: 	conf/style_melgan.v1.yaml
speaker: 		agn
dev_count: 		250
exp_dir: 		agn-01/exp/train_nodev_agn_style_melgan.v1
final_model: 	agn-01/agn.style.v01-1000000.tar.gz
nvidia-smi: 	GeForce GTX 1080 Ti, 11178 MiB, 460.91.03
cuda visible dev: 0	
python: 		Python 3.10.20
torch: 			1.13.1+cu117
cuda in python: 11.7
```
Check that the corpus file and exp dir are correct. 
Check that cuda in python displays a version.

### Run model training
```bash
make build
## or in background
nohup make build &
```

A model will be trained and packed at: `${work_dir}/${speaker}.style.${version}-1000000.tar.gz`
