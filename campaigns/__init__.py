import os
import yaml

campaign_dirs = (x for x in os.listdir('campaigns') if os.path.isdir(os.path.join('campaigns', x)) and not x.startswith('_'))

CAMPAIGNS = {}
for campaign_dir in campaign_dirs:
    try:
        path = 'campaigns/{0}/'.format(campaign_dir)
        state_path = path + 'state.yaml'
        with open(state_path, 'r') as state_file:
            state = yaml.load(state_file.read())
            subjects_dict = {}
            campaign_dict = {
                'starting_state': state,
                'subjects': subjects_dict
            }
            subjects_path = path + 'subjects/'
            subject_json_files = (x for x in os.listdir(subjects_path) if x.endswith('.yaml'))
            for filename in subject_json_files:
                subject_path = subjects_path + filename
                with open(subject_path, 'r') as subject_json_file:
                    subject = yaml.load(subject_json_file.read())
                    id = filename.split('.')[0]
                    subjects_dict[id] = subject
            CAMPAIGNS[state['id']] = campaign_dict
    except Exception:
        raise

print(CAMPAIGNS)