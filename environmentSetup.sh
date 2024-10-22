# Prerequisites: Set up the conda environment and do the steps for Google Cloud Set Up (https://github.com/users/silvhua/projects/3/views/1?pane=issue&itemId=83178642)
# activate the conda environment for the project
conda activate datajam

# Set the environmental variables
# See here to find path to application_default_credentials.json https://cloud.google.com/docs/authentication/application-default-credentials#personal
conda env config vars set GOOGLE_APPLICATION_CREDENTIALS_PATH=path_to_application_default_credentials.json
conda env config vars set AWS_PROFILE=aws_profile_name
conda env config vars list