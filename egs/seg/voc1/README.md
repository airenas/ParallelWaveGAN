## Train

```bash
make prepare && make train
## or 
make prepare && nohup make train > v01.log &
```

if there is a problem with a low hd space: 
```bash
make prepare m_jobs=4  # default 10
```

## Pack model

```bash
make prepare-model steps=1500000 exp_dir=exp/train_nodev_ljspeech_style_melgan.v1 final_model_name=style.v02
```


## Resume training

```bash
make train-resume steps=500000
## or 
nohup make train-resume steps=500000 skip-ask=true > v01.log &
```
