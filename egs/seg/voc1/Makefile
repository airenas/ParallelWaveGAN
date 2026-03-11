cfg?=Makefile.options
-include $(cfg)
#####################################################################################
work_dir?=.
cuda?=0
n_jobs?=16
train_config?=conf/style_melgan.v1.yaml
# need full path
tmp_dump_dir?=$(HOME)/dump
dump_dir?=dump
m_jobs?=10
speaker?=lina
#####################################################################################
$(work_dir)/downloads:
	mkdir -p $@
#####################################################################################
prepare:  
	CUDA_VISIBLE_DEVICES=$(cuda) ./run.sh --stage -1 --stop-stage 1
#####################################################################################
train: 
	CUDA_VISIBLE_DEVICES=$(cuda) ./run.sh --stage 2 --stop-stage 2
#####################################################################################
steps?=1000000
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
final_model_name?=style.v01
final_name?=$(speaker).$(final_model_name)-$(steps)
final_model=$(CURDIR)/$(final_name).tar.gz
prepare_dir=prepared
$(prepare_dir)/$(final_name):
	mkdir -p $@
$(prepare_dir)/$(final_name)/%: $(exp_dir)/% | $(prepare_dir)/$(final_name)
	cp $< $@
$(prepare_dir)/.done: $(prepare_dir)/$(final_name)/checkpoint-$(steps)steps.pkl $(prepare_dir)/$(final_name)/config.yml $(prepare_dir)/$(final_name)/stats.h5
	touch $@
$(final_model): $(prepare_dir)/.done
	cd $(prepare_dir) && tar -czvf $@ $(final_name)
prepare-model: $(final_model)
#####################################################################################
$(tmp_dump_dir):
	mkdir -p $@

preprocess-%: | $(tmp_dump_dir)
	parallel-wavegan-preprocess \
                --config "$(train_config)" \
                --scp "$(dump_dir)/wav.$*.scp" \
                --dumpdir "$(tmp_dump_dir)/$(dump_dir)/dump.$*" \
                --verbose "$(verbose)" 2>&1 | tee $(dump_dir)/preprocessing.$*.log
	mv $(tmp_dump_dir)/$(dump_dir)/dump.$* $(dump_dir)

normalize-%:
	parallel-wavegan-normalize \
                --config "$(train_config)" \
                --stats "$(stats)" \
                --rootdir "$(norm_dir)/raw/dump.$*" \
                --dumpdir "$(tmp_dump_dir)/$(norm_dir)/norm/dump.$*" \
                --verbose "$(verbose)" 2>&1 | tee $(norm_dir)/norm/normalize.$*.log 
	mv $(tmp_dump_dir)/$(norm_dir)/norm/dump.$* $(norm_dir)/norm		
#####################################################################################
clean:
	@echo -n "WARNING! Are you sure to delete $(work_dir)/... and data/...? [y/N] " && read ans && [ $${ans:-N} = y ]
	rm -rf $(work_dir)
	rm -rf data dump
.PHONY: clean	
clean/data:
	@echo -n "WARNING! Are you sure to delete downloads? [y/N] " && read ans && [ $${ans:-N} = y ]
	rm -rf downloads
.PHONY: clean/data	
#####################################################################################

.EXPORT_ALL_VARIABLES:	
