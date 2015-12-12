#
# Makefile for Parker Lab analysis {{ANALYSIS_NAME}}
#

ANALYSIS_NAME = {{ANALYSIS_NAME}}
CONTROL_PATH = {{CONTROL_PATH}}
ANALYSIS_PATH = {{ANALYSIS_PATH}}

$(ANALYSIS_PATH)/pipeline: $(CONTROL_PATH)/commands
	@mkdir -p $(ANALYSIS_PATH) && cd $(ANALYSIS_PATH) && sh $(CONTROL_PATH)/commands

run: $(ANALYSIS_PATH)/pipeline
	@cd $(ANALYSIS_PATH)/work && swarm -j $(ANALYSIS_NAME) $(ANALYSIS_PATH)/pipeline

$(ANALYSIS_PATH)/work/$(ANALYSIS_NAME).cancel:
	@mkdir -p $(ANALYSIS_PATH)/work && echo 'printf "\nThe pipeline has not been started in the usual way.\nYou will have to delete any running jobs manually.\n\n"' > $(ANALYSIS_PATH)/work/$(ANALYSIS_NAME).cancel

cancel_run: $(ANALYSIS_PATH)/work/$(ANALYSIS_NAME).cancel
	@cd $(ANALYSIS_PATH)/work && sh $(ANALYSIS_NAME).cancel

clean:
	@read -p "Enter 'yes' if you really want to delete your pipeline, data and work: " ANSWER && [[ "yesx" = "$${ANSWER}x" ]] && rm -rf $(ANALYSIS_PATH)/pipeline $(ANALYSIS_PATH)/data $(ANALYSIS_PATH)/work && echo "All clean." || echo "OK, not deleting anything."

github_repo:
	@hub create -p ParkerLab/$(ANALYSIS_NAME) && git push --set-upstream origin master

wiki_page:
	@(cat README.mediawiki; printf "\nIn progress at $$(hostname):$$(/bin/pwd)\n\n") | create_wiki_page "$(ANALYSIS_NAME)" -
