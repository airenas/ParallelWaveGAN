## Train

```bash
make prepare && make train
## or 
make prepare && nohup make train > v01.log &
```

## Pack model

```bash
make prepare-model steps=1500000 exp_dir=exp/train_nodev_ljspeech_style_melgan.v1 final_model_name=style.v02
```