#
# Makefile for Parker Lab analysis {{ANALYSIS_NAME}}
#

ANALYSIS_NAME = {{ANALYSIS_NAME}}
CONTROL_PATH = {{CONTROL_PATH}}
ANALYSIS_PATH = {{ANALYSIS_PATH}}
DATA_PATH = {{ANALYSIS_PATH}}/data
WORK_PATH = {{ANALYSIS_PATH}}/work
CANCEL_SCRIPT = {{ANALYSIS_PATH}}/work/.drmr/{{ANALYSIS_NAME}}.cancel

.PHONY: run cancel clean clean_data clean_pipeline clean_work github_repo wiki_page

pipeline: $(ANALYSIS_PATH)/pipeline

work_directory:
	mkdir -p ${WORK_PATH}

$(ANALYSIS_PATH)/pipeline: $(CONTROL_PATH)/commands
	@mkdir -p $(ANALYSIS_PATH) && cd $(ANALYSIS_PATH) && chmod +x $(CONTROL_PATH)/commands && $(CONTROL_PATH)/commands

run: $(ANALYSIS_PATH)/pipeline
	@cd $(WORK_PATH) && drmr -j $(ANALYSIS_NAME) --mail-at-finish --mail-on-error $(ANALYSIS_PATH)/pipeline

$(CANCEL_SCRIPT):
	@mkdir -p `dirname $(CANCEL_SCRIPT)` && echo 'printf "\nThe pipeline has not been started in the usual way.\nYou will have to delete any running jobs manually.\n\n"' > $(CANCEL_SCRIPT)

cancel: $(CANCEL_SCRIPT)
	@cd $(WORK_PATH) && sh $(CANCEL_SCRIPT)

clean:
	@read -p "Enter 'yes' if you really want to delete your pipeline, data and work: " ANSWER && test "yesx" = "$${ANSWER}x" && rm -rf $(ANALYSIS_PATH)/pipeline $(DATA_PATH) $(WORK_PATH) && echo "All clean." || echo "OK, not deleting anything."

clean_data:
	@read -p "Enter 'yes' if you really want to delete your data staging directory: " ANSWER && test "yesx" = "$${ANSWER}x" && rm -rf $(DATA_PATH) && echo "Data staging directory deleted." || echo "OK, not deleting anything."

clean_pipeline:
	@rm -f $(ANALYSIS_PATH)/pipeline && echo "Pipeline script deleted."

clean_work:
	@read -p "Enter 'yes' if you really want to delete your work tree: " ANSWER && test "yesx" = "$${ANSWER}x" && rm -rf $(WORK_PATH) && echo "Work tree deleted." || echo "OK, not deleting anything."

github_repo:
	@hub create -p ParkerLab/$(ANALYSIS_NAME) && git push --set-upstream origin master

wiki_page:
	@(cat README.mediawiki; printf "\nIn progress at $$(hostname):$$(/bin/pwd)\n\n") | create_wiki_page "$(ANALYSIS_NAME)" -
