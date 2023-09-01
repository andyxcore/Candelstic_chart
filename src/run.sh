#!/bin/bash
if [ -d ../.venv ]
then
  echo "virtualenv exists, activating"
  source .venv/bin/activate
else
  echo "venv not exists, creating.. "
  python -m venv ../.venv/ && source ../.venv/bin/activate
  echo "Installing requirements: $(cat ../requirements.txt)"
  pip install -r ../requirements.txt
  echo "Success"
  echo
fi

echo "python main.py --data_path $1 --time_inter $2 --EMA_inter $3"
