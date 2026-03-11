cfg?=Makefile.options
-include $(cfg)
#####################################################################################
work_dir?=v01
n_jobs?=16
train_config?=conf/style_melgan.v1.yaml
# need full path
tmp_dump_dir?=$(HOME)/dump
dump_dir?=dump
m_jobs?=10
speaker?=agn
dev_count?=250
#####################################################################################
info:
	@echo "corpus_file: 	${corpus_file}"
	@echo "work_dir: 		${work_dir}"
	@echo "train_config: 	${train_config}"
	@echo "speaker: 		${speaker}"
	@echo "dev_count: 		${dev_count}"
	@echo "exp_dir: 		${exp_dir}"
	@echo "final_model: 	${final_model}"
	@echo "nvidia-smi: 		$$(nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv | tail -n1)"
	@echo "cuda visible dev: 	$$(echo $$CUDA_VISIBLE_DEVICES)"
	@echo "python: 			$$(python --version)"
	@echo "torch: 			$$(python -c 'import torch; print(torch.__version__)')"
	@echo "cuda in python: 	$$(python -c 'import torch; print(torch.version.cuda) if torch.cuda.is_available() else "N/A"')"


.PHONY: info
#####################################################################################
$(work_dir)/downloads $(work_dir):
	mkdir -p $@
#####################################################################################
$(work_dir)/.prepare.done: | $(work_dir)
	./run.sh --stage -1 --stop-stage 1
	touch $@
prepare: $(work_dir)/.prepare.done
.PHONY: prepare
#####################################################################################
$(work_dir)/.train.done: $(work_dir)/.prepare.done
	./run.sh --stage 2 --stop-stage 2
	touch $@
train: $(work_dir)/.train.done
.PHONY: train
#####################################################################################
steps?=1000000
resume=$(exp_dir)/checkpoint-$(steps)steps.pkl
train/resume:
ifneq ($(skip-ask), true)
	@echo -n "Resume from $(resume)? [y/N] " && read ans && [ $${ans:-N} = y ]
endif
	./run.sh --stage 2 --stop-stage 2 	--resume $(resume)
.PHONY: train/resume	
#####################################################################################
version?=v01
final_model_name?=style.${version}
final_name?=$(speaker).$(final_model_name)-$(steps)
final_model=$(work_dir)/$(final_name).tar.gz
prepare_dir=prepared
exp_dir?=$(work_dir)/exp/train_nodev_${speaker}_style_melgan.v1
$(prepare_dir)/$(final_name):
	mkdir -p $@
$(prepare_dir)/$(final_name)/%: $(work_dir)/.train.done $(exp_dir)/% | $(prepare_dir)/$(final_name)
	cp $(exp_dir)/$* $@
$(prepare_dir)/.done: $(work_dir)/.train.done $(prepare_dir)/$(final_name)/checkpoint-$(steps)steps.pkl $(prepare_dir)/$(final_name)/config.yml $(prepare_dir)/$(final_name)/stats.h5
	touch $@
$(final_model): $(prepare_dir)/.done
	cd $(prepare_dir) && tar -czvf $@ $(final_name)
pack/model: $(final_model)
.PHONY: pack/model
#####################################################################################
build: pack/model
.PHONY: build
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
