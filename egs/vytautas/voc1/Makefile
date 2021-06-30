-include Makefile.options
#####################################################################################
USER=avaiciunas
SERVER_URL?=agpu
SSH_PORT?=22
HOME_DIR?=/home/avaiciunas

SSH_CMD=ssh -p $(SSH_PORT) -t $(USER)@$(SERVER_URL)
SSH_TF_CMD=ssh -L 6006:localhost:6006 -p $(SSH_PORT) -t $(USER)@$(SERVER_URL)
SSH_JN_CMD=ssh -L 8888:localhost:8888 -p $(SSH_PORT) -t $(USER)@$(SERVER_URL)
#####################################################################################
work_dir?=.
tts_dir=$(HOME_DIR)/gfs/tts
exp_dir?=exp/train_nodev_ljspeech_parallel_wavegan.v3
trans_type?=char
exp?=$(trans_type)_train_no_dev_pytorch_train_pytorch_tacotron2
cuda?=0
#####################################################################################
$(work_dir)/downloads:
	mkdir -p $@

init-data: | $(work_dir)/downloads	
#####################################################################################
logs:
	$(SSH_CMD) "cd $(exp_dir) && tail -n 40 -f exp/$(exp)/train.log"

nvidia:
	$(SSH_CMD) "watch nvidia-smi"
#####################################################################################
ssh:
	$(SSH_CMD)
#####################################################################################
prepare: 
	CUDA_VISIBLE_DEVICES=$(cuda) ./run.sh --stage -1 --stop-stage 1
	CUDA_VISIBLE_DEVICES=$(cuda) ./run.sh --stage 21 --stop-stage 21
#####################################################################################
train: 
	CUDA_VISIBLE_DEVICES=$(cuda) ./run.sh --stage 2 --stop-stage 2

#####################################################################################
steps?=700000
resume=$(exp_dir)/checkpoint-$(steps)steps.pkl
train-resume:
ifneq ($(skip-ask), true)
	@echo -n "Resume from $(resume)? [y/N] " && read ans && [ $${ans:-N} = y ]
endif
	CUDA_VISIBLE_DEVICES=$(cuda) ./run.sh --stage 2 --stop-stage 2 	--resume $(resume)
#####################################################################################
train-one:
	CUDA_VISIBLE_DEVICES=$(cuda) ./run.sh --stage $(stage) --stop-stage $(stage) 

train-many: 
	CUDA_VISIBLE_DEVICES=$(cuda) ./run.sh --stage $(from) --stop-stage $(to)

#####################################################################################
put-data:
	scp -P $(SSH_PORT) $(corpus_file) $(USER)@$(SERVER_URL):$(exp_dir)/downloads
#####################################################################################
final_name=vytautas.pwg.01-$(steps)
final_model=$(CURDIR)/$(final_name).tar.gz
prepare_dir=prepared
$(prepare_dir)/$(final_name):
	mkdir -p $@
$(prepare_dir)/$(final_name)/%: $(exp_dir)/% | $(prepare_dir)/$(final_name)
	cp $< $@
$(prepare_dir)/.done: $(prepare_dir)/$(final_name)/checkpoint-$(steps)steps.pkl $(prepare_dir)/$(final_name)/config.yml
	touch $@
$(final_model): $(prepare_dir)/.done
	cd $(prepare_dir) && tar -czvf $@ $(final_name)
prepare-model: $(final_model)
#####################################################################################
clean:
	@echo -n "Are you sure to delete $(work_dir)/...? [y/N] " && read ans && [ $${ans:-N} = y ]
	rm -rf $(work_dir)/data $(work_dir)/exp $(work_dir)/dump $(work_dir)/exp $(work_dir)/fbank $(work_dir)/tensorboard

clean-data:
	@echo -n "Are you sure to delete $(work_dir)/downloads? [y/N] " && read ans && [ $${ans:-N} = y ]
	rm -rf $(work_dir)/downloads
#####################################################################################
.EXPORT_ALL_VARIABLES:	
